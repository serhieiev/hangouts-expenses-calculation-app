import pytest
import asyncio
from async_asgi_testclient import TestClient
from src.main import app
from src.database import engine, Base, AsyncSessionLocal


@pytest.fixture(scope="session", autouse=True)
def set_event_loop():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    yield
    asyncio.set_event_loop(None)


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
async def test_db():
    # Create the test database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # this is where the testing happens

    # Drop the test database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(test_db):  # Added test_db as a dependency
    # Start a new database session and begin a transaction
    session = AsyncSessionLocal()
    await session.begin()

    yield session  # this is where the test will use the session

    # Rollback the transaction and close the session
    await session.rollback()
    await session.close()
