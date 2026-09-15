from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

chat_prompt= ChatPromptTemplate.from_messages(
    [
        ('system','你是一个边塞诗人，可以作诗'),
        MessagesPlaceholder('history'),
        ('human','请再做一首唐诗'),
    ]
)

history_data = [
    ('human', '写一首唐诗'),
    ('ai', '锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦')
]

model = ChatTongyi(model='qwen3-max')
Parser = StrOutputParser()

chain = chat_prompt | model | Parser | model
res = chain.invoke({'history':history_data})

print(res.content)