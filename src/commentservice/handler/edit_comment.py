import grpc

from commentservice.grpc import comment_pb2
from commentservice.service.service import CommentService


def EditComment(
    service: CommentService,
    request: comment_pb2.EditCommentRequest,
    _: grpc.ServicerContext,
) -> comment_pb2.EditCommentResponse:
    success = service.edit_comment(request.comment_id, request.text)
    return comment_pb2.EditCommentResponse(success=success)
