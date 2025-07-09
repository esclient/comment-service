from commentservice.grpc import comment_pb2
import grpc
from commentservice.service.create_comment import create_comment as service_create_comment

def CreateComment(request: comment_pb2.CreateCommentRequest, context: grpc.ServicerContext):
    id = service_create_comment(request.mod_id, request.author_id, request.text)
    return comment_pb2.CreateCommentResponse(
        comment_id=id,
    )