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
## Create Database
* Firstly, create an empty database "library" in MySQL 8.0

## Database Migration
* run migrations initialization with db init command:
```
python -m src.manage db init
```
* Populate migrations files and generate users and blogs tables with our model changes:
```
python -m src.manage db migrate
```
* Apply the changes to the db by running the following command:
```
python -m src.manage db upgrade
```
There will be 3 tables, "users", "books", and "authors" created in the MySQL database "library" after the `upgrade`.

# Test using PyTest:

* There are 7 test cases
  - JWT token generation and decoding
  - GreetingsController
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
* POST http://localhost:5555/api/v1/users
```
{
	"firstname": "First Name",
	"lastname": "LastName",
	"email": "firstname.lastname@email.com",
	"password": "P@$$w0rd"
}
```
## Login:
* POST http://localhost:5555/api/v1/users/login
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
* POST http://localhost:5555/api/v1/books/author
```
{
    "email": "jk@email.com",
    "firstname": "JK",
    "lastname": "Rowing"
}
```
## Create Book:
* POST http://localhost:5555/api/v1/books/
```
{
    "author_id": 1,
    "isbn": "987654",
    "page_count": "456",
    "title": "My Second Book"
}
```
## Get Requests:
* Headers:
```
Key: api-key
Vaue: jwt_token from the login response
```
* visit http://localhost:5555/api/v1/greeting
* visit http://localhost:5555/api/v1/greeting?name=MickeyMouse
* visit http://localhost:5555/api/v1/users
* visit http://localhost:5555/api/v1/books
* visit http://localhost:5555/api/v1/books/authors
* visit http://localhost:5555/api/v1/fibonacci/?n=10
