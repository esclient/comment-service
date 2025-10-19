from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.repository import CommentRepository
from commentservice.service.service import CommentService


@pytest.mark.asyncio
async def test_service_edit_comment(
    mocker: MockerFixture, faker: Faker
) -> None:
    fake_repo = mocker.Mock(spec=CommentRepository)
    fake_repo.edit_comment = AsyncMock(return_value=True)

    comment_id = faker.random_int(min=1, max=100000)
    new_text = faker.sentence()

    service = CommentService(fake_repo)
    result = await service.edit_comment(
        comment_id=comment_id, new_text=new_text
    )

    assert result is True
    fake_repo.edit_comment.assert_awaited_once_with(comment_id, new_text)
