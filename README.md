# fastapi-sqlalchemy-boilerplate

This project provides a boilerplate for a FastAPI application integrated with SQLAlchemy 2 (async) and the [databases](https://pypi.org/project/databases/) library for async database interactions. It uses PostgreSQL as the database backend and Docker is used to set up the PostgreSQL container.

## Setup Instructions

### 1. Copy Environment Variables

Before starting the project, create a `.env` file by copying the provided `example.env`:

```bash
cp example.env .env
```

### 2. Run PostgreSQL with Docker Compose

Start the PostgreSQL container using Docker Compose:

```bash
docker-compose up -d
```

This will spin up a PostgreSQL database that the FastAPI application will connect to.

### 3. Install Dependencies

Install the project dependencies using `pipenv`:

```bash
pipenv shell
pipenv install --dev
```

This will install the required libraries for development and testing.

### 4. Apply Database Migrations

To apply database migrations, run the following command:

```bash
make migrate_head
```

This will ensure that the database schema is up to date.

### 5. Run the Application

Start the FastAPI application with:

```bash
make run
```

The application will now be available at [http://localhost:8000/docs#/](http://localhost:8000/docs#/), where you can interact with the API documentation.

### 6. Running Tests

To run the project's tests, you can execute `pytest` from the root directory:

```bash
pytest
```

This will run all the tests defined in the project.

## Technologies Used

- **FastAPI**: Fast web framework for building APIs with Python.
- **SQLAlchemy 2 (Async)**: ORM for Python with async support.
- **Databases**: Asynchronous database query library.
- **PostgreSQL**: Relational database management system used for storage.
- **Docker**: To run PostgreSQL in a container.
- **Pipenv**: To manage project dependencies.

## Notes

- Ensure that PostgreSQL is running before you attempt to start the FastAPI application.
- The `make migrate_head` command applies the latest database migrations. Make sure the database is initialized and running.
- To generate a new migration, use the command `make create_migration name=new_migration` 

---

Happy coding! 🚀
