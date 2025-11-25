from datetime import UTC, timedelta

import grpc
import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.grpc.comment_pb2 import (
    GetCommentsRequest,
    GetCommentsResponse,
)
from commentservice.handler.get_comments import GetComments, ts_to_dt
from commentservice.repository.model import Comment
from commentservice.service.service import CommentService


@pytest.mark.asyncio
async def test_get_comments_success(
    mocker: MockerFixture, faker: Faker
) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)

    now = faker.date_time(tzinfo=UTC)
    earlier = now - timedelta(hours=faker.random_int(min=1, max=12))

    comment1 = Comment(
        id=faker.random_int(min=1, max=100000),
        author_id=faker.random_int(min=1, max=100000),
        text=faker.sentence(),
        created_at=earlier,
        edited_at=None,
    )
    comment2 = Comment(
        id=faker.random_int(min=1, max=100000),
        author_id=faker.random_int(min=1, max=100000),
        text=faker.sentence(),
        created_at=now,
        edited_at=now,
    )
    comments = [comment1, comment2]
    fake_service.get_comments.return_value = comments

    mod_id = faker.random_int(min=1, max=100000)
    request = GetCommentsRequest(mod_id=mod_id)
    response = await GetComments(fake_service, request, ctx)

    assert isinstance(response, GetCommentsResponse)
    assert response.mod_id == mod_id
    assert len(response.comments) == 2

    c1 = response.comments[0]
    assert c1.id == comment1.id
    assert c1.author_id == comment1.author_id
    assert c1.text == comment1.text
    assert not c1.HasField("edited_at")
    assert ts_to_dt(c1.created_at, tz=UTC) == earlier

    c2 = response.comments[1]
    assert c2.id == comment2.id
    assert c2.author_id == comment2.author_id
    assert c2.text == comment2.text
    assert c2.HasField("edited_at")
    assert ts_to_dt(c2.created_at, tz=UTC) == now

    fake_service.get_comments.assert_called_once_with(mod_id=mod_id)
