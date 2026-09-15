import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_handler import load_chroma
from utils.file_handler import text_loader, listdir_with_allowed_type, get_file_md5_hex ,pdf_loader
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from model import factory



class VectorStoreService:
    def __init__(self):
        self.chroma = Chroma(
            collection_name=load_chroma['collection_name'],
            persist_directory=get_abs_path(load_chroma['persist_directory']),
            embedding_function=factory.embed_model
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=load_chroma['chunk_size'],
            chunk_overlap=load_chroma['chunk_overlap'],
            separators=load_chroma['separator'],
            length_function=len
        )

    def get_retriever(self):
        return self.chroma.as_retriever(search_kwargs={"k": load_chroma['k']})

    def load_document(self):
        '''
        从数据文件夹内读取文件，转为向量存入向量库
        要计算文件MD5去重
        :return:
        '''
        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(load_chroma['md5_hex_store']):
                open(get_abs_path(load_chroma['md5_hex_store']), 'w',encoding='utf-8').close()
                return False
            with open(get_abs_path(load_chroma['md5_hex_store']), 'r',encoding='utf-8') as f:
                for line in f.readlines():
                    if line.strip() == md5_for_check:
                        return True
            return False

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(load_chroma['md5_hex_store']),'a',encoding='utf-8') as f:
                f.write(md5_for_check + '\n')

        def get_file_document(read_path: str):
            if read_path.endswith('txt'):
                return text_loader(read_path)

            if read_path.endswith('pdf'):
                return pdf_loader(read_path)

            return []

        allowed_file_path: list[str] = listdir_with_allowed_type(
            get_abs_path(load_chroma['data_path']),
            tuple(load_chroma['allow_knowledge_file_type'])
        )
        for path in allowed_file_path:
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f'[加载向量库]{path}文件已加载过，跳过')
                continue

            try:
                documents: list[Document] = get_file_document(path)

                if not documents:
                    logger.error(f'[加载向量库]{path}文件内容为空')
                    continue

                split_documents: list[Document] = self.splitter.split_documents(documents)

                if not split_documents:
                    logger.error(f'[加载向量库]{path}文件分片后内容为空')
                    continue

                self.chroma.add_documents(split_documents)
                save_md5_hex(md5_hex)
                logger.info(f'[加载向量库]{path}文件加载成功')

            except Exception as e:
                logger.error(f'[加载向量库]{path}文件加载向量库失败：{str(e)}',exc_info=True)
                continue

if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke('迷路')
    for r in res:
        print(r.page_content)
        print('*'*20)
