import asyncio
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.repository import CommentRepository
from commentservice.service.service import CommentService


@pytest.fixture()
def fake() -> Faker:
    f = Faker()
    f.seed_instance(20251019)
    return f


def test_service_create_comment(mocker: MockerFixture, fake: Faker) -> None:
    fake_repo = mocker.Mock(spec=CommentRepository)
    new_id = fake.random_int(min=1, max=100000)
    fake_repo.create_comment = AsyncMock(return_value=new_id)

    mod_id = fake.random_int(min=1, max=100000)
    author_id = fake.random_int(min=1, max=100000)
    text = fake.sentence()

    service = CommentService(fake_repo)
    result = asyncio.run(
        service.create_comment(mod_id=mod_id, author_id=author_id, text=text)
    )

    assert result == new_id
    fake_repo.create_comment.assert_awaited_once_with(mod_id, author_id, text)
