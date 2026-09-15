import os,json
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import  ChatPromptTemplate,MessagesPlaceholder


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id=session_id
        self.storage_path=storage_path

        self.file_path=os.path.join(self.storage_path,self.session_id)

        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)

        new_messages = [message_to_dict(message) for message in all_messages]

        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump(new_messages,f)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path,'r',encoding='utf-8') as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return  []

    def clear(self) -> None:
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump([],f)

str_parser = StrOutputParser()   #将ai返回的ai message转换成string形式再输出

model = ChatTongyi(model='qwen3-max')   #调用聊天模型

prompt1 = ChatPromptTemplate.from_messages(   #创建Chatprompt模板
    [
        ('system','你需要根据会话历史回应用户问题'),
        MessagesPlaceholder('chat_history'),    #使用占位符导入历史会话
        ('human','用户当前输入‘：{input}')
    ]
)

def print_prompt(full_prompt):      #打印每次提问与回答
    print('='*10,full_prompt.to_string(),'='*10)
    return full_prompt

basic_chain = prompt1 | print_prompt | model | str_parser   #基础链


def get_history(session_id):
    return FileChatMessageHistory(session_id,'./chat_history')

conversation_chain = RunnableWithMessageHistory(    #生成带有临时会话记录的增强链
    basic_chain,
    get_history,
    input_messages_key='input',
    history_messages_key='chat_history'
)

if __name__=='__main__':
    session_config={'configurable':{'session_id':'user_001'}}   #配置当前会话id

    res1 = conversation_chain.invoke({'input':'小明有一只猫'},session_config)
    print('第一次提问：',res1)
    res2 = conversation_chain.invoke({'input':'小明有两只狗'},session_config)
    print('第二次提问：',res2)
    res3 = conversation_chain.invoke({'input':'小明一共有多少只宠物'},session_config)
    print('第三次提问：',res3)