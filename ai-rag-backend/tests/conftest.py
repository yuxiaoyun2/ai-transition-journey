import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def test_session_factory(tmp_path):
    db_path = tmp_path / "test.db"

    database_url = f"sqlite:///{db_path}"

    test_engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )

    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestSessionLocal
    finally:
        app.dependency_overrides.pop(
            get_db,
            None,
        )

        test_engine.dispose()
