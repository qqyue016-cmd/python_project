from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

loder = CSVLoader(
    file_path='./data/stu1.csv',
    encoding='utf-8',
    source_column='source'
)

documents = loder.load()

vector_store=InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)

vector_store.add_documents(
    documents=documents,
    ids=['id'+str(i) for i in range(1,len(documents)+1)]
)

# vector_store.delete(['id1','id2']) 删除数据

res = vector_store.similarity_search(
    'python是不是简单易学',
    2
)

print(res)

