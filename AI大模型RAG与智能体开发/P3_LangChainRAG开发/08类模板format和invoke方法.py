from langchain_core.prompts import PromptTemplate

examples = PromptTemplate.from_template('我的邻居是{lastname}')

res = examples.format(lastname = '小林')
print(res,type(res))

res2 = examples.invoke( {'lastname':'小林'})
print(res2,type(res2))