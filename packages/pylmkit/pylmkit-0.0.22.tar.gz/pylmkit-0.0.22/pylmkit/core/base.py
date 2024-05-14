import re
import time, logging
import pandas as pd
from pathlib import Path
import streamlit as st
from pylmkit.utils.data_utils import *
from pylmkit.core.prompt import *
from functools import partial
from pylmkit.core.html import init_css, init_footer, init_logo
from pylmkit.core.html import _zh, _en

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)


class BaseMemory(object):
    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    system_prefix: str = "System"

    def __init__(self, init_memory=None, streamlit_web=False):
        self.memory_messages = []
        self.streamlit_web = streamlit_web
        if self.streamlit_web:  # streamlit rerun page, so need cache
            if "memory" not in st.session_state:
                st.session_state["memory"] = self.memory_messages
        if isinstance(init_memory, list):
            self.memory_messages = init_memory
            if self.streamlit_web:
                st.session_state['memory'] = self.memory_messages
        if self.streamlit_web:  # streamlit rerun page, so need cache
            self.memory_messages = st.session_state['memory']

    def add(self, role, content, refer=''):
        """ role，human ai system
        """
        if role in ['user', 'User', 'USER', 'human', 'Human', 'HUMAN']:
            role = self.human_prefix
        elif role in ['ai', 'Ai', 'AI', 'assistant']:
            role = self.ai_prefix
        elif role in ['sys', 'system', 'System', 'SYS', 'SYSTEM']:
            role = self.system_prefix
        else:
            raise Exception(f"The role `{role}` does not exist")
        self.memory_messages.append(
            {"role": role, "content": content, "refer": refer, "date": time.strftime('%Y-%m-%d %H:%M:%S')})
        if self.streamlit_web:  # streamlit rerun page, so need cache
            st.session_state['memory'] = self.memory_messages

    def to_csv(self, filepath, index=False, **kwargs):
        data = self.memory_messages
        pd.DataFrame(data).to_csv(filepath, index=index, **kwargs)

    def clear(self):
        self.memory_messages = []
        if self.streamlit_web:  # streamlit rerun page, so need cache
            st.session_state['memory'] = self.memory_messages

    def _get(self, mode='message'):
        if mode == 'message':
            return self.memory_messages
        elif mode == 'string':
            return message_as_string(self.memory_messages)
        else:
            raise Exception(f"There is no such `{mode}` mode. Support modes: message, string")


class BaseKnowledgeBase(object):
    def __init__(self, init_documents=None):
        self.documents = []
        self.splitter_documents = []
        if isinstance(init_documents, list):
            self.documents = init_documents

    @classmethod
    def load(cls, filepath, is_return=True, return_mode="doc", extend=True):
        if filepath.endswith('.json'):
            data = read_json(filepath)
        elif filepath.endswith('.yaml') or filepath.endswith('yml'):
            data = read_yaml(filepath)  # data=[{},{}]
        else:
            raise Exception(f"The file type is not supported")
        data_dict_as_document = dict_as_document(data)
        result = cls()._base(documents=data_dict_as_document, return_mode=return_mode, is_return=is_return,
                             extend=extend)
        if is_return:
            return result

    @classmethod
    def add(cls, texts, metadatas=None, is_return=True, return_mode="doc", extend=True, types="Document"):
        data_dict_as_document = text_as_document(texts=texts, metadatas=metadatas, types=types)
        result = cls()._base(documents=data_dict_as_document, return_mode=return_mode, is_return=is_return,
                             extend=extend)
        if is_return:
            return result

    def split(self, splitter=None, chunk_size=500, chunk_overlap=100, return_mode='doc', **kwargs):
        if splitter is None:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, **kwargs)
        else:
            splitter = splitter
        self.splitter_documents = splitter.split_documents(self.documents)
        if return_mode == 'doc':
            return self.splitter_documents
        else:
            return document_as_dict(self.splitter_documents)

    def to_csv_loader(self, filepath, index=False, **kwargs):
        data = document_as_dict(self.documents)
        pd.DataFrame(data).to_csv(filepath, index=index, **kwargs)

    def to_csv_splitter(self,
                        filepath,
                        splitter=None,
                        chunk_size=500,
                        chunk_overlap=100,
                        index=False,
                        splitter_kwargs={},
                        csv_kwargs={}
                        ):
        if not self.splitter_documents:
            self.splitter_documents = self.split(splitter=splitter, chunk_size=chunk_size,
                                                 chunk_overlap=chunk_overlap, **splitter_kwargs)
        data = document_as_dict(self.splitter_documents)
        pd.DataFrame(data).to_csv(filepath, index=index, **csv_kwargs)

    def clear(self, mode='doc'):
        if mode == 'doc':
            self.documents = []
        else:
            self.splitter_documents = []

    def _base(self, documents, is_return=True, return_mode='doc', extend=True):
        if extend:
            self.documents.extend(documents)  # # dict -> Document
            if is_return:
                if return_mode == 'doc':
                    return self.documents
                else:
                    return document_as_dict(self.documents)
        else:
            # self.documents = documents  # when extend is False, just reset documents
            if is_return:
                if return_mode == 'doc':
                    return documents
                else:
                    return document_as_dict(documents)


