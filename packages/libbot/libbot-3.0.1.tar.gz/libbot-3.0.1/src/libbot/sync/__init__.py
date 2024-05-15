from pathlib import Path
from typing import Any, Union

try:
    from ujson import dumps, loads
except ImportError:
    from json import dumps, loads


def json_read(path: Union[str, Path]) -> Any:
    """Read contents of a JSON file

    ### Args:
        * path (`Union[str, Path]`): Path-like object or path as a string

    ### Returns:
        * `Any`: File contents
    """
    with open(str(path), mode="r", encoding="utf-8") as f:
        data = f.read()
    return loads(data)


def json_write(data: Any, path: Union[str, Path]) -> None:
    """Write contents to a JSON file

    ### Args:
        * data (`Any`): Contents to write. Must be a JSON serializable
        * path (`Union[str, Path]`): Path-like object or path as a string of a destination
    """
    with open(str(path), mode="w", encoding="utf-8") as f:
        f.write(
            dumps(data, ensure_ascii=False, escape_forward_slashes=False, indent=4)
            if hasattr(dumps, "escape_forward_slashes")
            else dumps(data, ensure_ascii=False, indent=4)
        )


def nested_set(target: dict, value: Any, *path: str, create_missing=True) -> dict:
    """Set the key by its path to the value

    ### Args:
        * target (`dict`): Dictionary to perform modifications on
        * value (`Any`): Any data
        * *path (`str`): Path to the key of the target
        * create_missing (`bool`, *optional*): Create keys on the way if they're missing. Defaults to `True`

    ### Returns:
        * `dict`: Changed dictionary
    """
    d = target
    for key in path[:-1]:
        if key in d:
            d = d[key]
        elif create_missing:
            d = d.setdefault(key, {})
        else:
            raise KeyError(
                f"Key '{key}' is not found under path provided ({path}) and create_missing is False"
            )
    if path[-1] in d or create_missing:
        d[path[-1]] = value
    return target


def config_get(
    key: str, *path: str, config_file: Union[str, Path] = "config.json"
) -> Any:
    """Get a value of the config key by its path provided
    For example, `foo.bar.key` has a path of `"foo", "bar"` and the key `"key"`

    ### Args:
        * key (`str`): Key that contains the value
        * *path (`str`): Path to the key that contains the value
        * config_file (`Union[str, Path]`, *optional*): Path-like object or path as a string of a location of the config file. Defaults to `"config.json"`

    ### Returns:
        * `Any`: Key's value

    ### Example:
    Get the "salary" of "Pete" from this JSON structure:
    ```json
    {
        "users": {
            "Pete": {
                "salary": 10.0
            }
        }
    }
    ```

    This can be easily done with the following code:
    ```python
    import libbot
    salary = libbot.sync.config_get("salary", "users", "Pete")
    ```
    """
    this_key = json_read(config_file)
    for dict_key in path:
        this_key = this_key[dict_key]
    return this_key[key]


def config_set(
    key: str, value: Any, *path: str, config_file: Union[str, Path] = "config.json"
) -> None:
    """Set config's key by its path to the value

    ### Args:
        * key (`str`): Key that leads to the value
        * value (`Any`): Any JSON serializable data
        * *path (`str`): Path to the key of the target
        * config_file (`Union[str, Path]`, *optional*): Path-like object or path as a string of a location of the config file. Defaults to `"config.json"`
    """
    json_write(nested_set(json_read(config_file), value, *(*path, key)), config_file)
    return
