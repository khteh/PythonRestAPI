"""
Tests for the SQLAlchemy async (AsyncSession) data access layer.
They need the PostgreSQL database ("library" with migrations applied). They are skipped if it is not reachable.
"""
import os, uuid, pytest
from http import HTTPStatus
from sqlalchemy import text
os.environ["Testing"] = "True"

@pytest.fixture
async def db(app_context):
    from src.models import async_session
    try:
        async with async_session() as session:
            await session.execute(text("select 1"))
            await session.scalar(text("select count(*) from users"))
    except Exception as e:
        pytest.skip(f"Database not available: {e}")

def _unique(prefix="t"):
    return f"{prefix}-{uuid.uuid4().hex[:10]}"

async def _new_user(password="P@$$w0rd"):
    from src.models.UserModel import UserModel, UserSchema
    email = f"{_unique('user')}@email.com"
    data = UserSchema().load({"firstname": "First", "lastname": "Last", "email": email, "password": password})
    assert isinstance(data, UserModel) # loaded without any database session
    id = await UserModel.add(data)
    return id, email

async def test_user_crud(db):
    from src.models.UserModel import UserModel
    id, email = await _new_user()
    assert id
    assert await UserModel.isExistingUser(email)
    user = await UserModel.get_user_by_email(email)
    assert user.id == id and user.email == email
    assert user.password != "P@$$w0rd" # hashed
    assert user.check_hash("P@$$w0rd")
    assert not user.check_hash("wrong")
    await user.update({"firstname": "Changed"})
    again = await UserModel.get_user(id)
    assert again.firstname == "Changed" and user.firstname == "Changed" # persisted and reflected locally
    assert again.modified_at is not None
    await user.delete()
    assert await UserModel.get_user(id) is None
    assert not await UserModel.isExistingUser(email)

async def test_author_book_relationship_and_eager_loading(db):
    from src.models.AuthorModel import AuthorModel, AuthorSchema
    from src.models.BookModel import BookModel, BookSchema
    email = f"{_unique('author')}@email.com"
    author = AuthorSchema().load({"firstname": _unique("fn"), "lastname": _unique("ln"), "email": email})
    author_id = await AuthorModel.add(author)
    assert not await AuthorModel.isExistingAuthor("nobody@nowhere.com")
    assert await AuthorModel.isExistingAuthor(email)
    isbn = f"{uuid.uuid4().int % 10**13:013d}"
    book = BookSchema().load({"title": "My Book", "isbn": isbn, "page_count": "123", "author_id": author_id})
    book_id = await BookModel.add(book)
    assert await BookModel.isExistingBook(isbn)
    # Relationship must be usable after the session is closed (no lazy loading in async)
    fetched = await AuthorModel.get_author_by_email(email)
    assert [b.id for b in fetched.books] == [book_id]
    assert (await AuthorModel.get_author(author_id)).books[0].isbn == isbn # selectin eager loaded
    dumped = AuthorSchema().dump(fetched)
    assert dumped["email"] == email and len(dumped["books"]) == 1
    assert (await BookModel.get_book_by_isbn(isbn)).id == book_id
    assert [b.id for b in await BookModel.get_books_by_title("My Book") if b.id == book_id] == [book_id]
    assert any(r.isbn == isbn for r in await BookModel.get_books_like("my boo"))
    assert any(a.id == author_id and a.bookcount == 1 for a in await AuthorModel.get_authors())
    assert BookSchema().dump(await BookModel.get_book(book_id))["isbn"] == isbn
    book = await BookModel.get_book(book_id)
    await book.update({"title": "Renamed"})
    assert (await BookModel.get_book(book_id)).title == "Renamed"
    await book.delete()
    assert await BookModel.get_book(book_id) is None
    await (await AuthorModel.get_author(author_id)).delete()
    assert await AuthorModel.get_author(author_id) is None

async def test_login_and_protected_endpoints(db):
    """End to end through the Quart test client: login -> async auth_required decorator -> async DB access"""
    from src.main import app
    from src.models.UserModel import UserModel
    id, email = await _new_user()
    client = app.test_client()
    # Not logged in => redirected to login
    response = await client.get("/authors/all")
    assert response.status_code == HTTPStatus.FOUND and "/auth/login" in response.headers["Location"]
    response = await client.post("/auth/login", form={"username": email, "password": "wrong"})
    response = await client.get("/authors/all")
    assert response.status_code == HTTPStatus.FOUND
    response = await client.post("/auth/login", form={"username": email, "password": "P@$$w0rd"})
    assert response.status_code == HTTPStatus.FOUND, await response.get_data()
    assert (await UserModel.get_user(id)).lastlogin is not None
    response = await client.get("/authors/all")
    assert response.status_code == HTTPStatus.OK, await response.get_data()
    assert isinstance(await response.get_json(), list)
    response = await client.get("/books/all")
    assert response.status_code == HTTPStatus.OK, await response.get_data()
    response = await client.get("/users/all")
    assert response.status_code == HTTPStatus.OK
    assert email in (await response.get_data(as_text=True))
    await (await UserModel.get_user(id)).delete()

async def test_logged_in_pages_use_async_user_lookup(db):
    """Regression: pages that resolve the session user must await UserModel.get_user() (home, fibonacci)"""
    from src.main import app
    from src.models.UserModel import UserModel
    id, email = await _new_user()
    client = app.test_client()
    response = await client.post("/auth/login", form={"username": email, "password": "P@$$w0rd"})
    assert response.status_code == HTTPStatus.FOUND, await response.get_data()
    response = await client.post("/fibonacci/", data="n=10", headers={"content-type": "application/x-www-form-urlencoded"})
    body = await response.get_data(as_text=True)
    assert response.status_code == HTTPStatus.OK, body
    assert "Hello First, fibonacci(10): 55" in body, body # user.firstname resolved, not a coroutine
    response = await client.get("/")
    body = await response.get_data(as_text=True)
    assert response.status_code == HTTPStatus.OK, body
    assert "Hello First! It" in body, body # greeting built from the awaited user
    await (await UserModel.get_user(id)).delete()
