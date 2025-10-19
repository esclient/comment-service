import asyncio
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


@pytest.fixture()
def fake() -> Faker:
    f = Faker()
    f.seed_instance(20251019)
    return f


def test_edit_comment_success(mocker: MockerFixture, fake: Faker) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)
    fake_service.edit_comment = AsyncMock(return_value=True)

    comment_id = fake.random_int(min=1, max=100000)
    new_text = fake.sentence()
    request = EditCommentRequest(comment_id=comment_id, text=new_text)
    response = asyncio.run(EditComment(fake_service, request, ctx))

    assert isinstance(response, EditCommentResponse)
    assert response.success is True
    fake_service.edit_comment.assert_awaited_once_with(comment_id, new_text)


def test_edit_comment_not_found(mocker: MockerFixture, fake: Faker) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)
    fake_service.edit_comment = AsyncMock(return_value=False)

    comment_id = fake.random_int(min=1, max=100000)
    new_text = fake.sentence()
    request = EditCommentRequest(comment_id=comment_id, text=new_text)
    response = asyncio.run(EditComment(fake_service, request, ctx))

    assert response.success is False
    fake_service.edit_comment.assert_awaited_once_with(comment_id, new_text)
