from pylmkit.app import RolePlay
from typing import Any, Optional, Iterable, List, Tuple, Type


class VectorDB(object):

    def __init__(self, corpus=None, embed_model=None, vdb_model=None, init_vdb=None):
        self.vdb = init_vdb
        if corpus and embed_model and vdb_model:
            corpus = self.any2doc(corpus)
            self.vdb = vdb_model.from_documents(corpus, embed_model, ids=[i for i in range(1, len(corpus) + 1)])

    @classmethod
    def load(cls, vdb_model, embed_model, vdb_path, vdb_name="index", is_return=True, extend=True, **kwargs):
        _vdb = vdb_model.load_local(vdb_path, embed_model, index_name=vdb_name, **kwargs)
        cls()._base(_vdb, is_return=is_return, extend=extend)

    @classmethod
    def save(cls, vdb_path: str, vdb_name: str = "index", vdb_model=None):
        if vdb_model is None:
            vdb_model = cls().vdb
        vdb_model.save_local(folder_path=vdb_path, index_name=vdb_name)

    @classmethod
    def add(cls, corpus, vdb_model=None, is_return=True, extend=True):
        if vdb_model is None:
            vdb_model = cls().vdb
        corpus = cls().any2doc(corpus)
        vdb = vdb_model.add_documents(documents=corpus)
        cls()._base(vdb, is_return=is_return, extend=extend)

    @classmethod
    def update(cls, ids, corpus, vdb_model=None, is_return=True, extend=True):
        if vdb_model is None:
            vdb_model = cls().vdb
        corpus = cls().any2doc(corpus)
        vdb_model.update_documents(ids=ids, documents=corpus)
        cls()._base(vdb_model, is_return=is_return, extend=extend)

    def get(self, ids, vdb_model=None):
        if vdb_model is None:
            vdb_model = self.vdb
        return vdb_model._collection.get(ids=ids)

    def delete(self, ids, vdb_model=None, is_return=False, extend=False):
        if vdb_model is None:
            vdb_model = self.vdb
        vdb_model = vdb_model._collection.delete(ids=ids)
        self._base(vdb_model, is_return=is_return, extend=extend)

    def count(self, vdb_model=None):
        if vdb_model is None:
            vdb_model = self.vdb
        return vdb_model._collection.count()

    def any2doc(self, corpus):
        from pylmkit.perception.text import Dict2Document, Text2Document
        # any, str dict doc
        if corpus and isinstance(corpus[0], str):
            corpus = Text2Document.get(texts=corpus, is_return=True, return_mode='doc', extend=False)
        elif corpus and isinstance(corpus[0], dict):
            corpus = Dict2Document.get(doc_dict=corpus, is_return=True, extend=False, return_mode='doc')
        else:
            corpus = corpus
        return corpus

    def _base(self, vdb_model, is_return=True, extend=False):
        if extend:
            self.vdb = vdb_model
        if is_return:
            return vdb_model

    def ra(self,
           question: str,
           topk: int = 5,
           search_language=[],
           lambda_val: float = 0.025,
           filter: Optional[str] = None,
           n_sentence_context: int = 2,
           **kwargs: Any, ):
        return self.vdb.similarity_search(
            query=question,
            k=topk,
            lambda_val=lambda_val,
            filter=filter,
            n_sentence_context=n_sentence_context,
            **kwargs
        )

    def retriever(self,
                  topk,
                  filter_metadata={},
                  fetch_k=20,
                  lambda_mult=0.5,
                  score_threshold=0.8,
                  search_type="similarity"
                  ):
        """from langchain: Return VectorStoreRetriever initialized from this VectorStore.

                Args:
                    search_type (Optional[str]): Defines the type of search that
                        the Retriever should perform.
                        Can be "similarity" (default), "mmr", or "similarity_score_threshold".
                    search_kwargs (Optional[Dict]): Keyword arguments to pass to the
                        search function. Can include things like:

                            public setting:
                                k: Amount of documents to return (Default: 4)
                                filter: Filter by document metadata

                            similarity_score_threshold setting:
                                score_threshold: Minimum relevance threshold
                                    for similarity_score_threshold

                            mmr setting:
                                fetch_k: Amount of documents to pass to MMR algorithm (Default: 20)
                                lambda_mult: Diversity of results returned by MMR;
                                    1 for minimum diversity and 0 for maximum. (Default: 0.5)


                Returns:
                    VectorStoreRetriever: Retriever class for VectorStore.

                Examples:

                .. code-block:: python

                    # Retrieve more documents with higher diversity
                    # Useful if your dataset has many similar documents
                    docsearch.as_retriever(
                        search_type="mmr",
                        search_kwargs={'k': 6, 'lambda_mult': 0.25}
                    )

                    # Fetch more documents for the MMR algorithm to consider
                    # But only return the top 5
                    docsearch.as_retriever(
                        search_type="mmr",
                        search_kwargs={'k': 5, 'fetch_k': 50}
                    )

                    # Only retrieve documents that have a relevance score
                    # Above a certain threshold
                    docsearch.as_retriever(
                        search_type="similarity_score_threshold",
                        search_kwargs={'score_threshold': 0.8}
                    )

                    # Only get the single most similar document from the dataset
                    docsearch.as_retriever(search_kwargs={'k': 1})

                    # Use a filter to only retrieve documents from a specific paper
                    docsearch.as_retriever(
                        search_kwargs={'filter': {'paper_title':'GPT-4 Technical Report'}}
                    )
                """
        search_kwargs = {}
        for kwarg in [topk, filter_metadata, fetch_k, lambda_mult, score_threshold]:
            if kwarg:
                search_kwargs[str(kwarg)] = kwarg
        return self.vdb.as_retriever(search_kwargs=search_kwargs, search_type=search_type)


