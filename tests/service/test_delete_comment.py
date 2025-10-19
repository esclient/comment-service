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


def test_service_delete_comment(mocker: MockerFixture, fake: Faker) -> None:
    fake_repo = mocker.Mock(spec=CommentRepository)
    fake_repo.delete_comment = AsyncMock(return_value=True)

    comment_id = fake.random_int(min=1, max=100000)

    service = CommentService(fake_repo)
    result = asyncio.run(service.delete_comment(comment_id=comment_id))

    assert result is True
    fake_repo.delete_comment.assert_awaited_once_with(comment_id)
