from langchain_core.prompts import  PromptTemplate
from langchain_community.llms.tongyi import Tongyi


prompt_template=PromptTemplate.from_template(
    '我的邻居姓{lastname}，刚生了{gender}，你帮我起一个名字，简单回答'
)

model = Tongyi(model='qwen-max')
# prompt_text = prompt_template.format(lastname='张',gender='女儿')
#
# model = Tongyi(model='qwen-max')
# res = model.stream(input=prompt_text)
#
# for chunk in res:
#     print(chunk,end='',flush=True)

chain = prompt_template | model

res = chain.invoke(input={'lastname':'张','gender':'女儿'})
print(res)