# PythonFlaskRestAPI
Python RestAPI using Flask Framework.

# Database setup:
## Install python modules
```
cd src
pipenv install
cd test
pipenv install
```
## Setup environment:
### Windows
```
set FLASK_ENV=development
set DATABASE_URL=postgres://username:password@host:port/blogsdb
set JWT_SECRET_KEY=yoursecretkey
```
### UNIX
```
export FLASK_ENV=development
eport DATABASE_URL=postgres://username:password@host:port/blogs
export JWT_SECRET_KEY=yoursecretkey
```
## Create Database
`$ createdb blogs`

## Database Migration
```
cd PythonFlaskRestAPI\PythonFlaskRestAPI
```
* run migrations initialization with db init command:
```
python manage.py db init
```
* Populate migrations files and generate users and blogs tables with our model changes:
```
python manage.py db migrate
```
* Apply the changes to the db by running the following command:
```
python manage.py db upgrade
```
# Test using PyTest:

There are 7 test cases
* JWT token generation and decoding
* GreetingsController
* FibonacciController
```
pytest -v
```
# Continuous Integration:
* Integrated with CircleCI

# Start the application:
```
python src/main.py
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
## Get Requests:
* Headers:
```
Key: api-key
Vaue: jwt_token from the login response
```
* visit http://localhost:5555/api/v1/greeting
* visit http://localhost:5555/api/v1/greeting?name=MickeyMouse
* visit http://localhost:5555/api/v1/users
* visit http://localhost:5555/api/v1/blogs
* visit http://localhost:5555/api/v1/fibonacci/?n=10
