import logging

from bot_station.data.bot.bot_impl import BotImpl
from bot_station.data.bot.chat_message_storage_impl import ChatMessageStorageImpl
from bot_station.data.bot.model.qdrant_config import QdrantConfig
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.domain.base.const import message_history_path
from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.bot_factory import BotFactory
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo


class BotFactoryImpl(BotFactory):
    yandex_cloud_config: YandexCloudConfig
    qdrant_config: QdrantConfig

    def __init__(
            self,
            yandex_cloud_config: YandexCloudConfig,
            qdrant_config: QdrantConfig,
    ):
        self.yandex_cloud_config = yandex_cloud_config
        self.qdrant_config = qdrant_config

    async def create(self, meta: BotMetaInfo) -> Bot:
        logging.debug(f"create new bot {meta}")
        bot = BotImpl(
            message_storage=ChatMessageStorageImpl(
                root_message_history_path=message_history_path
            ),
            yandex_cloud_config=self.yandex_cloud_config,
            qdrant_config=self.qdrant_config,
        )
        await bot.load(meta=meta)
        return bot
