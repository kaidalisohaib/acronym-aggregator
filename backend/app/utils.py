import csv
import os
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app import app, db
from app.models import Acronym, Report
from flask_sqlalchemy import BaseQuery
from sqlalchemy import String, cast
from werkzeug.datastructures import MultiDict


def string_is_empty(string: str) -> bool:
    """Verify if a string is empty. Empty means that the string lenght
    is zero or that the string contains only white spaces.

    Args:
        string (str): String to test.

    Returns:
        bool: If the string is empty True, otherwise False.
    """
    return len(string.strip()) == 0


def generate_new_report() -> int:
    """Generate the zip file that contains the csv report.

    Raises:
        Exception: If anything goes wrong.

    Returns:
        int: The id of the new report.
    """
    try:
        # Create temp dir if it doesn't exist
        temp_path = Path(tempfile.gettempdir())
        temp_path.mkdir(exist_ok=True)

        # Create report dir if it doesn't exist
        new_report = Report(temp_path.absolute())
        db.session.add(new_report)
        # Commit so we can get the new id
        db.session.commit()

        # Latest version number
        new_version = new_report.id

        # Create the reports dir if it doesn't exist
        reports_path = Path(app.config["REPORTS_FOLDER"])
        reports_path.mkdir(exist_ok=True)

        # New csv file path
        new_csv_temp_path: Path = temp_path.joinpath(f"all_acronyms_v{new_version}.csv")
        # New pdf file path
        new_pdf_temp_path: Path = temp_path.joinpath(f"all_acronyms_v{new_version}.pdf")
        # New report zip file path
        new_zip_path: Path = reports_path.joinpath(f"all_acronyms_v{new_version}.zip")

        # Create and fill the csv file
        create_and_fill_csv_file(str(new_csv_temp_path.absolute()))
        # Create and fill the pdf file
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
        # Update the zip path to the correct one
        Report.query.get(new_version).zip_path = str(new_zip_path.absolute())
        db.session.commit()
        return new_version
    except Exception:
        # If anything goes wrong remove the report and raise an Exception
        db.session.rollback()
        Report.query.filter(Report.id == new_version).delete()
        db.session.commit()
        raise Exception("Could't generate a new report.")
    finally:
        # In all cases, remove the tmp files if they exists.
        if new_csv_temp_path.exists():
            os.remove(new_csv_temp_path)
        if new_pdf_temp_path.exists():
            os.remove(new_pdf_temp_path)


def create_and_fill_csv_file(filepath: str) -> None:
    """Fill a csv file with all the acronyms.
    Writes only the acronym, meaning, comment and company rows.

    Args:
        filepath (str): The absolute path of the wanted csv file path.
    """
    with open(filepath, "w") as file:
        out = csv.writer(file)
        # Write headers
        out.writerow(["acronym", "meaning", "comment", "company"])
        # Write only the acronym, meaning, comment and company rows into the file
        for acronym in Acronym.query.all():
            out.writerow(
                [
                    acronym.acronym,
                    acronym.meaning,
                    acronym.comment,
                    acronym.company,
                ]
            )


# For now this function does nothing because I didn't found a library
# to generate a good pdf file
def create_and_fill_pdf_file(filepath: str) -> None:
    pass


def allowed_upload_file(filename: str) -> bool:
    """Verify if the filename is allowed to upload into the server.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: Returns if it's allowed.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def build_acronyms_filter_sort_query(args: MultiDict) -> BaseQuery:
    """Build a query with the filters to apply and the column to sort

    Args:
        args (MultiDict): The arguments of the request.

    Returns:
        BaseQuery: The query object that contains all the filters and sort.
    """

    query_object = Acronym.query
    # Adding filters to the query
    # For each argument we verify if it start with the word "filter"
    # and then we isolate the column name by slicing it
    # e.g: filter[id] -> id
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
    # If there is no sorting column we sorte the query by the id
    else:
        query_object = query_object.order_by(Acronym.id)

    return query_object
