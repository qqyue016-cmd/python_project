from langchain_chroma import Chroma
import config_data

class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding = embedding
        self.vectorstores = Chroma(
            collection_name=config_data.collection_name,
            embedding_function=self.embedding,
            persist_directory=config_data.persist_directory
        )

    def get_retriever(self):
        return self.vectorstores.as_retriever(search_kwargs={"k":config_data.search_kwargs})

if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    vector_store_service = VectorStoreService(embedding=DashScopeEmbeddings(model='text-embedding-v4'))
    retriever = vector_store_service.get_retriever()
    res = retriever.invoke('我180cm适合什么尺码')
    print(res)
