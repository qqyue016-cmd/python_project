from vector_stores import VectorStoreService
from langchain_core.documents import Document
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableLambda ,RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(embedding=DashScopeEmbeddings(model=config.embedding_model))
        self.prompt_temmplate = ChatPromptTemplate.from_messages(
            [
                ('system','以我提供的参考资料为主'
                 '简洁和专业的回答用户问题，参考资料{context}'),
                ('system','用户提供了会话历史如下：'),
                MessagesPlaceholder('chat_history'),
                ('human','{input}')
            ]
        )
        self.chat_model = ChatTongyi(model=config.chat_model, streaming=True)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_func(inputs: list[Document]):
            if not inputs:
                return '无相关资料'

            reference_text = '\n'
            for i in inputs:
                reference_text += f"文本内容：{i.page_content}\n源文件：{i.metadata}\n\n"
            return reference_text

        def format_for_retriever(value:list) -> str:
            return value['input']

        def format_for_prompt_template(value:dict):
            new_value = {}
            new_value['input'] = value['input']['input']
            new_value['chat_history'] = value['input']['chat_history']
            new_value['context'] = value['context']
            return new_value

        chain=({
            'input': RunnablePassthrough(),
            'context': RunnableLambda(format_for_retriever) | retriever | format_func
        } | RunnableLambda(format_for_prompt_template) | self.prompt_temmplate | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(  # 生成带有临时会话记录的增强链
            chain,
            get_history,
            input_messages_key='input',
            history_messages_key='chat_history'
        )

        return conversation_chain

if __name__ == '__main__':
    session_config = {
        "configurable":{
            'session_id':'user_001'
        }
    }
    rag_service = RagService()
    print(rag_service.chain.invoke({"input":"我体重180斤，尺码推荐"}, session_config))
