# main.py
from dotenv import load_dotenv
from pylmkit import BaseWebUI
from pylmkit.llms import ChatQianfan
from pylmkit.llms import EmbeddingsHuggingFace
from langchain.vectorstores import FAISS
from pylmkit.perception.text import DocumentLoader
from pylmkit.perception.text import WebLoader
from pylmkit.app import DocRAG


load_dotenv()
web = BaseWebUI(language='zh')

# load: documents
# loader = DocumentLoader(path='./document_test/aaa.txt')  # 加载一个文档
# loader = DocumentLoader(path='./document_test', show_progress=False)  # 批量加载
# docs = loader.split(chunk_size=200, chunk_overlap=50)
# docs = loader.get()
# print(len(docs))
# print(docs[-1])

# load: web
loader = WebLoader(path='https://zhuanlan.zhihu.com/p/339971541')
docs = loader.split(
    chunk_size=web.param(label="数据块大小", type='int', value=200),
    chunk_overlap=web.param(label="数据块重叠大小", type='int', value=50),
)
# docs = loader.split(
#     chunk_size=200,
#     chunk_overlap=50,
# )

# rag
embed_model = EmbeddingsHuggingFace(model_name="all-MiniLM-L6-v2")  #
vdb_model = FAISS
llm_model = ChatQianfan(model="ERNIE-Bot-turbo")
role_template = "{ra}\n user question: {query}"
rag = DocRAG(
    embed_model=embed_model,
    vdb_model=vdb_model,
    llm_model=llm_model,
    corpus=docs,
    role_template=role_template,
    return_language="中文",
    online_search_kwargs={},
    # online_search_kwargs={'topk': 2, 'timeout': 20},  # 搜索引擎配置，不开启则可以设置为 online_search_kwargs={}
)

web.run(
    obj=rag.invoke,
    input_param=[{"name": "query", "label": "用户输入内容", "type": "chat"},
                 {"name": "topk", "label": "最相似topk", "type": "int", "value": 5}
                 ],
    output_param=[{'label': '结果', 'name': 'ai', 'type': 'chat'},
                  {'label': '参考', 'name': 'refer', 'type': 'refer'}
                  ]
)

# rag.invoke(query="怎样评价宁德时代？")


