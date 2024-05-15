import logging
from pathlib import Path
from typing import Any, Dict, Union

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.schedulers.background import BackgroundScheduler
    from discord import Bot
except ImportError as exc:
    raise ImportError(
        "You need to install libbot[pycord] in order to use this class."
    ) from exc

try:
    from ujson import loads
except ImportError:
    from json import loads

from libbot.i18n import BotLocale
from libbot.i18n.sync import _

logger = logging.getLogger(__name__)


class PycordBot(Bot):
    def __init__(
        self,
        config: Union[Dict[str, Any], None] = None,
        config_path: Union[str, Path] = Path("config.json"),
        locales_root: Union[str, Path, None] = None,
        scheduler: Union[AsyncIOScheduler, BackgroundScheduler, None] = None,
        **kwargs,
    ):
        if config is None:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config: dict = loads(f.read())
        else:
            self.config = config

        super().__init__(
            debug_guilds=self.config["bot"]["debug_guilds"],
            owner_ids=self.config["bot"]["owners"],
            **kwargs,
        )

        self.bot_locale: BotLocale = BotLocale(
            default_locale=self.config["locale"],
            locales_root=(Path("locale") if locales_root is None else locales_root),
        )
        self.default_locale: str = self.bot_locale.default
        self.locales: dict = self.bot_locale.locales

        self._ = self.bot_locale._
        self.in_all_locales = self.bot_locale.in_all_locales
        self.in_every_locale = self.bot_locale.in_every_locale

        self.scheduler: Union[AsyncIOScheduler, BackgroundScheduler, None] = scheduler
