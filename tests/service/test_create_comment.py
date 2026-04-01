from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.repository import CommentRepository
from commentservice.service.service import CommentService


@pytest.mark.asyncio
async def test_service_create_comment(
    mocker: MockerFixture, faker: Faker
) -> None:
    fake_repo = mocker.Mock(spec=CommentRepository)
    moderation_service = mocker.Mock()
    new_id = faker.random_int(min=1, max=100000)
    fake_repo.create_comment = AsyncMock(return_value=new_id)

    mod_id = faker.random_int(min=1, max=100000)
    author_id = faker.random_int(min=1, max=100000)
    text = faker.sentence()

    service = CommentService(fake_repo, moderation_service)
    result = await service.create_comment(
        mod_id=mod_id, author_id=author_id, text=text
    )

    assert result == new_id
    fake_repo.create_comment.assert_awaited_once_with(mod_id, author_id, text)
    moderation_service.request_moderaiton.assert_called_once_with(new_id, text)
