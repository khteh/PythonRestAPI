# PythonFlaskRestAPI
Python RestAPI using Quart ASGI framework. It runs on HTTP/2 and will be HTTP/3 when mainstream browsers support it in the near future.

# Database setup:
* This project uses MySQL database with SQLAlchemy ORM with marshmallow for object SerDes.
## Install python modules
```
cd src
pipenv install
cd test
pipenv install
```
## To use Flask CLI in virtual environment:
* `python -m venv venv`
* `. venv/bin/activate`
* `flask <command>`
* `deactivate` to leave the venv

## Create Database
* Firstly, create an empty database "library" in MySQL 8.0

## Database Migration
* run migrations initialization with db init command:
```
$ pipenv run alembic init migrations
$ cp alembic_migrations_env.py migrations/env.py
$ pipenv run alembic revision --autogenerate -m "Initial migration"
$ pipenv run alembic upgrade head
```
* There will be 3 tables, "users", "books", and "authors" created in the MySQL database "library" after the `upgrade`.

# Test using PyTest:

* There are 7 test cases
  - JWT token generation and decoding
  - HomeController
  - FibonacciController
```
$ pytest -v
$ python -m pytest
```
# Continuous Integration:
* Integrated with CircleCI

# Start the application:
* `pipenv shell`
* `./quart.sh`

## Create User:
* POST https://localhost:8080/users/create
```
{
	"firstname": "First Name",
	"lastname": "LastName",
	"email": "firstname.lastname@email.com",
	"password": "P@$$w0rd"
}
```
## Login:
* POST https://localhost:8080/users/login
```
{
	"email": "firstname.lastname@email.com",
	"password": "P@$$w0rd"
}
```
* Response:
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
* POST https://localhost:8080/authors/create
```
{
    "email": "jk@email.com",
    "firstname": "JK",
    "lastname": "Rowing"
}
```
## Create Book:
* POST https://localhost:8080/books/create
```
{
    "author_id": 1,
    "isbn": "123456",
    "page_count": "123",
    "title": "My First Book"
}
```
## Delete an author:
* Books table has a foreign key id to Authors.id and this is defined as required in BookSchema.
* Therefore, when a DELETE RESTful operation is sent to the application to delete an author which has associated book:
```
mysql.connector.errors.IntegrityError: 1048 (23000): Column 'author_id' cannot be null
```
## Get Requests:
* Headers:
```
Key: api-key
Vaue: jwt_token from the login response
```
* visit https://localhost:8080
* visit https://localhost:8080/fibonacci/
* visit https://localhost:8080/users/all
* visit https://localhost:8080/authors/all
* visit https://localhost:8080/books/all
