# tests/test_book_model.py
import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.models.book import Book, Base
from core.config import DATABASE_URL

@pytest.fixture(scope="module")
def db_session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_record_and_read_book(db_session):
    #given
    book = Book(
        name="Test Book",
        author="Test Author",
        date_of_release="2023-08-22",
        description="Pytest",
        genre="Genre"
    )
    db_session.add(book)
    db_session.commit()

    # when
    received_book = db_session.query(Book).filter_by(name="Test Book").first()

    #then
    assert received_book is not None
    assert received_book.author == "Test Author"
    assert received_book.name == "Test Book"
    assert received_book.genre == "Genre"
    assert received_book.description == "Pytest"

def test_no_book_available(db_session):
    # Try to read a book that doesn't exist
    received_book = db_session.query(Book).filter_by(name="Nonexistent Book").first()

    assert received_book is None