# Accronym aggregator

This website provide a portal to view, create, upload, update and delete acronyms.
The purpose of this web app is to centralize all the acronyms of an organisation.

## Description

- The backend of the website provide the api to view/create/upload/update/delete the acronyms.
- To create/upload/update/delete acronyms you need to be logged in.
- To upload some acronyms you need to send a csv file with a specific format described in the upload page.
- You can also create and download a report in a csv format.
- You can register and login.
- For certain api routes that require logging in, a JWT token is sent with the request to make sure the user is logged in.

## Getting Started

### Dependencies

All you need is [docker](https://www.docker.com/products/docker-desktop/). The docker compose stack downloads everything the app need.

- Stack/Containers:
  - Postgres db for development.
  - Postgres db for testing.
  - Flask app for backend api.
  - Ember.js for frontend.

### Installing

1. Download [docker](https://www.docker.com/products/docker-desktop/)
2. Download the repository.
3. You can edit the `.env` file in the backend folder.

### Executing program

1. Create a `.env` file inside the backend folder. (Use the `.env.example` for the template)
2. Open a terminal in the current working directory.
3. Execute the command below to create and start the containers. You can add the `-d` flag if you want to launch the stack in detached mode.

```
docker compose up
```

<small>The command should take around 6-7 mins to download the images and setup the stack.</small>

4. Once everything has built, open this address `127.0.0.1:4200` in your browser to view the website.

## Help

If for any reason you encounter some error, try to delete all the containers, images and volumes and try to recreate the images again.

## Author

- [Kaidali Sohaib](https://github.com/kaidalisohaib)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
