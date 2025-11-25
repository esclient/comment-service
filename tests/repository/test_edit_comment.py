import textwrap
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.repository import CommentRepository


@pytest.mark.asyncio
async def test_repo_edit_comment_success(
    mocker: MockerFixture, faker: Faker
) -> None:
    conn = mocker.Mock()
    conn.fetchval = AsyncMock()
    pool = mocker.Mock()
    pool.acquire = mocker.Mock()
    pool.acquire.return_value = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    pool.acquire.return_value.__aexit__.return_value = None
    repo = CommentRepository(pool)

    cid = faker.random_int(min=1, max=100000)
    new_text = faker.sentence()
    conn.fetchval.return_value = cid
    ok = await repo.edit_comment(comment_id=cid, new_text=new_text)
    assert ok is True
    expected_sql = """
            UPDATE comments
            SET text = $1, edited_at = NOW()
            WHERE id = $2
            RETURNING id
            """
    actual_sql = conn.fetchval.await_args.args[0]
    assert (
        textwrap.dedent(actual_sql).strip()
        == textwrap.dedent(expected_sql).strip()
    )
    assert conn.fetchval.await_args.args[1:] == (new_text, cid)


@pytest.mark.asyncio
async def test_repo_edit_comment_not_found(
    mocker: MockerFixture, faker: Faker
) -> None:
    conn = mocker.Mock()
    conn.fetchval = AsyncMock(return_value=None)
    pool = mocker.Mock()
    pool.acquire = mocker.Mock()
    pool.acquire.return_value = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    pool.acquire.return_value.__aexit__.return_value = None
    repo = CommentRepository(pool)

    cid = faker.random_int(min=1, max=100000)
    new_text = faker.sentence()
    ok = await repo.edit_comment(comment_id=cid, new_text=new_text)
    assert ok is False
    expected_sql = """
            UPDATE comments
            SET text = $1, edited_at = NOW()
            WHERE id = $2
            RETURNING id
            """
    actual_sql = conn.fetchval.await_args.args[0]
    assert (
        textwrap.dedent(actual_sql).strip()
        == textwrap.dedent(expected_sql).strip()
    )
    assert conn.fetchval.await_args.args[1:] == (new_text, cid)
