from langchain_community.document_loaders import JoplinLoader, JSONLoader

loder = JSONLoader(
    file_path='./data/stu_json_line.json',
    jq_schema=".name",
    text_content=False,
    json_lines=True
)

document = loder.load()
print(document)