def input_widget(input1, input2, type, value):
    if type == "int":
        return st.number_input(format='%d', step=1, **input1)
    if type == "float":
        return st.number_input(format='%f', **input1)
    elif type in ['list', 'List', 'select']:
        return st.selectbox(options=value, **input2)
    elif type == "bool":
        if value in [True, 'True', 'true']:
            options = [True, False]
        else:
            options = [False, True]
        return st.radio(options=options, horizontal=True, **input2)
    elif type == "file":
        uploaded_file = st.file_uploader(**input2)
        if uploaded_file is not None:
            res = str(Path().cwd() / uploaded_file.name)
            with open(res, "wb") as f:
                f.write(uploaded_file.getbuffer())
        else:
            res = None
        return res
    elif type in ['multiselect']:
        return st.multiselect(options=value, **input2)
    else:
        return st.text_input(**input1)


def generate_input_widget(mode="main", **kwargs):  # 在前端生成输入框
    """
    mode, default "main" ,other "sidebar"
    """
    label = kwargs.get('label', "")
    value = kwargs.get('value', None)
    name = kwargs.get('name', None)
    _input1 = {"label": label, "value": value, "key": f"{name}-{label}"}
    _input2 = {"label": label, "key": f"{name}-{label}"}
    _type = kwargs.get('type', None)  # int float bool string chat file
    if mode == 'main':
        return input_widget(
            input1=_input1,
            input2=_input2,
            type=_type,
            value=value
        )
    else:
        with st.sidebar:
            return input_widget(
                input1=_input1,
                input2=_input2,
                type=_type,
                value=value
            )


class BaseSQLRunnable(object):
    def __init__(self, model, connector):
        self.model = model
        self.connector = connector
        self.sql_prompt = sql_prompt
        self.sql_qa_prompt = sql_qa_prompt
        self.chart_prompt = chart_prompt
        self.select_tool_prompt = select_tool_prompt
        self.tool_list = [table_list, line_chart, pie_chart, bar_chart, funnel_chart, scatter_chart, text_answer]

    def runnable(self, prompt_list, rollback_num: int = 5, connector: dict = {}):
        from pylmkit.tools.kit import SQLToolKit
        res = SQLToolKit.sql_executor(
            model=self.model,
            prompt_list=prompt_list,
            rollback_num=rollback_num,
            db=self.connector,
            connector=connector
        )
        return res

    def wrapper(self, fun):
        return partial(fun)


