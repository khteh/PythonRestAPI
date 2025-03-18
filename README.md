# PythonFlaskRestAPI

Python RestAPI using Quart HTTP/3 ASGI framework.

## Environment setup

- On a development host, create a virtual environment for development and test. Both must be using the same virtual environment.
- Virtual environment is optional for CI/CD do because everything runs in a docker container.
- Add the following to `.env` for database access credentials:

```
DB_USERNAME=username
DB_PASSWORD=password
```

### Clean up pipenv

- `pipenv --rm`
- `pipenv --clear`
- `pipenv lock --clear --verbose`

### Setup new pipenv

```
$ pipenv install
$ pipenv shell
```

## Database setup:

- This project uses PostgreSQL database with SQLAlchemy ORM with marshmallow for object SerDes.

## Install python modules

```
$ pipenv install --python=/path/to/python
$ cd src
$ pipenv install --python=/path/to/python
$ cd test
$ pipenv install --python=/path/to/python
```

## Create Database

- Firstly, create an empty database "library" in PostgreSQL

## Database Migration

- run migrations initialization with db init command:

  ```
  $ pipenv run alembic init migrations
  $ pipenv run alembic revision --autogenerate -m "Initial migration"
  $ pipenv run alembic upgrade head
  ```

- There will be 3 tables, "users", "books", and "authors" created in the PostgreSQL database "library" after the `upgrade`.

# Test using PyTest:

- There are 7 test cases
  - JWT token generation and decoding
  - HomeController
  - FibonacciController
  ```
  $ pipenv run pytest -v
  $ python -m pytest
  ```

# Continuous Integration:

- Integrated with CircleCI

# Start the application:

- `./quart.sh`

## Create User:

- POST https://localhost:4433/users/create with the following JSON data:
  ```
  {
      "firstname": "First Name",
      "lastname": "LastName",
      "email": "firstname.lastname@email.com",
      "password": "P@$$w0rd"
  }
  ```

## Login:

- POST https://localhost:4433/users/login with the following JSON data:
  ```
  {
      "email": "firstname.lastname@email.com",
      "password": "P@$$w0rd"
  }
  ```
- Sample response:
  ```
  {
      "jwt_token": "token string"
  }
  ```

## Subsequent request header:

```
Key: api-key
Vaue: jwt_token from the login response
```

## Create Author:

- POST https://localhost:4433/authors/create with the following JSON data:
  ```
  {
      "email": "jk@email.com",
      "firstname": "JK",
      "lastname": "Rowing"
  }
  ```

## Create Book:

- POST https://localhost:4433/books/create with the following JSON data:
  ```
  {
      "author_id": 1,
      "isbn": "123456",
      "page_count": "123",
      "title": "My First Book"
  }
  ```

## Delete an author:

- Books table has a foreign key id to Authors.id and this is defined as required in BookSchema.
- Therefore, when a DELETE RESTful operation is sent to the application to delete an author which has associated book:

```
mysql.connector.errors.IntegrityError: 1048 (23000): Column 'author_id' cannot be null
```

## Get Requests:

- Headers:

  ```
  Key: api-key
  Vaue: jwt_token from the login response
  ```

- visit https://localhost:4433
- visit https://localhost:4433/fibonacci/
- visit https://localhost:4433/users/all
- visit https://localhost:4433/authors/all
- visit https://localhost:4433/books/all
