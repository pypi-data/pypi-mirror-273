try:
    from ujson import JSONDecodeError, dumps
except ImportError:
    from json import dumps, JSONDecodeError

from pathlib import Path
from typing import Any, Union

import pytest

from libbot import sync


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            "tests/data/test.json",
            {
                "foo": "bar",
                "abcdefg": ["higklmnop", {"lol": {"kek": [1.0000035, 0.2542, 1337]}}],
            },
        ),
        ("tests/data/empty.json", {}),
    ],
)
def test_json_read_valid(path: Union[str, Path], expected: Any):
    assert sync.json_read(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("tests/data/invalid.json", JSONDecodeError),
        ("tests/data/nonexistent.json", FileNotFoundError),
    ],
)
def test_json_read_invalid(path: Union[str, Path], expected: Any):
    with pytest.raises(expected):
        assert sync.json_read(path) == expected


@pytest.mark.parametrize(
    "data, path",
    [
        (
            {
                "foo": "bar",
                "abcdefg": ["higklmnop", {"lol": {"kek": [1.0000035, 0.2542, 1337]}}],
            },
            "tests/data/test.json",
        ),
        ({}, "tests/data/empty.json"),
    ],
)
def test_json_write(data: Any, path: Union[str, Path]):
    sync.json_write(data, path)

    assert Path(path).is_file()
    with open(path, "r", encoding="utf-8") as f:
        assert f.read() == dumps(data, ensure_ascii=False, indent=4)
