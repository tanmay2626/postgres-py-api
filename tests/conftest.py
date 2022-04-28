from app.database import connection
import pytest
from app.models import Base
import os


@pytest.fixture
def setup():
    connection.init()

    yield

    for table in reversed(Base.metadata.sorted_tables):
        connection.session.execute(table.delete())
        connection.session.commit()
