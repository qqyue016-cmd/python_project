from vector_stores import VectorStoreService
from langchain_core.documents import Document
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(embedding=DashScopeEmbeddings(model=config.embedding_model))
        self.prompt_temmplate = ChatPromptTemplate.from_messages(
            [
                ('system','以我提供的参考资料为主'
                 '简洁和专业的回答用户问题，参考资料{context}'),
                ('human','{input}')
            ]
        )
        self.chat_model = ChatTongyi(model=config.chat_model)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_func(inputs: list[Document]):
            if not inputs:
                return '无相关资料'

            reference_text = '\n'
            for i in inputs:
                reference_text += f"文本内容：{i.page_content}\n" + "源文件：{i.metadata}\n\n"
            return reference_text

        chain=({
            'input': RunnablePassthrough(),
            'context': retriever | format_func
        } | self.prompt_temmplate | self.chat_model | StrOutputParser()
        )

        return chain

if __name__ == '__main__':
    rag_service = RagService()
    print(rag_service.chain.invoke('我体重180斤，尺码推荐'))
