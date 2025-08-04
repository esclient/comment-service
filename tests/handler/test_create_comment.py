import grpc
from pytest_mock import MockerFixture

from commentservice.grpc.comment_pb2 import (
    CreateCommentRequest,
    CreateCommentResponse,
)
from commentservice.handler.create_comment import CreateComment
from commentservice.service.service import CommentService


def test_create_comment_success(mocker: MockerFixture) -> None:
    ctx = mocker.Mock(spec=grpc.ServicerContext)
    fake_service = mocker.Mock(spec=CommentService)
    fake_service.create_comment.return_value = 42

    request = CreateCommentRequest(
        mod_id=7,
        author_id=13,
        text="Test text",
    )

    response = CreateComment(fake_service, request, ctx)

    assert isinstance(response, CreateCommentResponse)
    assert response.comment_id == 42

    fake_service.create_comment.assert_called_once_with(7, 13, "Test text")
