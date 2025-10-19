import textwrap
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.repository import CommentRepository


@pytest.mark.asyncio
async def test_repo_create_comment_returns_id(
    mocker: MockerFixture, faker: Faker
) -> None:
    comment_id = faker.random_int(min=1, max=100000)
    conn = mocker.Mock()
    conn.fetchval = AsyncMock(return_value=comment_id)

    pool = mocker.Mock()
    pool.acquire = mocker.Mock()
    pool.acquire.return_value = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    pool.acquire.return_value.__aexit__.return_value = None

    repo = CommentRepository(pool)
    mod_id = faker.random_int(min=1, max=100000)
    author_id = faker.random_int(min=1, max=100000)
    text = faker.sentence()
    new_id = await repo.create_comment(
        mod_id=mod_id, author_id=author_id, text=text
    )

    assert new_id == comment_id
    assert conn.fetchval.await_count == 1
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