class BaseAgentParse(object):
    def __init__(self):
        pass

    def base(self, command: str, formatter: str, parse_type: str):
        """解析命令字符串中的特定格式代码块。

        ## 参数
        command : str
            包含要解析的代码块的字符串。
        formatter : str
            指定要解析的代码块的格式化器，例如'tool'或'python'。
        parse_type : str
            指定解析类型，'xml'或'codeblock'。

        ## 返回
        OutputFormat
            一个OutputFormat实例，其中包含解析结果的状态、输出和错误信息。

        ## 示例
        >>> command = "这里是文字<tool>第一个工具内容</tool>这里是文字<tool>第二个工具内容</tool>这里是文字"
        >>> results = parse(command, 'tool', 'xml')
        >>> print(results.output)
        ['第一个工具内容', '第二个工具内容']
        """
        from pylmkit.tools.parse import OutputFormat
        _results = OutputFormat()
        _results.output = _results.output.copy()
        if parse_type == 'xml':
            pattern = f'<{formatter}>(.*?)</{formatter}>'
        elif parse_type == 'codeblock':
            pattern = f'```{formatter}\n(.*?)\n```'
        else:
            raise TypeError('Type must be specified!')
        try:
            matches = re.findall(pattern, command, re.DOTALL)
            if matches:
                _results.output = matches
                _results.status = True
            else:
                _results.output = []
            return _results
        except Exception as e:
            _results.error = str(e)
            return _results


class BasePromptFlow(object):
    @classmethod
    def formatted_str(cls, prompt_list: list, sep: str = '\n') -> str:
        return f"{sep}".join(prompt_list).strip()

    @classmethod
    def set_language(cls, lang: str = 'zh') -> str:
        if lang in ['zh', '中文', '中文简体', '中文繁体', 'china', 'China', 'Chinese', 'chinese', '中国']:
            return "Please answer in simplified Chinese."
        else:
            return "Please answer in English."

    @classmethod
    def replace_placeholders(cls, template: str, replacements: dict):
        replacements = {f'{{{key}}}': value for key, value in replacements.items()}

        def replace_placeholder(match):
            return replacements.get(match.group(0), match.group(0))

        return re.sub(r'\{[a-zA-Z0-9_]+\}', replace_placeholder, template)

    @classmethod
    def formatted_list(cls, prompt_list: list, sep: str = '1__0__1', **kwargs) -> list:
        if kwargs:
            prompt = cls.formatted_str(prompt_list, sep=sep)
            prompt = cls.replace_placeholders(prompt, kwargs)
            prompt = prompt.split(sep)
        else:
            prompt = prompt_list
        return prompt


