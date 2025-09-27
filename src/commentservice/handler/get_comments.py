from datetime import UTC, datetime, timezone

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

from commentservice.grpc import comment_pb2
from commentservice.repository.model import Comment
from commentservice.service.service import CommentService


def dt_to_ts(dt: datetime) -> Timestamp:
    dt = dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt.astimezone(UTC)
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def ts_to_dt(ts: Timestamp, tz: timezone = UTC) -> datetime:
    dt_utc = ts.ToDatetime().replace(tzinfo=UTC)
    return dt_utc.astimezone(tz)


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
    created_at_ts = dt_to_ts(comment.created_at)

    comment_proto = comment_pb2.Comment(
        id=comment.id,
        author_id=comment.author_id,
        text=comment.text,
        created_at=created_at_ts,
    )

    if comment.edited_at is not None:
        edited_at_ts = dt_to_ts(comment.edited_at)
        comment_proto.edited_at.CopyFrom(edited_at_ts)

    return comment_proto


def convertCommentsToProto(
    comments: list[Comment],
) -> list[comment_pb2.Comment]:
    return [convertCommentToProto(i) for i in comments]
