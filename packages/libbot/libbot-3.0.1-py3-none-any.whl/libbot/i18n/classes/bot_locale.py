from os import listdir
from pathlib import Path
from typing import Any, Dict, Union

from libbot import sync


class BotLocale:
    """Small addon that can be used by bot clients' classes in order to minimize I/O"""

    def __init__(
        self,
        default_locale: Union[str, None] = "en",
        locales_root: Union[str, Path] = Path("locale"),
    ) -> None:
        if isinstance(locales_root, str):
            locales_root = Path(locales_root)
        elif not isinstance(locales_root, Path):
            raise TypeError("'locales_root' must be a valid path or path-like object")

        files_locales: list = listdir(locales_root)

        valid_locales: list = [
            ".".join(entry.split(".")[:-1]) for entry in files_locales
        ]

        self.default: str = (
            sync.config_get("locale") if default_locale is None else default_locale
        )
        self.locales: dict = {}

        for lc in valid_locales:
            self.locales[lc] = sync.json_read(Path(f"{locales_root}/{lc}.json"))

    def _(self, key: str, *args: str, locale: Union[str, None] = None) -> Any:
        """Get value of locale string

        ### Args:
            * key (`str`): The last key of the locale's keys path
            * *args (`list`): Path to key like: `dict[args][key]`
            * locale (`Union[str, None]`, *optional*): Locale to looked up in. Defaults to config's `"locale"` value

        ### Returns:
            * `Any`: Value of provided locale key. Is usually `str`, `dict` or `list`
        """

        if locale is None:
            locale = self.default

        try:
            this_dict = self.locales[locale]
        except KeyError:
            try:
                this_dict = self.locales[self.default]
            except KeyError:
                return f'⚠️ Locale in config is invalid: could not get "{key}" in {args} from locale "{locale}"'

        this_key = this_dict
        for dict_key in args:
            this_key = this_key[dict_key]

        try:
            return this_key[key]
        except KeyError:
            return f'⚠️ Locale in config is invalid: could not get "{key}" in {args} from locale "{locale}"'

    def in_all_locales(self, key: str, *args: str) -> list:
        """Get value of the provided key and path in all available locales

        ### Args:
            * key (`str`): The last key of the locale's keys path.
            * *args (`list`): Path to key like: `dict[args][key]`.

        ### Returns:
            * `list`: List of values in all locales
        """

        output = []

        for name, lc in self.locales.items():
            try:
                this_dict = lc
            except KeyError:
                continue

            this_key = this_dict
            for dict_key in args:
                this_key = this_key[dict_key]

            try:
                output.append(this_key[key])
            except KeyError:
                continue

        return output

    def in_every_locale(self, key: str, *args: str) -> Dict[str, Any]:
        """Get value of the provided key and path in every available locale with locale tag

        ### Args:
            * key (`str`): The last key of the locale's keys path.
            * *args (`list`): Path to key like: `dict[args][key]`.

        ### Returns:
            * `Dict[str, Any]`: Locale is a key and it's value from locale file is a value
        """

        output = {}

        for name, lc in self.locales.items():
            try:
                this_dict = lc
            except KeyError:
                continue

            this_key = this_dict
            for dict_key in args:
                this_key = this_key[dict_key]

            try:
                output[name] = this_key[key]
            except KeyError:
                continue

        return output
