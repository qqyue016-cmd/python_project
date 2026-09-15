from langchain_classic.schema import document
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatTongyi(model='qwen3-max')
prompt = ChatPromptTemplate.from_messages(
    [
        ('system','以我提供的已知参考资料，简洁和专业的回答用户问题，参考资料{context}'),
        ('human','{input}')
    ]
)

vector_store=InMemoryVectorStore(embedding=DashScopeEmbeddings(model='text-embedding-v4'))

vector_store.add_texts(['减肥就是要少吃多练','在减肥期间吃东西很重要，清淡少油控制卡路里摄入并运动起来','跑步是很好的运动哦'])

input_text = '怎么减肥'

retriever = vector_store.as_retriever(search_kwargs={"k":2})

def format_func(result :list[document]):
    if not result:
        return '无相关资料'

    reference_text = '['
    for i in result:
       reference_text += i.page_content + '\n'
    reference_text +=']'
    return reference_text

def print_prompt(o):
    print(o.to_string())
    print('='*20)
    return o



chain = (
    {'input':RunnablePassthrough(),'context': retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
)

res = chain.invoke(input_text)
print(res)