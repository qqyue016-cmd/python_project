from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

loder = CSVLoader(
    file_path='./data/stu1.csv',
    encoding='utf-8',
    source_column='source'
)

documents = loder.load()

vector_store=Chroma(
    collection_name='test',
    embedding_function=DashScopeEmbeddings(),
    persist_directory='./chroma_db'
)

vector_store.add_documents(
    documents=documents,
    ids=['id'+str(i) for i in range(1,len(documents)+1)]
)

# vector_store.delete(['id1','id2']) 删除数据

res = vector_store.similarity_search(
    'python简单易学',
    3,
    filter={'source':'黑马程序员'}
)

print(res)
