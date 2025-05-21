# Python Quart RestAPI

Python RestAPI using Quart HTTP/3 ASGI framework.

## Environment setup

- On a development host, create a virtual environment for development and test. Both must be using the same virtual environment.
- Virtual environment is optional for CI/CD do because everything runs in a docker container.
- Add the following to `.env` for database access credentials:

```
DB_USERNAME=username
DB_PASSWORD=password
```

### Google Gemini API

- Obtain an API key from https://aistudio.google.com/apikey
- Add a `.env` file with the following content:
  ```
  GEMINI_API_KEY=<api key>
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

- Copy `env.py` to `migrations/` folder.
- Set the values `DB_foo` in `/etc/pythonrestapi_config.json`
- run migrations initialization with db init command:

  ```
  $ pipenv run alembic init migrations
  $ cp env.py migrations
  $ pipenv run alembic revision --autogenerate -m "Initial migration"
  $ pipenv run alembic upgrade head
  ```

- There will be 3 tables, "users", "books", and "authors" created in the PostgreSQL database "library" after the `upgrade`.

## Test using PyTest:

- There are 7 test cases
  - JWT token generation and decoding
  - HomeController
  - FibonacciController
  ```
  $ pipenv run pytest -v
  $ python -m pytest
  ```

## Continuous Integration:

- Integrated with CircleCI

## Start the application:

- `./hypercorn.sh`

## Curl

- Add `Host` header which is defined as `server_names` in `hypercorn.toml`

```
curl --http3-only --insecure -v https://localhost:4433/<path> -H "Host: khteh.com"
```

```
curl --http3-only --insecure -vv https://localhost:4433/chat/invoke -F 'prompt=:"What is task decomposition?"' -F 'file=@/usr/src/Python/PythonRestAPI/data/1.jpg' -F 'receipt=true'
```

## Browser

- Add extensions to add `Host` header based on filter

## Use Cases

### Google Gemini API

- Return text message from input prompt string by calling the API
- Return text message from input prompt string and an image file by calling the API
- Multimodal:
  - Upload an image, "receipt" in this case, and it wil return a structured data containing details in the receipt:
  ```
  2025-05-21 13:15:34 DEBUG    ProcessReceipt response: {
  "date_str": "28-07-2017",
  "vendor": "Walmart",
  "currency": "USD",
  "items": [
    {
      "name": "PET TOY",
      "amount": 1.97
    },
    {
      "name": "FLOPPY PUPPY",
      "amount": 1.97
    },
    {
      "name": "SSSUPREME S",
      "amount": 4.97
    },
    {
      "name": "2.5 SQUEAK",
      "amount": 5.92
    },
    {
      "name": "MUNCHY DMBEL",
      "amount": 3.77
    },
    {
      "name": "DOG TREAT",
      "amount": 2.92
    },
    {
      "name": "PED PCH 1",
      "amount": 0.50
    },
    {
      "name": "PED PCH 1",
      "amount": 0.50
    },
    {
      "name": "COUPON 23100",
      "amount": 1.00
    },
    {
      "name": "HNYMD SMORES",
      "amount": 3.98
    },
    {
      "name": "FRENCH DRSNG",
      "amount": 1.98
    },
    {
      "name": "3 ORANGES",
      "amount": 5.47
    },
    {
      "name": "BABY CARROTS",
      "amount": 1.48
    },
    {
      "name": "COLLARDS",
      "amount": 1.24
    },
    {
      "name": "CALZONE",
      "amount": 2.50
    },
    {
      "name": "MM RVW MNT",
      "amount": 19.77
    },
    {
      "name": "STKOBRLPLABL",
      "amount": 1.97
    },
    {
      "name": "STKOBRLPLABL",
      "amount": 1.97
    },
    {
      "name": "STKO SUNFLWR",
      "amount": 0.97
    },
    {
      "name": "STKO SUNFLWR",
      "amount": 0.97
    },
    {
      "name": "STKO SUNFLWR",
      "amount": 0.97
    },
    {
      "name": "STKO SUNFLWR",
      "amount": 0.97
    },
    {
      "name": "BLING BEADS",
      "amount": 0.97
    },
    {
      "name": "GREAT VALUE",
      "amount": 9.97
    },
    {
      "name": "LIPTON",
      "amount": 4.48
    },
    {
      "name": "DRY DOG",
      "amount": 12.44
    }
  ],
  "tax": 4.59,
  "total": 98.21
  }, receipt: vendor='Walmart' currency='USD' items=[ReceiptItem(name='PET TOY', amount=1.97), ReceiptItem(name='FLOPPY PUPPY', amount=1.97), ReceiptItem(name='SSSUPREME S', amount=4.97), ReceiptItem(name='2.5 SQUEAK', amount=5.92), ReceiptItem(name='MUNCHY DMBEL', amount=3.77), ReceiptItem(name='DOG TREAT', amount=2.92), ReceiptItem(name='PED PCH 1', amount=0.5), ReceiptItem(name='PED PCH 1', amount=0.5), ReceiptItem(name='COUPON 23100', amount=1.0), ReceiptItem(name='HNYMD SMORES', amount=3.98), ReceiptItem(name='FRENCH DRSNG', amount=1.98), ReceiptItem(name='3 ORANGES', amount=5.47), ReceiptItem(name='BABY CARROTS', amount=1.48), ReceiptItem(name='COLLARDS', amount=1.24), ReceiptItem(name='CALZONE', amount=2.5), ReceiptItem(name='MM RVW MNT', amount=19.77), ReceiptItem(name='STKOBRLPLABL', amount=1.97), ReceiptItem(name='STKOBRLPLABL', amount=1.97), ReceiptItem(name='STKO SUNFLWR', amount=0.97), ReceiptItem(name='STKO SUNFLWR', amount=0.97), ReceiptItem(name='STKO SUNFLWR', amount=0.97), ReceiptItem(name='STKO SUNFLWR', amount=0.97), ReceiptItem(name='BLING BEADS', amount=0.97), ReceiptItem(name='GREAT VALUE', amount=9.97), ReceiptItem(name='LIPTON', amount=4.48), ReceiptItem(name='DRY DOG', amount=12.44)] tax=4.59 total=98.21 date_of_receipt=datetime.date(2017, 7, 28)
  ```
  - On the UI:
    ![Process Receipt](./ProcessReceipt.png?raw=true "Process Receipt")

### Create User:

- POST https://localhost:4433/users/create with the following JSON data:
  ```
  {
      "firstname": "First Name",
      "lastname": "LastName",
      "email": "firstname.lastname@email.com",
      "password": "P@$$w0rd"
  }
  ```

### Login:

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

### Subsequent request header:

```
Key: api-key
Vaue: jwt_token from the login response
```

### Create Author:

- POST https://localhost:4433/authors/create with the following JSON data:
  ```
  {
      "email": "jk@email.com",
      "firstname": "JK",
      "lastname": "Rowing"
  }
  ```

### Create Book:

- POST https://localhost:4433/books/create with the following JSON data:
  ```
  {
      "author_id": 1,
      "isbn": "123456",
      "page_count": "123",
      "title": "My First Book"
  }
  ```

### Delete an author:

- Books table has a foreign key id to Authors.id and this is defined as required in BookSchema.
- Therefore, when a DELETE RESTful operation is sent to the application to delete an author which has associated book:

```
mysql.connector.errors.IntegrityError: 1048 (23000): Column 'author_id' cannot be null
```

### Get Requests:

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

### Diagnostics

- HTTP/3 curl:

```
$ docker run --rm ymuski/curl-http3 curl --http3 --verbose https://<nodeport service>:<nodeport>/health/ready
```

- To build your own HTTP/3 curl: https://curl.se/docs/http3.html
