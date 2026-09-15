from langchain_community.document_loaders import PyPDFLoader

loder = PyPDFLoader(
    file_path='./data/pdf1.pdf',
    mode='single',
    # password=''有密码输入密码
)

for doc in loder.lazy_load():
    print(doc)