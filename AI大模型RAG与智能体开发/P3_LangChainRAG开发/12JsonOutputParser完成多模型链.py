from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

Json_Parser = JsonOutputParser()
Str_Parser = StrOutputParser()

model = Tongyi(model='qwen-max')

first_prompt = PromptTemplate.from_template(
    '我的邻居{lastname}，刚刚生了个{gender}，请起名，并封装成JSON格式返回，'
    '返回的key为name，value为名字'
)

second_prompt = PromptTemplate.from_template('请解析{name}这个名字的含义')

chain = first_prompt | model | Json_Parser | second_prompt| model | Str_Parser

res = chain.invoke({'lastname':'陈汉升','gender':'女儿'})
print(res,type(res))