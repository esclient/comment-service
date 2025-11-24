import grpc

from commentservice.constants import STATUS_DELETED, STATUS_HIDDEN, STATUS_ON_MODERATION
from commentservice.grpc import comment_pb2
from commentservice.service.service import CommentService

_ENUM_TO_DB_STATUS_BY_VALUE: dict[int, str] = {
    comment_pb2.CommentStatus.COMMENT_STATUS_DELETED: STATUS_DELETED,
    comment_pb2.CommentStatus.COMMENT_STATUS_HIDDEN: STATUS_HIDDEN,
    comment_pb2.CommentStatus.COMMENT_STATUS_ON_MODERATION: STATUS_ON_MODERATION,
}


def _convert_enum_to_status(status_value: int) -> str:
    if status_value == comment_pb2.CommentStatus.COMMENT_STATUS_UNSPECIFIED:
        raise ValueError("Нужно указать статус")
    return _ENUM_TO_DB_STATUS_BY_VALUE[status_value]


async def SetStatus(
    service: CommentService,
    request: comment_pb2.SetStatusRequest,
    context: grpc.ServicerContext,  # noqa: ARG001
) -> comment_pb2.SetStatusResponse:
    try:
        status_str = _convert_enum_to_status(request.status)
        success = await service.set_status(request.comment_id, status_str)
        return comment_pb2.SetStatusResponse(success=success)
    except Exception as e:
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details(f"Ошибка при указании статуса {e!s}")
        return comment_pb2.SetStatusResponse(success=False)
