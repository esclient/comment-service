from commentservice.grpc import comment_pb2
import grpc
from commentservice.service.delete_comment import delete_comment as service_delete_comment

def DeleteComment(request: comment_pb2.DeleteCommentRequest, context: grpc.ServicerContext ):

    success = service_delete_comment(request.comment_id)

    return comment_pb2.DeleteCommentResponse(success = success)