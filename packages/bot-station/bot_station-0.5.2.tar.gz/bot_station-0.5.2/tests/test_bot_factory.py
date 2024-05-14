from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.bot_factory import BotFactory
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage, LMBotMessage
from bot_station.domain.bot.model.lm_train_data import TrainData


class TestBot(Bot):
    next_answer = ""
    is_closed = False

    def __init__(self):
        self.is_closed = False

    async def train(self, data: TrainData):
        if self.is_closed:
            raise AssertionError("Calling call on closed bot!")

    async def call(self, question: LMUserMessage) -> CallResult:
        if self.is_closed:
            raise AssertionError("Calling call on closed bot!")
        return CallResult(answer=LMBotMessage(text=self.next_answer, chat_id=question.chat_id), relevant_docs=[])

    async def load(self, meta: BotMetaInfo):
        pass

    async def delete(self):
        print("TEST delete()")
        self.is_closed = True

    def set_next_answer(self, answer: str):
        self.next_answer = answer

    async def close(self):
        print("TEST close()")
        self.is_closed = True


class TestBotFactory(BotFactory):
    bot: Bot = TestBot()

    def set_bot(self, bot: Bot):
        self.bot = bot

    async def create(self, meta: BotMetaInfo) -> Bot:
        return self.bot
