from  langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi

exmaple_template = PromptTemplate.from_template('单词:{word},反义词:{antonym}')

emxple_data = [
    {'word':'大',"antonym":"小"},
    {'word':'上',"antonym":"下"}
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=exmaple_template,
    examples=emxple_data,
    prefix='告诉我单词的反义词，我提供了示例',
    suffix='基于前面的示例，告诉我{input_word}的反义词是：',
    input_variables=['input_word']
)

prompt_text=few_shot_template.invoke(input={'input_word':'左'}).to_string()
model = Tongyi(model='qwen-max')

print(model.invoke(input=prompt_text))