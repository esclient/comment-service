from unittest.mock import AsyncMock

import grpc
import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.grpc import comment_pb2
from commentservice.handler.set_status import SetStatus
from commentservice.service.service import CommentService


@pytest.mark.asyncio
async def test_set_status_success(mocker: MockerFixture, faker: Faker) -> None:
    context = mocker.Mock(spec=grpc.ServicerContext)
    service = mocker.Mock(spec=CommentService)
    service.set_status = AsyncMock(return_value=True)

    comment_id = faker.random_int(min=1, max=100000)
    request = comment_pb2.SetStatusRequest(
        comment_id=comment_id,
        status=comment_pb2.CommentStatus.COMMENT_STATUS_DELETED,
    )

    response = await SetStatus(service, request, context)

    assert isinstance(response, comment_pb2.SetStatusResponse)
    assert response.success is True
    service.set_status.assert_awaited_once_with(comment_id, "DELETED")
    context.set_code.assert_not_called()
    context.set_details.assert_not_called()


@pytest.mark.asyncio
async def test_set_status_invalid_enum_sets_error(
    mocker: MockerFixture, faker: Faker
) -> None:
    context = mocker.Mock(spec=grpc.ServicerContext)
    service = mocker.Mock(spec=CommentService)
    service.set_status = AsyncMock()

    request = comment_pb2.SetStatusRequest(
        comment_id=faker.random_int(min=1, max=100000),
        status=comment_pb2.CommentStatus.COMMENT_STATUS_UNSPECIFIED,
    )

    response = await SetStatus(service, request, context)

    assert response.success is False
    service.set_status.assert_not_called()
    context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
    context.set_details.assert_called_once_with("Status must be specified")


@pytest.mark.asyncio
async def test_set_status_internal_error_sets_context(
    mocker: MockerFixture, faker: Faker
) -> None:
    context = mocker.Mock(spec=grpc.ServicerContext)
    service = mocker.Mock(spec=CommentService)
    error = RuntimeError(faker.sentence())
    service.set_status = AsyncMock(side_effect=error)

    request = comment_pb2.SetStatusRequest(
        comment_id=faker.random_int(min=1, max=100000),
        status=comment_pb2.CommentStatus.COMMENT_STATUS_HIDDEN,
    )

    response = await SetStatus(service, request, context)

    assert response.success is False
    context.set_code.assert_called_once_with(grpc.StatusCode.INTERNAL)
    assert (
        context.set_details.call_args.args[0]
        == f"Failed to set status: {error!s}"
    )