class BaseWebUI(object):
    def __init__(self,
                 title=None,
                 page_icon=None,
                 layout="centered",
                 language='en',
                 sidebar_title=None,
                 sidebar_describe=None,
                 footer_describe=None,
                 logo1=None,
                 logo2=None,
                 greetings=None,
                 placeholder=None,
                 refer_name=None,
                 ):
        self.title = title
        self.layout = layout
        self.page_icon = page_icon
        self.footer_describe = footer_describe
        self.sidebar_title = sidebar_title
        self.sidebar_describe = sidebar_describe
        self.logo1 = logo1
        self.logo2 = logo2
        self.greetings = greetings
        self.placeholder = placeholder
        self.refer_name = refer_name
        if language in ['zh', '中国', 'china']:
            self.lang = _zh
            self.spinner_text = 'PyLMKit：生成中，请稍候...'
        else:
            self.lang = _en
            self.spinner_text = 'PyLMKit: Generating, please wait...'
        if self.title is None:
            self.title = self.lang.get('_title', '')
        if self.page_icon is None:
            self.page_icon = self.lang.get('_page_icon', None)
        if self.footer_describe is None:
            self.footer_describe = self.lang.get('_footer_describe', '')
        if self.sidebar_title is None:
            self.sidebar_title = self.lang.get('_sidebar_title', '')
        if self.sidebar_describe is None:
            self.sidebar_describe = self.lang.get('_sidebar_describe', '')
        if self.logo1 is None:
            self.logo1 = self.lang.get('_logo1', '')
        if self.logo2 is None:
            self.logo2 = self.lang.get('_logo2', '')
        if self.greetings is None:
            self.greetings = self.lang.get('_greetings', '')
        if self.placeholder is None:
            self.placeholder = self.lang.get('_placeholder', '')
        if self.refer_name is None:
            self.refer_name = self.lang.get('_refer_name', 'refer')

        self.base_page()
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": self.greetings}]
        self.input_kwargs = {}
        st.session_state["output_kwargs"] = {}
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
            # refer setting
            refer = msg.get("refer", False)
            if refer:
                with st.expander(label=self.refer_name, expanded=False):
                    st.markdown(refer, unsafe_allow_html=True)

    def _input(self, content, role="user", avatar="😄", message_type='messages'):
        st.chat_message(role, avatar=avatar).write(content, unsafe_allow_html=True)
        msg = {"role": role, "content": content}
        st.session_state[message_type].append(msg)

    def _output(self, content, refer=None, role="assistant"):
        # st.chat_message(role).write(content, unsafe_allow_html=True)
        with st.chat_message(role):
            if isinstance(content, dict):
                st.json(content)
            else:
                content_placeholder = st.empty()
                full_content = ""
                for chunk in str(content):
                    full_content += chunk + ""
                    time.sleep(0.01)
                    content_placeholder.markdown(full_content + "▌")
                content_placeholder.markdown(full_content)

        if refer:  # refer setting
            with st.expander(label=self.refer_name, expanded=False):
                st.markdown(refer, unsafe_allow_html=True)
        msg = {"role": role, "content": content, "refer": refer}
        st.session_state.messages.append(msg)

    def output_parse(self, output_param, output_result):
        refer = None
        if len(output_param) == 0:
            response = None
        elif len(output_param) == 1:
            response = output_result
            st.session_state["output_kwargs"][output_param[0]['name']] = response
        else:
            response = output_result[0]
            for i, arg in enumerate(output_param):
                st.session_state["output_kwargs"][arg['name']] = output_result[i]
                if arg['type'] == 'chat':
                    response = output_result[i]
                if arg['type'] == 'refer':
                    refer = output_result[i]
        return response, refer

    def base_run(self, obj, input_param: list, message_type="messages"):
        chat_variable = ""
        obj = self.wrapper(obj)
        for arg in input_param:
            if arg['type'] != 'chat':
                self.input_kwargs[arg['name']] = generate_input_widget(mode='sidebar', **arg)
            else:
                chat_variable = arg['name']
        if chat_variable:
            if prompt := st.chat_input(placeholder=self.placeholder):
                self.input_kwargs[chat_variable] = prompt
                self._input(content=prompt, message_type=message_type)
                with st.spinner(self.spinner_text):  # 正在生成，请稍候...
                    result = obj(**self.input_kwargs)
                    return result, chat_variable
        else:
            with st.spinner(self.spinner_text):  # 正在生成，请稍候...
                result = obj(**self.input_kwargs)
                return result, chat_variable

    def run(self, obj, input_param: list, output_param: list):
        result = self.base_run(obj, input_param)
        if result:
            result, chat_variable = result
            if chat_variable:
                response, refer = self.output_parse(output_param, result)
                self._output(content=response, refer=refer)
            else:
                with st.spinner(self.spinner_text):  # 正在生成，请稍候...
                    response, refer = self.output_parse(output_param, result)
                    # self._output(content=response, refer=refer)
                    with st.expander(label="output", expanded=True):
                        st.json(st.session_state["output_kwargs"], expanded=True)

    def wrapper(self, fun):
        return partial(fun)

    def param(self, label, type, value, mode='sidebar'):
        input_kwargs = {
            "label": label,
            "type": type,
            "value": value
        }
        key = f"{label}-{type}-{str(value)}"
        if key not in st.session_state.keys():
            st.session_state[key] = ""
        renew_value = generate_input_widget(
            mode=mode,
            **input_kwargs
        )
        return renew_value

    def base_page(self):
        st.set_page_config(
            page_title=self.title,
            layout=self.layout,
            page_icon=self.page_icon,
        )
        st.markdown(init_css, unsafe_allow_html=True)
        if self.footer_describe:
            st.sidebar.markdown(init_footer.format(self.footer_describe), unsafe_allow_html=True)
        # if self.sidebar_title:
        #     st.sidebar.title(self.sidebar_title)
        # if self.sidebar_describe:
        #     st.sidebar.markdown(self.sidebar_describe, unsafe_allow_html=True)
        if self.logo2:
            st.markdown(init_logo.format(**self.logo2), unsafe_allow_html=True)
        if self.logo1:
            st.markdown(init_logo.format(**self.logo1), unsafe_allow_html=True)
