import asyncio
from datetime import UTC
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.model import Comment
from commentservice.repository.repository import CommentRepository
from commentservice.service.service import CommentService


@pytest.fixture()
def fake() -> Faker:
    f = Faker()
    f.seed_instance(20251019)
    return f


def test_service_get_comments(mocker: MockerFixture, fake: Faker) -> None:
    fake_repo = mocker.Mock(spec=CommentRepository)
    comments = [
        Comment(
            id=fake.random_int(),
            author_id=fake.random_int(),
            text=fake.sentence(),
            created_at=fake.date_time(tzinfo=UTC),
            edited_at=None,
        ),
        Comment(
            id=fake.random_int(),
            author_id=fake.random_int(),
            text=fake.sentence(),
            created_at=fake.date_time(tzinfo=UTC),
            edited_at=None,
        ),
    ]
    fake_repo.get_comments = AsyncMock(return_value=comments)

    mod_id = fake.random_int(min=1, max=100000)
    service = CommentService(fake_repo)
    out = asyncio.run(service.get_comments(mod_id=mod_id))

    assert out == comments
    fake_repo.get_comments.assert_awaited_once_with(mod_id)
