from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock

import grpc
import pytest
from faker import Faker
from pytest_mock import MockerFixture

import commentservice.handler.handler as handler_module
from commentservice.grpc import comment_pb2
from commentservice.handler.handler import CommentHandler
from commentservice.service.service import CommentService


def _build_create_pair(
    faker: Faker,
) -> tuple[
    comment_pb2.CreateCommentRequest, comment_pb2.CreateCommentResponse
]:
    mod_id = faker.random_int(min=1, max=100000)
    author_id = faker.random_int(min=1, max=100000)
    text = faker.sentence()
    response = comment_pb2.CreateCommentResponse(
        comment_id=faker.random_int(min=1, max=100000)
    )
    request = comment_pb2.CreateCommentRequest(
        mod_id=mod_id,
        author_id=author_id,
        text=text,
    )
    return request, response


def _build_edit_pair(
    faker: Faker,
) -> tuple[comment_pb2.EditCommentRequest, comment_pb2.EditCommentResponse]:
    comment_id = faker.random_int(min=1, max=100000)
    new_text = faker.sentence()
    response = comment_pb2.EditCommentResponse(success=True)
    request = comment_pb2.EditCommentRequest(
        comment_id=comment_id, text=new_text
    )
    return request, response


def _build_delete_pair(
    faker: Faker,
) -> tuple[
    comment_pb2.DeleteCommentRequest, comment_pb2.DeleteCommentResponse
]:
    comment_id = faker.random_int(min=1, max=100000)
    response = comment_pb2.DeleteCommentResponse(success=True)
    request = comment_pb2.DeleteCommentRequest(comment_id=comment_id)
    return request, response


def _build_get_pair(
    faker: Faker,
) -> tuple[comment_pb2.GetCommentsRequest, comment_pb2.GetCommentsResponse]:
    mod_id = faker.random_int(min=1, max=100000)
    response = comment_pb2.GetCommentsResponse(mod_id=mod_id)
    response.comments.add(
        id=faker.random_int(min=1, max=100000),
        author_id=faker.random_int(min=1, max=100000),
        text=faker.sentence(),
    )
    request = comment_pb2.GetCommentsRequest(mod_id=mod_id)
    return request, response


@dataclass(frozen=True)
class HandlerCase:
    method_name: str
    helper_attr: str
    builder: Callable[[Faker], tuple[Any, Any]]


CASES: tuple[HandlerCase, ...] = (
    HandlerCase(
        "CreateComment",
        "_create_comment",
        _build_create_pair,
    ),
    HandlerCase(
        "EditComment",
        "_edit_comment",
        _build_edit_pair,
    ),
    HandlerCase(
        "DeleteComment",
        "_delete_comment",
        _build_delete_pair,
    ),
    HandlerCase(
        "GetComments",
        "_get_comments",
        _build_get_pair,
    ),
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case",
    CASES,
    ids=lambda case: case.method_name,
)
async def test_comment_handler_delegates_to_helper(
    mocker: MockerFixture,
    faker: Faker,
    case: HandlerCase,
) -> None:
    service = mocker.Mock(spec=CommentService)
    handler = CommentHandler(service)
    request, expected_response = case.builder(faker)

    helper = mocker.patch.object(
        handler_module,
        case.helper_attr,
        new=AsyncMock(return_value=expected_response),
    )
    context = mocker.Mock(spec=grpc.ServicerContext)

    method = getattr(handler, case.method_name)
    result = await method(request, context)

    assert result is expected_response
    helper.assert_awaited_once_with(service, request, context)
