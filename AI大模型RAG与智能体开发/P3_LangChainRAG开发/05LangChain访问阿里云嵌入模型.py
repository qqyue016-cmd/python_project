from langchain_community.embeddings import  DashScopeEmbeddings

model = DashScopeEmbeddings()

print(model.embed_query('我喜欢你'))
print(model.embed_documents(['我喜欢你','我爱你']))