from unittest.mock import AsyncMock

import grpc
import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.grpc.comment_pb2 import (
    EditCommentRequest,
    EditCommentResponse,
)
from commentservice.handler.edit_comment import EditComment
from commentservice.service.service import CommentService


@pytest.mark.asyncio
async def test_edit_comment_success(
    mocker: MockerFixture, faker: Faker
) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)
    fake_service.edit_comment = AsyncMock(return_value=True)

    comment_id = faker.random_int(min=1, max=100000)
    new_text = faker.sentence()
    request = EditCommentRequest(comment_id=comment_id, text=new_text)
    response = await EditComment(fake_service, request, ctx)

    assert isinstance(response, EditCommentResponse)
    assert response.success is True
    fake_service.edit_comment.assert_awaited_once_with(comment_id, new_text)


@pytest.mark.asyncio
async def test_edit_comment_not_found(
    mocker: MockerFixture, faker: Faker
) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)
    fake_service.edit_comment = AsyncMock(return_value=False)

    comment_id = faker.random_int(min=1, max=100000)
    new_text = faker.sentence()
    request = EditCommentRequest(comment_id=comment_id, text=new_text)
    response = await EditComment(fake_service, request, ctx)

    assert response.success is False
    fake_service.edit_comment.assert_awaited_once_with(comment_id, new_text)
