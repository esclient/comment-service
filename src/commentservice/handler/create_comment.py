import grpc

from commentservice.grpc import comment_pb2
from commentservice.service.service import CommentService


async def CreateComment(
    service: CommentService,
    request: comment_pb2.CreateCommentRequest,
    _: grpc.ServicerContext,
) -> comment_pb2.CreateCommentResponse:
    id = await service.create_comment(
        request.mod_id, request.author_id, request.text
    )
    return comment_pb2.CreateCommentResponse(
        comment_id=id,
    )
