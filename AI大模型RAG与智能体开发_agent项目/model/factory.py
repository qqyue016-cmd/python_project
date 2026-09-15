from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import ChatTongyi,BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from utils.config_handler import load_rag

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[BaseChatModel | Embeddings]:
        pass

class chatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel | Embeddings]:
        return ChatTongyi(model=load_rag['chat_model_name'])

class embeddinglFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel | Embeddings]:
        return DashScopeEmbeddings(model=load_rag['embedding_model_name'])

chat_model = chatModelFactory().generator()
embed_model = embeddinglFactory().generator()
