import asyncio
from unittest.mock import AsyncMock

import grpc
import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.grpc.comment_pb2 import (
    CreateCommentRequest,
    CreateCommentResponse,
)
from commentservice.handler.create_comment import CreateComment
from commentservice.service.service import CommentService


@pytest.fixture()
def fake() -> Faker:
    f = Faker()
    f.seed_instance(20251019)
    return f


def test_create_comment_success(mocker: MockerFixture, fake: Faker) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)
    new_id = fake.random_int(min=1, max=100000)
    fake_service.create_comment = AsyncMock(return_value=new_id)

    mod_id = fake.random_int(min=1, max=100000)
    author_id = fake.random_int(min=1, max=100000)
    text = fake.sentence()
    request = CreateCommentRequest(
        mod_id=mod_id, author_id=author_id, text=text
    )

    response = asyncio.run(CreateComment(fake_service, request, ctx))

    assert isinstance(response, CreateCommentResponse)
    assert response.comment_id == new_id

    fake_service.create_comment.assert_awaited_once_with(
        mod_id, author_id, text
    )
