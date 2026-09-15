from utils.path_tool import get_abs_path
from utils.config_handler import load_prompts
from utils.logger_handler import logger

def load_system_prompt():
    try:
        system_prompt = get_abs_path(load_prompts['main_prompt_path'])
    except KeyError as e:
        logger.error(f'[load_system_prompt]配置项中没有main_prompt.txt配置项')
        raise e

    try:
        with open(system_prompt,'r',encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f'[load_system_prompt]解析系统提示词错误，{str(e)}')
        raise e

def load_rag_prompt():
    try:
        rag_prompt = get_abs_path(load_prompts['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f'[load_rag_prompt]配置项中没有rag_summarize_prompt_path配置项')
        raise e

    try:
        with open(rag_prompt,'r',encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f'[load_rag_prompt]解析系统提示词错误，{str(e)}')
        raise e

def load_report_prompt():
    try:
        report_prompt = get_abs_path(load_prompts['report_prompt_path'])
    except KeyError as e:
        logger.error(f'[load_report_prompt]配置项中没有report_prompt.txt配置项')
        raise e

    try:
        with open(report_prompt,'r',encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f'[load_report_prompt]解析系统提示词错误，{str(e)}')
        raise e

if __name__ == '__main__':
    print(load_system_prompt())