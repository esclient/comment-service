from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.repository import CommentRepository
from commentservice.service.service import CommentService


@pytest.mark.asyncio
async def test_service_set_status_uses_helper(mocker: MockerFixture, faker: Faker) -> None:
    repo = mocker.Mock(spec=CommentRepository)
    helper = AsyncMock(return_value=True)
    mocker.patch("commentservice.service.service._set_status", helper)

    service = CommentService(repo)

    comment_id = faker.random_int(min=1, max=100000)
    status = "DELETED"

    result = await service.set_status(comment_id, status)

    assert result is True
    helper.assert_awaited_once_with(repo, comment_id, status)