class BaseRAG(VectorDB, RolePlay):
    """BaseRAG用于结合向量数据库检索和角色扮演功能。

    :param embed_model: 文本嵌入模型，用于将文本转换为向量。
    :param vdb_model: 向量数据库模型，用于存储和检索文本向量。
    :param llm_model: 大语言模型，用于生成特定角色的回答。
    :param corpus: 知识库，可以是list[str]、list[dict]或list[Document类]，提供额外的知识源。
    :param vdb_path: 已存在的向量数据库模型路径，如果指定，将使用该路径的数据库。
    :param vdb_name: 已存在的向量数据库模型名称，与vdb_path配合使用。
    :param init_vdb: 初始化向量数据库的参数，如果提供，将根据该参数创建数据库。
    :param prompt_list: list，提示词编排流，用于指导大模型的回答。
    :param memory: 记忆实例，用于让大模型记住历史对话内容。
    :param online_search_kwargs: dict，线上搜索参数配置，默认为{}，表示不开启线上搜索功能。
    :param show_language: str，指定返回答案的语言类型，可选值为'zh'（中文）或'en'（英文），默认为'en'。

    """
    def __init__(self,
                 embed_model,
                 vdb_model,
                 llm_model,
                 corpus=None,
                 vdb_path=None,
                 vdb_name="index",
                 init_vdb=None,
                 prompt_list=[],
                 memory=None,
                 online_search_kwargs={},
                 show_language="en",
                 ):
        VectorDB.__init__(self, init_vdb=None)
        RolePlay.__init__(self,
                          prompt_list=prompt_list,
                          llm_model=llm_model,
                          memory=memory,
                          online_search_kwargs=online_search_kwargs,
                          show_language=show_language
                          )
        if init_vdb:
            VectorDB.__init__(self, init_vdb=init_vdb)
        elif vdb_path and vdb_name:
            super().load(vdb_model=vdb_model,
                         embed_model=embed_model,
                         vdb_path=vdb_path,
                         vdb_name=vdb_name,
                         is_return=False,
                         extend=True
                         )
        elif corpus:
            super().__init__(corpus=corpus, embed_model=embed_model, vdb_model=vdb_model)
        else:
            raise Exception("`corpus`, `vdb_path`, `init_vdb` Cannot all be None!")

    def invoke(
            self,
            question: str,
            topk: int = 5,
            search_language=[],
            lambda_val: float = 0.025,
            filter: Optional[str] = None,
            n_sentence_context: int = 2,
            ra_kwargs={},
            **kwargs
    ):
        """根据用户问题和其他参数生成特定回答和相关输出。

        :param question: str，用户提出的问题，必选参数。
        :param topk: int，从向量数据库中检索最相似的前k个结果，默认为5。
        :param search_language: List[str]，当前搜索文本的语言类型列表，默认为空列表。
        :param lambda_val: float，衰减因子，用于调整搜索结果的权重，默认为0.025。
        :param filter: Optional[str]，过滤条件，用于筛选搜索结果，默认为None。
        :param n_sentence_context: int，上下文句子的数量，默认为2。
        :param ra_kwargs: dict，角色扮演功能的附加参数，默认为空字典。
        :param kwargs: dict，其他可选参数，用于提供额外的配置或数据。

        :return: tuple，包含两个元素：
            - response: str，生成的特定回答文本。
            - refer: list，生成的回答中引用的参考内容列表。
        """
        ra_documents = super().ra(
            question=question,
            topk=topk,
            search_language=search_language,
            lambda_val=lambda_val,
            filter=filter,
            n_sentence_context=n_sentence_context,
            **ra_kwargs
        )
        return super().invoke(question=question, ra_documents=ra_documents, **kwargs)

    def stream(
            self,
            question: str,
            topk: int = 5,
            search_language=[],
            lambda_val: float = 0.025,
            filter: Optional[str] = None,
            n_sentence_context: int = 2,
            ra_kwargs={},
            **kwargs
    ):
        """根据用户问题和其他参数生成特定回答和相关输出。

        :param question: str，用户提出的问题，必选参数。
        :param topk: int，从向量数据库中检索最相似的前k个结果，默认为5。
        :param search_language: List[str]，当前搜索文本的语言类型列表，默认为空列表。
        :param lambda_val: float，衰减因子，用于调整搜索结果的权重，默认为0.025。
        :param filter: Optional[str]，过滤条件，用于筛选搜索结果，默认为None。
        :param n_sentence_context: int，上下文句子的数量，默认为2。
        :param ra_kwargs: dict，角色扮演功能的附加参数，默认为空字典。
        :param kwargs: dict，其他可选参数，用于提供额外的配置或数据。

        :return: tuple，包含两个元素：
            - response: str，生成的特定回答文本。
            - refer: list，生成的回答中引用的参考内容列表。
        """
        ra_documents = super().ra(
            question=question,
            topk=topk,
            search_language=search_language,
            lambda_val=lambda_val,
            filter=filter,
            n_sentence_context=n_sentence_context,
            **ra_kwargs
        )
        return super().stream(question=question, ra_documents=ra_documents, **kwargs)


