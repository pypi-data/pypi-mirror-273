from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader


# loader = UnstructuredFileLoader("../document_test/aaa.txt", encodings="utf-8")
# docs = loader.load()
# print(len(docs), docs)
#
# with open("../document_test/doc.json", 'r', encoding='utf-8') as fp:
#     line = fp.read()
#     print(line)

loader = DirectoryLoader('../document_test',
                         glob="**/*",
                         silent_errors=True,
                         )
docs = loader.load()
print(len(docs), len(docs[4].page_content))


