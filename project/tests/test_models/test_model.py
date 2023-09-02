import pytest
from sqlalchemy import delete, select
from core.db import session, set_session_context, reset_session_context

from domain.models import User

@pytest.fixture
async def database_setup():
    async with session() as db:
        # Create database tables
        async with db.begin():
            await db.run_sync(User.metadata.create_all)

        yield

        # Clean up database after tests
        async with db.begin():
            await db.execute(delete(User))

@pytest.mark.asyncio
async def test_user():
    set_session_context("test_session")

    async with session() as db:
        new_user_data = {
            "name": "Charlie",
            "lastname": "Brown",
            "password": "password",
            "email": "charlie@example.com"
        }
        async with db.begin():
            await db.execute(User.__table__.insert().values(new_user_data))

        # Check if the user was added to the database
        user = await db.execute(select(User).filter_by(email="charlie@example.com"))
        assert user.scalar() is not None