class DocRAG(BaseRAG):
    """BaseRAG类是VectorDB和RolePlay的基类，用于结合向量数据库和角色扮演功能。

    :param embed_model: 文本嵌入模型，用于将文本转换为向量。
    :param vdb_model: 向量数据库模型，用于存储和检索文本向量。
    :param llm_model: 大语言模型，用于生成特定角色的回答。
    :param corpus: 知识库，可以是list[str]、list[dict]或list[Document类]，提供额外的知识源。
    :param vdb_path: 已存在的向量数据库模型路径，如果指定，将使用该路径的数据库。
    :param vdb_name: 已存在的向量数据库模型名称，与vdb_path配合使用。
    :param init_vdb: 初始化向量数据库的参数，如果提供，将根据该参数创建数据库。
    :param prompt_list: list，提示词编排流，用于指导大模型的回答。
    :param memory: 记忆实例，用于让大模型记住历史对话内容。
    :param online_search_kwargs: dict，线上搜索参数配置，默认为{}，表示不开启线上搜索功能。
    :param show_language: str，指定返回答案的语言类型，可选值为'zh'（中文）或'en'（英文），默认为'en'。

    """
    def __init__(self,
                 embed_model,
                 vdb_model,
                 llm_model,
                 corpus=None,
                 vdb_path=None,
                 vdb_name="index",
                 init_vdb=None,
                 prompt_list=[],
                 memory=None,
                 online_search_kwargs={},
                 show_language="en",
                 ):
        super().__init__(
            embed_model=embed_model,
            vdb_model=vdb_model,
            llm_model=llm_model,
            corpus=corpus,
            vdb_path=vdb_path,
            vdb_name=vdb_name,
            init_vdb=init_vdb,
            prompt_list=prompt_list,
            memory=memory,
            online_search_kwargs=online_search_kwargs,
            show_language=show_language
        )


class WebRAG(BaseRAG):
    """BaseRAG类是VectorDB和RolePlay的基类，用于结合向量数据库和角色扮演功能。

        :param embed_model: 文本嵌入模型，用于将文本转换为向量。
        :param vdb_model: 向量数据库模型，用于存储和检索文本向量。
        :param llm_model: 大语言模型，用于生成特定角色的回答。
        :param corpus: 知识库，可以是list[str]、list[dict]或list[Document类]，提供额外的知识源。
        :param vdb_path: 已存在的向量数据库模型路径，如果指定，将使用该路径的数据库。
        :param vdb_name: 已存在的向量数据库模型名称，与vdb_path配合使用。
        :param init_vdb: 初始化向量数据库的参数，如果提供，将根据该参数创建数据库。
        :param prompt_list: list，提示词编排流，用于指导大模型的回答。
        :param memory: 记忆实例，用于让大模型记住历史对话内容。
        :param online_search_kwargs: dict，线上搜索参数配置，默认为{}，表示不开启线上搜索功能。
        :param show_language: str，指定返回答案的语言类型，可选值为'zh'（中文）或'en'（英文），默认为'en'。

        """
    def __init__(self,
                 embed_model,
                 vdb_model,
                 llm_model,
                 corpus=None,
                 vdb_path=None,
                 vdb_name="index",
                 init_vdb=None,
                 prompt_list=[],
                 memory=None,
                 online_search_kwargs={},
                 show_language="en",
                 ):
        super().__init__(
            embed_model=embed_model,
            vdb_model=vdb_model,
            llm_model=llm_model,
            corpus=corpus,
            vdb_path=vdb_path,
            vdb_name=vdb_name,
            init_vdb=init_vdb,
            prompt_list=prompt_list,
            memory=memory,
            online_search_kwargs=online_search_kwargs,
            show_language=show_language
        )



