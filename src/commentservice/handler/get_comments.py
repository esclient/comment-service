from commentservice.grpc import comment_pb2
import grpc
from commentservice.service.get_comments import get_comments as service_get_comments
from datetime import datetime

def GetComments(request: comment_pb2.GetCommentsRequest, context: grpc.ServicerContext):
    comments = service_get_comments(mod_id=request.mod_id)
    return comment_pb2.GetCommentsResponse(
        mod_id=request.mod_id, 
        comments=convertCommentsToProto(comments)
    )

def convertCommentToProto(comment: tuple):
    comment_proto=comment_pb2.Comment(
        id=comment[0], 
        author_id=comment[1], 
        text=comment[2],
        created_at=int(datetime.timestamp(comment[3])),
    )
 
    if comment[4] is not None:
        comment_proto.edited_at=int(datetime.timestamp(comment[4]))

    return comment_proto

def convertCommentsToProto(comments: tuple):
    return [convertCommentToProto(i) for i in comments]