from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.llms.tongyi import Tongyi
from langchain_core.output_parsers import StrOutputParser

Str_Parser = StrOutputParser()

first_prompt = PromptTemplate.from_template(
    '我的邻居{lastname}，刚生了个{gender}，请起个名字，只输出名字，不要输出额外内容'
)

model = Tongyi(model='qwen-max')

second_prompt = PromptTemplate.from_template(
    '请解释这个名字{name}的含义'
)

my_func = RunnableLambda(lambda ai_msq:{'name':ai_msq})

chain = first_prompt | model | my_func | second_prompt | model | Str_Parser
for chunk in chain.stream({'lastname':'陈汉升','gender':'女儿'}):
    print(chunk,end='',flush=True)