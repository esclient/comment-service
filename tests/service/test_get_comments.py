from datetime import UTC
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.model import Comment
from commentservice.repository.repository import CommentRepository
from commentservice.service.service import CommentService


@pytest.mark.asyncio
async def test_service_get_comments(
    mocker: MockerFixture, faker: Faker
) -> None:
    fake_repo = mocker.Mock(spec=CommentRepository)
    comments = [
        Comment(
            id=faker.random_int(),
            author_id=faker.random_int(),
            text=faker.sentence(),
            created_at=faker.date_time(tzinfo=UTC),
            edited_at=None,
        ),
        Comment(
            id=faker.random_int(),
            author_id=faker.random_int(),
            text=faker.sentence(),
            created_at=faker.date_time(tzinfo=UTC),
            edited_at=None,
        ),
    ]
    fake_repo.get_comments = AsyncMock(return_value=comments)

    mod_id = faker.random_int(min=1, max=100000)
    service = CommentService(fake_repo)
    out = await service.get_comments(mod_id=mod_id)

    assert out == comments
    fake_repo.get_comments.assert_awaited_once_with(mod_id)
