import logging
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection
from psycopg2.pool import ThreadedConnectionPool

from commentservice.grpc import comment_pb2_grpc, comment_pb2
from commentservice.handler.handler import CommentHandler
from commentservice.repository.repository import CommentRepository
from commentservice.service.service import CommentService
from commentservice.settings import Settings


def serve() -> None:
    settings = Settings()
    settings.configure_logging()
    logger = logging.getLogger(__name__)

    db_pool = ThreadedConnectionPool(
        minconn=1, maxconn=10, dsn=settings.database_url
    )

    repo = CommentRepository(db_pool)
    service = CommentService(repo)
    handler = CommentHandler(service)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    comment_pb2_grpc.add_CommentServiceServicer_to_server(
        handler, server
    )  # type: ignore[no-untyped-call]

    SERVICE_NAMES = (
        comment_pb2.DESCRIPTOR.services_by_name["CommentService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f"{settings.host}:{settings.port}")
    server.start()
    logger.info(f"gRPC server listening on {settings.host}:{settings.port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
