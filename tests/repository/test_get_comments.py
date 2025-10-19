import asyncio
import textwrap
from datetime import UTC
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


def test_repo_get_comments_maps_rows(
    mocker: MockerFixture, fake: Faker
) -> None:
    rows = [
        {
            "id": fake.random_int(),
            "author_id": fake.random_int(),
            "text": fake.sentence(),
            "created_at": fake.date_time(tzinfo=UTC),
            "edited_at": None,
        },
        {
            "id": fake.random_int(),
            "author_id": fake.random_int(),
            "text": fake.sentence(),
            "created_at": fake.date_time(tzinfo=UTC),
            "edited_at": fake.date_time(tzinfo=UTC),
        },
    ]

    conn = mocker.Mock()
    conn.fetch = AsyncMock(return_value=rows)
    acquire_cm = mocker.MagicMock()
    acquire_cm.__aenter__ = AsyncMock(return_value=conn)
    acquire_cm.__aexit__ = AsyncMock(return_value=None)
    pool = mocker.Mock()
    pool.acquire.return_value = acquire_cm
    repo = CommentRepository(pool)  # type: ignore[arg-type]

    out = asyncio.run(repo.get_comments(mod_id=77))

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
    assert (
        textwrap.dedent(actual_sql).strip()
        == textwrap.dedent(expected_sql).strip()
    )
    assert conn.fetch.await_args.args[1:] == (77,)
