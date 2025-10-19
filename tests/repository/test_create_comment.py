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


def test_repo_create_comment_returns_id(
    mocker: MockerFixture, fake: Faker
) -> None:
    conn = mocker.Mock()
    conn.fetchval = AsyncMock(return_value=42)

    acquire_cm = mocker.MagicMock()
    acquire_cm.__aenter__ = AsyncMock(return_value=conn)
    acquire_cm.__aexit__ = AsyncMock(return_value=None)

    pool = mocker.Mock()
    pool.acquire.return_value = acquire_cm

    repo = CommentRepository(pool)  # type: ignore[arg-type]
    mod_id = fake.random_int(min=1, max=100000)
    author_id = fake.random_int(min=1, max=100000)
    text = fake.sentence()
    new_id = asyncio.run(
        repo.create_comment(mod_id=mod_id, author_id=author_id, text=text)
    )

    assert new_id == 42
    assert conn.fetchval.await_count == 1
    # check SQL and args
    expected_sql = """
            INSERT INTO comments (mod_id, author_id, text)
            VALUES ($1, $2, $3)
            RETURNING id
            """
    actual_sql = conn.fetchval.await_args.args[0]
    assert (
        textwrap.dedent(actual_sql).strip()
        == textwrap.dedent(expected_sql).strip()
    )
    assert conn.fetchval.await_args.args[1:] == (mod_id, author_id, text)
