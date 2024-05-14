# coding: utf-8
import json
import toml
import pandas as pd
import yaml
from pathlib import Path
from yaml.loader import SafeLoader
from pydantic import Field, BaseModel
from typing import Literal
# from langchain.docstore.document import Document


def yield_specify_file(paths, suffixes):
    """Returns the file of the specified suffix"""
    for path in paths:
        if path.is_file():
            if suffixes and path.suffix not in suffixes:
                continue
            yield path


class Document(BaseModel):
    page_content: str
    metadata: dict = Field(default_factory=dict)
    type: str = "Document"

    def __str__(self):
        return f"Document(page_content='{self.page_content}', metadata={self.metadata})"


def stream_print(string, buffer_size=3):
    buffer = []
    for char in string:
        buffer.append(char)
        if len(buffer) >= buffer_size:
            yield ''.join(buffer)
            buffer.clear()
    if buffer:
        yield ''.join(buffer)


def document_as_refer(documents):
    document_refer = [f"[{i + 1}] **{doc.metadata['source']}**  {doc.page_content}\n\n" for i, doc in
                      enumerate(documents)]
    return "".join(document_refer)


def document_as_dict(documents):
    document_dict = [{"page_content": doc.page_content, "metadata": doc.metadata,
                      "type": doc.type} for doc in documents]
    return document_dict


def dict_as_document(doc_dict):
    document_dict = [Document(page_content=doc['page_content'],
                              metadata=doc.get('metadata', {}),
                              type=doc.get('type', 'Document')) for doc in doc_dict]
    return document_dict


def document_as_string(documents, sep=""):
    document_string = f"{sep}".join([doc.page_content for doc in documents])
    return document_string


def message_as_string(memory_messages):
    messages_string = [f"\n{message['role']}: {message['content']}" for message in memory_messages]
    return "".join(messages_string)


def text_as_document(texts, metadatas=None, types="Document"):
    documents = []
    if metadatas:
        if isinstance(types, str):
            for i, text in enumerate(texts):
                documents.append(Document(page_content=text, metadata=metadatas[i], type=types))
        else:  # types is `list` mode
            for i, text in enumerate(texts):
                documents.append(Document(page_content=text, metadata=metadatas[i], type=types[i]))
    else:
        if isinstance(types, str):
            for i, text in enumerate(texts):
                documents.append(Document(page_content=text, type=types))
        else:  # types is `list` mode
            for i, text in enumerate(texts):
                documents.append(Document(page_content=text, type=types[i]))
    return documents


def read_yaml(filepath):
    try:
        with open(filepath, encoding="utf-8") as fp:
            result = yaml.load(fp, Loader=SafeLoader)
    except Exception as e:
        raise Exception(e)
    return result


def write_yaml(data, filepath, mode="w", encoding='utf-8'):
    try:
        with open(filepath, mode=mode, encoding=encoding) as f:
            yaml.dump(data=data, stream=f, allow_unicode=True)
    except Exception as e:
        raise Exception(e)


def create_yaml(filepath, data):
    if not Path(filepath).exists():
        write_yaml(filepath, data)


def write_json(data, filepath, mode='w', encoding='utf-8', ensure_ascii=False):
    with open(filepath, mode, encoding=encoding) as fp:
        json.dump(data,  # 字典数据
                  fp=fp,  # open 文件
                  ensure_ascii=ensure_ascii,  # 确保中文无乱码
                  )


def read_json(filepath, mode='r', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as fp:
        data = json.load(fp)
    return data


def read_csv_document(filepath, **kwargs):
    df = pd.read_csv(filepath, **kwargs)
    data = df.to_dict(orient='records')  # list(dict)
    return data


def read_csv_memory(filepath, **kwargs):
    df = pd.read_csv(filepath, **kwargs)
    data = df.to_dict(orient='records')  # list(dict)
    return data


def read_toml(file_path):
    with open(file_path, "r") as file:
        toml_data = toml.load(file)
    return toml_data


def write_toml(data, file_path):
    with open(file_path, "w") as file:
        toml.dump(data, file)


def iter_data(seq):
    for i in seq:
        yield i


def line_chart():
    """当用户问题适合使用折线图时调用，如涉及趋势、曲线等"""
    from pylmkit.core.prompt import line_chart_prompt
    return line_chart_prompt.replace('{type}', 'LineChart')


def bar_chart():
    """当用户问题适合使用柱形图时调用"""
    from pylmkit.core.prompt import line_chart_prompt
    return line_chart_prompt.replace('{type}', 'BarChart')


def scatter_chart():
    """当用户问题适合使用散点图时调用"""
    from pylmkit.core.prompt import line_chart_prompt
    return line_chart_prompt.replace('{type}', 'ScatterChart')


def pie_chart():
    """当用户问题适合使用饼图时调用"""
    from pylmkit.core.prompt import pie_chart_prompt
    return pie_chart_prompt.replace('{type}', 'PieChart')


def funnel_chart():
    """当用户问题适合使用漏斗图时调用"""
    from pylmkit.core.prompt import pie_chart_prompt
    return pie_chart_prompt.replace('{type}', 'FunnelChart')


def table_list():
    """当用户问题适合使用表格、清单回答时调用"""
    from pylmkit.core.prompt import table_list_prompt
    return table_list_prompt


def text_answer():
    """当用户问题适合直接使用文本回答时调用"""
    from pylmkit.core.prompt import text_answer_prompt
    return text_answer_prompt


