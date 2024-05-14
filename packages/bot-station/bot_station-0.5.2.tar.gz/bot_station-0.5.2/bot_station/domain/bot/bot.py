from abc import abstractmethod, ABC

from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage
from bot_station.domain.bot.model.lm_train_data import TrainData


class Bot(ABC):
    meta: BotMetaInfo

    @abstractmethod
    async def load(self, meta: BotMetaInfo):
        pass

    @abstractmethod
    async def train(self, data: TrainData):
        pass

    @abstractmethod
    async def call(self, question: LMUserMessage) -> CallResult:
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def delete(self):
        """
        Удаляет все данные, связанные с ботом
        TODO: должно быть вынесено в рамках выноса Базы Знаний в отдельную сущность
        """
        pass
