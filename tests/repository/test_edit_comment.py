import asyncio
import textwrap
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.repository import CommentRepository


@pytest.fixture()
def fake() -> Faker:
    f = Faker()
    f.seed_instance(20251019)
    return f


def _make_pool(mocker: MockerFixture, conn: object):
    acquire_cm = mocker.MagicMock()
    acquire_cm.__aenter__ = AsyncMock(return_value=conn)
    acquire_cm.__aexit__ = AsyncMock(return_value=None)
    pool = mocker.Mock()
    pool.acquire.return_value = acquire_cm
    return pool


def test_repo_edit_comment_success(mocker: MockerFixture, fake) -> None:
    conn = mocker.Mock()
    conn.fetchval = AsyncMock(return_value=5)
    pool = _make_pool(mocker, conn)
    repo = CommentRepository(pool)  # type: ignore[arg-type]

    cid = fake.random_int(min=1, max=100000)
    new_text = fake.sentence()
    conn.fetchval.return_value = cid
    ok = asyncio.run(repo.edit_comment(comment_id=cid, new_text=new_text))
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


def test_repo_edit_comment_not_found(mocker: MockerFixture, fake) -> None:
    conn = mocker.Mock()
    conn.fetchval = AsyncMock(return_value=None)
    pool = _make_pool(mocker, conn)
    repo = CommentRepository(pool)  # type: ignore[arg-type]

    cid = fake.random_int(min=1, max=100000)
    new_text = fake.sentence()
    ok = asyncio.run(repo.edit_comment(comment_id=cid, new_text=new_text))
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
