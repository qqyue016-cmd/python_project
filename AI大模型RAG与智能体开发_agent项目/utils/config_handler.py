'''
配置处理工具
'''

import yaml
from utils.path_tool import get_abs_path

def load_rag_config(config_path: str=get_abs_path('config/rag.yaml'),encoding: str='utf-8'):
    with open(config_path,'r',encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_agent_config(config_path: str=get_abs_path('config/agent.yaml'),encoding: str='utf-8'):
    with open(config_path,'r',encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_chroma_config(config_path: str=get_abs_path('config/chroma.yaml'),encoding: str='utf-8'):
    with open(config_path,'r',encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_prompts_config(config_path: str=get_abs_path('config/prompts.yaml'),encoding: str='utf-8'):
    with open(config_path,'r',encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)


load_rag = load_rag_config()
load_agent = load_agent_config()
load_chroma = load_chroma_config()
load_prompts = load_prompts_config()

if __name__ == '__main__':
    print(load_rag['chat_model_name'])
