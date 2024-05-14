import logging
from typing import List

import langchain
from langchain_community.chat_models import ChatYandexGPT
from langchain_community.document_transformers import LongContextReorder
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document as LangchainDocument
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever
from qdrant_client import QdrantClient

from bot_station.data.bot.mapper.document_mapper import DocumentMapper
from bot_station.data.bot.model.qdrant_config import QdrantConfig
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.domain.base.const import embeddings_cache_dir
from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.chat_message_storage import ChatMessageStorage
from bot_station.domain.bot.model.document import Document
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMBotMessage, LmChatMessage
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage
from bot_station.domain.bot.model.lm_train_data import (
    TrainData,
    DocumentsTrainData,
    QnATrainData,
)


class BotImpl(Bot):
    """
    Реализации LLM бота с памятью на основе YandexGPT и Qdrant
    TODO: перенести prompt и настройки LLM в конфиг или наверх
    """

    yandex_cloud_config_path: str = None
    embeddings: Embeddings = None

    knowledge_vector_store: Qdrant = None
    qdrant_cli: QdrantClient = None
    knowledge_retriever: VectorStoreRetriever = None

    gpt: BaseChatModel = None
    yandex_cloud_config: YandexCloudConfig = None
    qdrant_config: QdrantConfig = None

    message_storage: ChatMessageStorage = None

    meta: BotMetaInfo = None

    __is_loaded: bool = False

    save_doc_max_per_second_count = 10
    doc_splitter_chunk_size = 2000
    doc_splitter_chunk_overlap = 30

    def __init__(
            self,
            message_storage: ChatMessageStorage,
            yandex_cloud_config: YandexCloudConfig,
            qdrant_config: QdrantConfig,
    ):
        self.message_storage = message_storage
        self.yandex_cloud_config = yandex_cloud_config
        self.qdrant_config = qdrant_config

    async def load(self, meta: BotMetaInfo):
        if self.__is_loaded:
            return
        logging.debug(f"load(meta = {meta})")

        langchain.debug = True

        self.embeddings: Embeddings = FastEmbedEmbeddings(cache_dir=embeddings_cache_dir)
        self.gpt = ChatYandexGPT(
            api_key=self.yandex_cloud_config.api_key,
            folder_id=self.yandex_cloud_config.folder_id,
            temperature=meta.temperature,
            model_name=self.yandex_cloud_config.model_name,
            verbose=True,
        )
        self.meta = meta

        if self.qdrant_config.qdrant_url is not None:
            self.qdrant_cli = QdrantClient(url=self.qdrant_config.qdrant_url)
        elif self.qdrant_config.qdrant_db_path is not None:
            self.qdrant_cli = QdrantClient(path=self.qdrant_config.qdrant_db_path)
        else:
            raise AssertionError("qdrant_uri or qdrant_db_path not set")

        self._prepare_vectorstore()
        self.__is_loaded = True

    async def train(self, data: TrainData):
        logging.debug(f"train({data})")
        if isinstance(data, DocumentsTrainData):
            await self._train_by_docs(data)
        if isinstance(data, QnATrainData):
            await self._train_by_q_n_a(data)

    async def call(self, question: LMUserMessage) -> CallResult:
        logging.debug(f"answer_question({question})")

        prompt_with_question = self.meta.prompt_intro + "\n"

        # 1. Add previous messages to prompt
        if self.meta.add_messages_history_to_prompt:
            message_history: List[LmChatMessage] = (
                await self.message_storage.get_history(
                    chat_id=question.chat_id, limit=10
                )
            )
            if len(message_history) > 2:
                prompt_with_question = (
                        prompt_with_question + "\n\nПереписка с пользователем:" + "\n"
                )
                for m in message_history:
                    prompt_with_question = prompt_with_question + "- " + m.text + "\n"

        # 2. Add context to prompt
        relevant_docs: List[LangchainDocument] = []
        if self.meta.add_external_context_to_prompt:
            relevant_docs = self.knowledge_retriever.get_relevant_documents(
                query=question.text
            )
            if len(relevant_docs) > 0:
                reordered_documents: List[LangchainDocument] = list(
                    LongContextReorder().transform_documents(relevant_docs)
                )
                prompt_with_question = (
                        prompt_with_question
                        + "\n\nДля ответа используй только следующие знания:\n"
                )
                for d in reordered_documents:
                    prompt_with_question = prompt_with_question + d.page_content + "\n"

        prompt_with_question = (
                prompt_with_question + "\n\n Сообщение пользователя: " + question.text
        )

        logging.debug(f"Running LLM Chain")

        response = self.gpt.invoke(prompt_with_question).content
        logging.debug(f"response = {response}")
        answer = LMBotMessage(text=response, chat_id=question.chat_id)
        await self.message_storage.add_user_message(
            chat_id=question.chat_id, message=question
        )
        await self.message_storage.add_bot_message(
            chat_id=question.chat_id, message=answer
        )
        relevant_docs: List[Document] = [
            DocumentMapper.from_langchain_document(d) for d in relevant_docs
        ]
        return CallResult(answer=answer, relevant_docs=relevant_docs)

    async def close(self):
        try:
            self.qdrant_cli.close()
        except Exception as e:
            logging.error(e)

    async def delete(self):
        try:
            await self.close()
            self.qdrant_cli.delete_collection(collection_name=self.meta.id)
        except Exception as e:
            logging.error(e)

    async def _train_by_docs(self, data: DocumentsTrainData):
        logging.debug(f"_train_by_docs data={data}")
        documents: List[LangchainDocument] = [
            DocumentMapper.to_langchain_document(d) for d in data.docs
        ]
        await self.knowledge_vector_store.aadd_documents(documents=documents)

    async def _train_by_q_n_a(self, data: QnATrainData):
        logging.debug(f"_train_by_q_n_a data={data}")
        text = data.question + "\n" + data.answer
        await self.knowledge_vector_store.aadd_texts(texts=[text])

    def _prepare_vectorstore(self):
        logging.debug(f"_prepare_vectorstore()")
        self.knowledge_vector_store = Qdrant(
            client=self.qdrant_cli,
            collection_name=self.meta.id,
            embeddings=self.embeddings,
            vector_name=self.qdrant_cli.get_vector_field_name(),
        )
        self.__ensure_quadrant_collection_created()
        self.knowledge_retriever = self.knowledge_vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.7, "k": 3},
        )

    def __ensure_quadrant_collection_created(self):
        try:
            self.qdrant_cli.get_collection(collection_name=self.meta.id)
        except Exception:
            self.qdrant_cli.create_collection(
                collection_name=self.meta.id,
                vectors_config=self.qdrant_cli.get_fastembed_vector_params(),
            )
