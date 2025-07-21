from commentservice.grpc import comment_pb2
import grpc
from commentservice.service.edit_comment import (
    edit_comment as service_edit_comment,
)


def EditComment(
    request: comment_pb2.EditCommentRequest, context: grpc.ServicerContext
):
    success = service_edit_comment(request.comment_id, request.text)

    return comment_pb2.EditCommentResponse(success=success)
