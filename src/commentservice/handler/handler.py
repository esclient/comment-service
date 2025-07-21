from commentservice.grpc import comment_pb2_grpc
from commentservice.handler.create_comment import CreateComment
from commentservice.handler.get_comments import GetComments
from commentservice.handler.delete_comment import DeleteComment
from commentservice.handler.edit_comment import EditComment


class CommentHandler(comment_pb2_grpc.CommentServiceServicer):
    CreateComment = staticmethod(CreateComment)
    GetComments = staticmethod(GetComments)
    DeleteComment = staticmethod(DeleteComment)
    EditComment = staticmethod(EditComment)