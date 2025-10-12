import grpc

from commentservice.grpc import comment_pb2, comment_pb2_grpc
from commentservice.handler.create_comment import (
    CreateComment as _create_comment,
)
from commentservice.handler.delete_comment import (
    DeleteComment as _delete_comment,
)
from commentservice.handler.edit_comment import EditComment as _edit_comment
from commentservice.handler.get_comments import GetComments as _get_comments
from commentservice.service.service import CommentService


class CommentHandler(comment_pb2_grpc.CommentServiceServicer):
    def __init__(self, service: CommentService):
        self._service = service

    async def CreateComment(
        self,
        request: comment_pb2.CreateCommentRequest,
        context: grpc.ServicerContext,
    ) -> comment_pb2.CreateCommentResponse:
        return await _create_comment(self._service, request, context)

    async def EditComment(
        self,
        request: comment_pb2.EditCommentRequest,
        context: grpc.ServicerContext,
    ) -> comment_pb2.EditCommentResponse:
        return await _edit_comment(self._service, request, context)

    async def DeleteComment(
        self,
        request: comment_pb2.DeleteCommentRequest,
        context: grpc.ServicerContext,
    ) -> comment_pb2.DeleteCommentResponse:
        return await _delete_comment(self._service, request, context)

    async def GetComments(
        self,
        request: comment_pb2.GetCommentsRequest,
        context: grpc.ServicerContext,
    ) -> comment_pb2.GetCommentsResponse:
        return await _get_comments(self._service, request, context)
