from pathlib import Path
from typing import Any, List

import pytest

from libbot import sync


@pytest.mark.parametrize(
    "args, expected",
    [
        (["locale"], "en"),
        (["bot_token", "bot"], "sample_token"),
    ],
)
def test_config_get_valid(args: List[str], expected: str, location_config: Path):
    assert sync.config_get(args[0], *args[1:], config_file=location_config) == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        (["bot_stonks", "bot"], pytest.raises(KeyError)),
    ],
)
def test_config_get_invalid(args: List[str], expected: Any, location_config: Path):
    with expected:
        assert (
            sync.config_get(args[0], *args[1:], config_file=location_config) == expected
        )


@pytest.mark.parametrize(
    "key, path, value",
    [
        ("locale", [], "en"),
        ("bot_token", ["bot"], "sample_token"),
    ],
)
def test_config_set(key: str, path: List[str], value: Any, location_config: Path):
    sync.config_set(key, value, *path, config_file=location_config)
    assert sync.config_get(key, *path, config_file=location_config) == value
