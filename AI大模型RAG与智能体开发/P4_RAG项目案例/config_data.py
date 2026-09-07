md5_text = './md5_path'

# Chroma
collection_name = 'rag'
persist_directory = './chroma.db'

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ['\n\n','\n','.','！','?','。','！','？',' ']
max_split_char_number = 1000

# search kwargs
search_kwargs = 2

# model
embedding_model = 'text-embedding-v4'
chat_model  = 'qwen3-max'