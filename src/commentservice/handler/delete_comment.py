import grpc

from commentservice.grpc import comment_pb2
from commentservice.service.service import CommentService


async def DeleteComment(
    service: CommentService,
    request: comment_pb2.DeleteCommentRequest,
    _: grpc.ServicerContext,
) -> comment_pb2.DeleteCommentResponse:
    success = await service.delete_comment(request.comment_id)
    return comment_pb2.DeleteCommentResponse(success=success)
