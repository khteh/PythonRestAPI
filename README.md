# PythonFlaskRestAPI
Python RestAPI using Flask web Framework and marshmallow for SerDes.

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
python -m src.manage db init
```
* OR (may need to be inside the venv):
```
flask db init
```
* Populate migrations files and generate users and blogs tables with our model changes:
```
python -m src.manage db migrate
```
* OR (may need to be inside the venv):
```
flask db migrate
```

* Apply the changes to the db by running the following command:
```
python -m src.manage db upgrade
```
* OR (may need to be inside the venv):
```
flask db upgrade
```

There will be 3 tables, "users", "books", and "authors" created in the MySQL database "library" after the `upgrade`.

# Test using PyTest:

* There are 7 test cases
  - JWT token generation and decoding
  - HomeController
  - FibonacciController
```
pytest -v
```
# Continuous Integration:
* Integrated with CircleCI

# Start the application:
```
python -m src.main
```
## Create User:
* POST http://localhost:8080/users/create
```
{
	"firstname": "First Name",
	"lastname": "LastName",
	"email": "firstname.lastname@email.com",
	"password": "P@$$w0rd"
}
```
## Login:
* POST http://localhost:8080/users/login
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
* POST http://localhost:8080/authors/create
```
{
    "email": "jk@email.com",
    "firstname": "JK",
    "lastname": "Rowing"
}
```
## Create Book:
* POST http://localhost:8080/books/create
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
* visit http://localhost:8080
* visit http://localhost:8080/users/all
* visit http://localhost:8080/authors/all
* visit http://localhost:8080/books/all