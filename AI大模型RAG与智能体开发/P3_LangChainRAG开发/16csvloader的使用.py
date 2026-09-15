from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path='./data/stu.csv',
    csv_args={
        'delimiter':',',
        # 'quotecher':'“'  指定带有分隔符文本的引号包围是单引号还是双引号
        # 'fieldnames':['a','b','c','d'] 如果没有表头就可以使用
    },
    encoding='utf-8'
)


for document in loader.lazy_load():
    print(document)