from unittest.mock import AsyncMock

import grpc
import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.grpc.comment_pb2 import (
    DeleteCommentRequest,
    DeleteCommentResponse,
)
from commentservice.handler.delete_comment import DeleteComment
from commentservice.service.service import CommentService


@pytest.mark.asyncio
async def test_delete_comment_success(
    mocker: MockerFixture, faker: Faker
) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)
    fake_service.delete_comment = AsyncMock(return_value=True)

    comment_id = faker.random_int(min=1, max=100000)
    request = DeleteCommentRequest(comment_id=comment_id)

    response = await DeleteComment(fake_service, request, ctx)

    assert isinstance(response, DeleteCommentResponse)
    assert response.success is True
    fake_service.delete_comment.assert_awaited_once_with(comment_id)


@pytest.mark.asyncio
async def test_delete_comment_not_found(
    mocker: MockerFixture, faker: Faker
) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)
    fake_service.delete_comment = AsyncMock(return_value=False)

    comment_id = faker.random_int(min=1, max=100000)
    request = DeleteCommentRequest(comment_id=comment_id)
    response = await DeleteComment(fake_service, request, ctx)

    assert response.success is False
    fake_service.delete_comment.assert_awaited_once_with(comment_id)
