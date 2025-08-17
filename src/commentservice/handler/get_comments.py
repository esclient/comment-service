from datetime import datetime

import grpc

from commentservice.grpc import comment_pb2
from commentservice.repository.model import Comment
from commentservice.service.service import CommentService


def GetComments(
    service: CommentService,
    request: comment_pb2.GetCommentsRequest,
    _: grpc.ServicerContext,
) -> comment_pb2.GetCommentsResponse:
    comments = service.get_comments(mod_id=request.mod_id)
    return comment_pb2.GetCommentsResponse(
        mod_id=request.mod_id, comments=convertCommentsToProto(comments)
    )


def convertCommentToProto(comment: Comment) -> comment_pb2.Comment:
    comment_proto = comment_pb2.Comment(
        id=comment.id,
        author_id=comment.author_id,
        text=comment.text,
        created_at=int(datetime.timestamp(comment.created_at)),
    )

    if comment.edited_at is not None:
        comment_proto.edited_at = int(datetime.timestamp(comment.edited_at))

    return comment_proto


def convertCommentsToProto(
    comments: list[Comment],
) -> list[comment_pb2.Comment]:
    return [convertCommentToProto(i) for i in comments]
