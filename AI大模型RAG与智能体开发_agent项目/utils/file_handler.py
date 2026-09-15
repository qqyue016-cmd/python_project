'''
文件处理工具
'''

import os
import hashlib
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_md5_hex(filepath):
    if not os.path.exists(filepath): # 判断文件是否存在
        logger.error(f'[md5计算]文件{filepath}不存在')
        return

    if not os.path.isfile(filepath): # 判断是否是文件
        logger.error(f'[md5计算]{filepath}不是文件')
        return

    md5_obj = hashlib.md5() # 创建md5对象
    chunk_size = 4096 # 每次读取的字节数

    try:
        with open(filepath,'rb') as f: # 用循环读取文件并计算md5，必须二进制读取
            while chunk :=f.read(chunk_size):
                md5_obj.update(chunk)
            md5_obj_hex = md5_obj.hexdigest()
            return md5_obj_hex
    except Exception as e:
        logger.error(f'计算文件{filepath}md5失败，{str(e)}')
        return None

def listdir_with_allowed_type(path,allowed_type: tuple[str]):
    if not os.path.isdir(path):
        logger.error(f'[listdir_with_allowed_type]{path}不是文件夹')
        return []

    files = []
    for i in os.listdir(path):
        if i.endswith(allowed_type):
            files.append(os.path.join(path,i))
    return tuple(files)

def pdf_loader(filepath: str) -> list[Document]:
    return PyPDFLoader(filepath).load() # 返回文档列表

def text_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath,encoding='utf-8').load() # 返回文档列表
