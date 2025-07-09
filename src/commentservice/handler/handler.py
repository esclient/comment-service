from commentservice.grpc import comment_pb2_grpc
from commentservice.handler.create_comment import CreateComment

class CommentHandler(comment_pb2_grpc.CommentServiceServicer):
    CreateComment = staticmethod(CreateComment)