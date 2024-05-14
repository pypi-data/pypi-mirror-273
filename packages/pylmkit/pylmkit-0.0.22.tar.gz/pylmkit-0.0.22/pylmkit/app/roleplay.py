import logging
from pylmkit.utils.data_utils import *
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )
logger = logging.getLogger(__name__)


class RolePlay(object):
    """角色扮演功能，旨在引导大型语言模型按照特定的设定方向生成回答。

    :param llm_model: 大型语言模型实例，必选参数。用于生成特定角色的回答。
    :param prompt_list: list of str, 提示词编排流。例如，prompt_list=['你是一个搞笑大王，对用户输入问题编一个笑话。']。
    :param memory: 记忆实例，可选参数。用于让大型模型记住历史对话内容。
    :param online_search_kwargs: dict, 线上搜索参数配置，可选参数。默认为{}，表示不开启线上搜索功能。
    :param show_language: str, 指定返回答案的语言类型。可选项为 'zh'（中文）或 'en'（英文），默认为 'en'。
    """
    def __init__(self,
                 llm_model,
                 prompt_list: list = [],
                 memory=None,
                 online_search_kwargs={},
                 show_language="en",
                 ):
        logger.info('RolePlay init ...')
        self.model = llm_model
        self.prompt_list = prompt_list
        if not self.prompt_list:
            self.prompt_list += ['Based on the provided content, answer the user’s question.']
        self.show_language = show_language
        self.memory = memory
        if online_search_kwargs:
            from pylmkit.tools.search import WebSearch
            self.search = WebSearch(**online_search_kwargs)
        else:
            self.search = None

    def invoke(self, question: str, ra_documents: list = [], **kwargs):
        """调用角色扮演功能，结合用户提出的问题和检索到的文档列表来生成特定的回答。

        :param question: str，用户提出的问题，必选参数。
        :param ra_documents: list，检索到的文档列表，用于提供额外的上下文信息，可选参数。
        :param kwargs: dict，其他可选的关键字参数，用于提供额外的配置或数据。

        :return: tuple，包含两个元素：
            - response: str，生成的特定回答文本。
            - refer: list，生成的回答中引用的参考内容列表。
        """
        _prompt, refer = self._invoke(question, ra_documents=ra_documents, **kwargs)
        response = self.model.invoke(_prompt)
        response = [response if isinstance(response, str) else response.content][0]
        if self.memory:
            if not refer:
                self.memory.add(role='ai', content=response)  # add ai output
            else:
                self.memory.add(role='ai', content=response, refer=refer)
        return response, refer

    def stream(self, question: str, ra_documents=[], **kwargs):
        """流式调用角色扮演功能，根据用户问题和检索到的文档生成特定回答。

        :param question: str，用户提出的问题。
        :param ra_documents: list，检索到的文档列表，用于提供额外的上下文信息。
        :param kwargs: dict，其他可选参数，用于自定义角色扮演的行为。

        :return: tuple，包含两个元素：
            - response: str，生成的特定回答文本。
            - refer: list，生成的回答中引用的参考内容列表。
        """
        _prompt, refer = self._invoke(question, ra_documents=ra_documents, **kwargs)
        response = self.model.invoke(_prompt)
        response = [response if isinstance(response, str) else response.content][0]
        if self.memory:
            if not refer:
                self.memory.add(role='ai', content=response)  # add ai output
            else:
                self.memory.add(role='ai', content=response, refer=refer)
        return iter_data(response), refer

    def return_memory(self):
        return self.memory.memory_messages

    def clear_memory(self):
        self.memory.clear()

    def _invoke(self, query, ra_documents=[], **kwargs):
        from pylmkit.core.base import BasePromptFlow
        temporary_prompt = []
        # search
        search_content = ""
        search_documents = []
        if self.search and query:
            try:
                search_documents = self.search.get(keyword=query)
                search_content = document_as_string(documents=search_documents)
            except Exception as e:
                logger.error(f"RolePlay web search error：{e}")
        # ra base
        ra_content = ""
        if ra_documents:
            ra_content = document_as_string(documents=ra_documents)
        # refer
        refer = []
        refer.extend(search_documents)
        refer.extend(ra_documents)
        refer = document_as_refer(refer)
        # memory
        memory_content = ""
        if self.memory and query:
            memory_content = self.memory.get()
            if isinstance(memory_content, list):
                memory_content = message_as_string(memory_content)
            self.memory.add(content=query, role='human')  # add user input
        temporary_prompt = self.prompt_list.copy()
        if memory_content:
            temporary_prompt.insert(len(temporary_prompt), "Historical dialogue:\n{memory}")
        content_prompt = "Contextual content found in the search results:"
        if search_content:
            content_prompt += "\n{search}"
        if ra_content:
            content_prompt += "\n{docs}"
        if search_content or ra_content:
            temporary_prompt.insert(len(temporary_prompt), content_prompt)
        temporary_prompt.insert(len(temporary_prompt), 'question: {question}')
        temporary_prompt.insert(len(temporary_prompt), BasePromptFlow.set_language(lang=self.show_language))
        # prompt
        _prompt = BasePromptFlow.formatted_list(
            temporary_prompt,
            memory=memory_content.strip(),
            search=search_content.strip(),
            docs=ra_content.strip(),
            question=query.strip()
        )
        prompt = BasePromptFlow.formatted_str(_prompt, sep='\n\n')
        return prompt.strip(), refer

