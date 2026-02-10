from typing import Optional

import faker
import pytest


from api.v1.schemas.links import LinkIn

fake = faker.Faker()


@pytest.fixture
def link_in_data():
    source_url = fake.url(schemes=["http"])
    yield {"source_url": source_url}


@pytest.fixture
def mock_link_in(link_in_data):
    def _mock_link_in(data: Optional[dict] = None) -> LinkIn:
        if data is None:
            data = {}
        return LinkIn(**(link_in_data | data))

    return _mock_link_in
