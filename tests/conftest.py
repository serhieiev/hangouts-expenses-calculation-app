import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.app.models import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # In-memory SQLite database for testing

@pytest.fixture
async def test_db():
    # Create a new engine instance for each test
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    # Create all tables in the test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a new SessionLocal class for each test
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Create a new database session for a test
    async with AsyncSessionLocal() as session:
        yield session  # Use the session in tests

    # Drop all tables after each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def mock_current_user(mocker):
    test_user = User(
        id="c9d3e1d6-fa36-4c7a-b468-dcd4fe677855",
        email="test@example.com",
        password = "P@ssw0rd",
        avatar = "someavatar"
    )

    # Use mocker.patch to mock get_current_user dependency
    mocker.patch("src.app.api.users.get_current_user", return_value=test_user)
