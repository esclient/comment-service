import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from commentservice.handler.handler import CommentHandler
from commentservice.grpc import comment_pb2_grpc
from commentservice.grpc import comment_pb2
from commentservice.settings import settings

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    comment_pb2_grpc.add_CommentServiceServicer_to_server(
        CommentHandler(), server
    )

    SERVICE_NAMES = (
        comment_pb2.DESCRIPTOR.services_by_name["CommentService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f"{settings.host}:{settings.port}")
    server.start()
    print(f"gRPC server listening on {settings.host}:{settings.port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
