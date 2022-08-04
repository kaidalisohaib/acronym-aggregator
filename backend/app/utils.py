import csv
import os
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app import app, db
from app.models import Acronym, Report
from flask_sqlalchemy import BaseQuery
from sqlalchemy import String, cast


def string_is_empty(value: str):
    return len(value.strip()) == 0


def generate_new_report():
    try:
        # Create temp dir if it doesn't exist
        temp_path = Path(tempfile.gettempdir())
        temp_path.mkdir(exist_ok=True)

        new_report = Report(temp_path.absolute())
        db.session.add(new_report)
        db.session.commit()

        # Latest version number
        new_version = new_report.id

        # Create the reports dir if it doesn't exist
        reports_path = Path(app.config["REPORTS_FOLDER"])
        reports_path.mkdir(exist_ok=True)

        # New csv file
        new_csv_temp_path: Path = temp_path.joinpath(f"all_acronyms_v{new_version}.csv")
        # New pdf file
        new_pdf_temp_path: Path = temp_path.joinpath(f"all_acronyms_v{new_version}.pdf")
        # New report zip file
        new_zip_path: Path = reports_path.joinpath(f"all_acronyms_v{new_version}.zip")
        create_and_fill_csv_file(str(new_csv_temp_path.absolute()))
        create_and_fill_pdf_file(str(new_pdf_temp_path.absolute()))
        # Compress the generated files
        with ZipFile(new_zip_path, mode="w") as zipfile:
            if new_csv_temp_path.exists():
                zipfile.write(
                    new_csv_temp_path.absolute(),
                    new_csv_temp_path.name,
                    compress_type=ZIP_DEFLATED,
                )

            if new_pdf_temp_path.exists():
                zipfile.write(
                    new_pdf_temp_path.absolute(),
                    new_pdf_temp_path.name,
                    compress_type=ZIP_DEFLATED,
                )
        Report.query.get(new_version).zip_path = str(new_zip_path.absolute())
        db.session.commit()
        return new_version
    except Exception:
        db.session.rollback()
        Report.query.filter(Report.id == new_version).delete()
        db.session.commit()
        raise Exception("Could't generate a new report.")
    finally:
        if new_csv_temp_path.exists():
            os.remove(new_csv_temp_path)
        if new_pdf_temp_path.exists():
            os.remove(new_pdf_temp_path)


def create_and_fill_csv_file(filepath: Path):
    "Fill a csv file with all the acronyms"
    with open(filepath, "w") as file:
        out = csv.writer(file)
        # out.writerow(Acronym.__table__.columns.keys())
        out.writerow(["acronym", "meaning", "comment", "company"])
        # Write all rows into the file
        for acronym in Acronym.query.all():
            out.writerow(
                [
                    acronym.acronym,
                    acronym.meaning,
                    acronym.comment,
                    acronym.company,
                    # getattr(acronym, column_name)
                    # for column_name in Acronym.__table__.columns.keys()
                ]
            )


# For now this function does nothing because I didn't found a library
# to generate a good pdf file
def create_and_fill_pdf_file(filepath: Path):
    pass


def allowed_file(filename) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def build_acronyms_filter_sort_query(args) -> BaseQuery:
    """Build a query with the filters given and the column to sort

    Keyword arguments:
    argument -- Parameters of the api request
    Return: return_description
    For each column we verify if the args contains the proper keyword
        If yes we add the filter
        Else we continue to the next column
    """

    query_object = Acronym.query
    # Adding filters to the query
    for key, value in args.items():
        if key.startswith("filter"):
            # 7 is the length of the word "filter" + 1
            # I only take the name of the column inside the square brackets
            column_name = key[7:-1]
            column = getattr(Acronym, column_name)
            query_object = query_object.filter(
                cast(column, String).contains(str(value))
            )
    # Adding the sorting to the query
    if "sorting[column]" in args:
        if args["sorting[ascending]"]:
            query_object = query_object.order_by(
                getattr(Acronym, args["sorting[column]"]).asc(), Acronym.id
            )
        else:
            query_object = query_object.order_by(
                getattr(Acronym, args["sorting[column]"]).desc(), Acronym.id
            )
    else:
        query_object = query_object.order_by(Acronym.id)

    return query_object
