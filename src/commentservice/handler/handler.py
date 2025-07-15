from commentservice.grpc import comment_pb2_grpc
from commentservice.handler.create_comment import CreateComment
from commentservice.handler.get_comments import GetComments

class CommentHandler(comment_pb2_grpc.CommentServiceServicer):
    CreateComment = staticmethod(CreateComment)
    GetComments = staticmethod(GetComments)