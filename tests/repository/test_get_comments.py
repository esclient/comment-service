import textwrap
from datetime import UTC
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from commentservice.repository.repository import CommentRepository


@pytest.mark.asyncio
async def test_repo_get_comments_maps_rows(mocker: MockerFixture, faker: Faker) -> None:
    rows = [
        {
            "id": faker.random_int(),
            "author_id": faker.random_int(),
            "text": faker.sentence(),
            "created_at": faker.date_time(tzinfo=UTC),
            "edited_at": None,
        },
        {
            "id": faker.random_int(),
            "author_id": faker.random_int(),
            "text": faker.sentence(),
            "created_at": faker.date_time(tzinfo=UTC),
            "edited_at": faker.date_time(tzinfo=UTC),
        },
    ]

    conn = mocker.Mock()
    conn.fetch = AsyncMock(return_value=rows)
    pool = mocker.Mock()
    pool.acquire = mocker.Mock()
    pool.acquire.return_value = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    pool.acquire.return_value.__aexit__.return_value = None
    repo = CommentRepository(pool)

    mod_id = faker.random_int(min=1, max=100000)

    out = await repo.get_comments(mod_id=mod_id)

    assert len(out) == 2
    assert out[0].id == rows[0]["id"] and out[0].text == rows[0]["text"]
    assert out[0].edited_at is None
    assert out[1].id == rows[1]["id"] and out[1].text == rows[1]["text"]
    assert out[1].edited_at is not None
    expected_sql = """
            SELECT id, author_id, text, created_at, edited_at
            FROM comments
            WHERE mod_id = $1
            """
    actual_sql = conn.fetch.await_args.args[0]
    assert textwrap.dedent(actual_sql).strip() == textwrap.dedent(expected_sql).strip()
    assert conn.fetch.await_args.args[1:] == (mod_id,)
