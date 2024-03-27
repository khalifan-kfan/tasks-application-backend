# Tasks Application

Tasks management application and user actions.

### Project Setup

Follow these steps to have a local running copy of the app.

### Clone The Repo

```bash
git clone https://github.com/khalifan-kfan/tasks-application-backend.git
```

### Running application with Docker

---

`make` is a build automation tool that is used to manage the build process of a software project.

- In the project directory, running `make` shows you a list of commands to use.
- Run `make start` to start the application and required services.
- Run `make connect-to-container` to connect to the FastAPI application container.
- Run `make stop` to stop the application and required services.
- Run `make test` to test the application

After you run the application, checkout
`` http://localhost:8000/docs`  `` to see the API documentation.

### Available services

---

- `tasks-app`: Application API server (Default port: 8000)
- `tasks-mongo-db`: Applications MongoDB Server (Default port: 27001)
