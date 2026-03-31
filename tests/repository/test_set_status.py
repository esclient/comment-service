import textwrap

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.set_status import set_status


@pytest.mark.asyncio
async def test_set_status_returns_true_on_update(
    mocker: MockerFixture, faker: Faker
) -> None:
    conn = mocker.Mock()
    conn.execute = mocker.AsyncMock(return_value="UPDATE 1")
    acquire_cm = mocker.AsyncMock()
    acquire_cm.__aenter__.return_value = conn
    acquire_cm.__aexit__.return_value = None
    pool = mocker.Mock()
    pool.acquire.return_value = acquire_cm

    comment_id = faker.random_int(min=1, max=100000)
    status = "DELETED"

    result = await set_status(pool, comment_id, status)

    assert result is True
    expected_sql = """
        UPDATE comments
        SET status = $1
        WHERE id = $2
        """
    actual_sql = conn.execute.await_args.args[0]
    assert (
        textwrap.dedent(actual_sql).strip()
        == textwrap.dedent(expected_sql).strip()
    )
    assert conn.execute.await_args.args[1:] == (status, comment_id)


@pytest.mark.asyncio
async def test_set_status_returns_false_on_exception(
    mocker: MockerFixture, faker: Faker
) -> None:
    pool = mocker.Mock()
    pool.acquire.side_effect = RuntimeError("boom")

    result = await set_status(
        pool, faker.random_int(min=1, max=100000), "HIDDEN"
    )

    assert result is False
