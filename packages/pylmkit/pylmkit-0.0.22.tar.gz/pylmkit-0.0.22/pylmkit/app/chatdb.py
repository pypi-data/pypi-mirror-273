import os
import logging
import pandas as pd
from typing import Dict, List, Optional
from pylmkit.tools.parse import ActionParse
from pylmkit.tools.parse import OutputFormat
from pylmkit.utils.sql_base import DBConnector
from pylmkit.tools.action import RollBackAction
from pylmkit.core.base import BaseSQLRunnable, BasePromptFlow
from pylmkit.tools.common import select_tool
from pylmkit.tools.executor import PythonREPL

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )
logger = logging.getLogger(__name__)


class ChatDB(BaseSQLRunnable):
    """ChatDB用于与数据库进行交互，支持结构化数据的问答。

    :param db_config: dict，数据库配置参数，必选。用于连接和操作数据库。
    :param model: 大语言模型实例，必选。用于生成自然语言形式的回答。
    :param memory: 记忆实例，可选。用于存储和检索历史对话信息。
    :param include_tables: List[str]，需要包含的数据库表名列表，可选。例如：['table1', 'table2']。
    :param include_columns: Dict[str, List]，需要包含的数据库字段映射，可选。例如：{'table1': ['column1', 'column2'], 'table2': []}。
    """

    def __init__(
            self,
            model,
            db_config: dict = {},
            memory=None,
            init_db=None,
            include_tables: List[str] = None,
            include_columns: Optional[Dict[str, List]] = {}
    ):
        logger.info("ChatDB init ...")
        self.model = model
        if init_db:
            self.db = init_db
        else:
            self.db = DBConnector.from_uri_db(**db_config)
        if not db_config and not init_db:
            raise ValueError("db_config 和 init_db 不可以同时为空！")
        self.db_type = self.db.extract_db_type()
        self.include_tables = include_tables
        self.include_columns = include_columns
        BaseSQLRunnable.__init__(self, model=self.model, connector=self.db)
        logger.info(f"Database type is {self.db_type}")

    def sql(self, question, rollback_num: int = 5, sql_prompt_list: List = []) -> OutputFormat:
        """根据用户问题生成SQL查询。

        :param question: str, 用户提出的问题，必选参数。
        :param rollback_num: int, 最大回滚数，用于控制历史记录的回溯，可选参数，默认为5。
        :param sql_prompt_list: List[str], 生成SQL查询的提示词列表，可选参数，默认为空列表。

        :return: OutputFormat, 返回一个OutputFormat类的实例，包含以下属性：
            - status: 状态信息，表示操作是否成功。
            - error: 错误信息，如果操作失败，将包含错误详情。
            - output: dict, 输出结果，包含以下键：
                - sql: 生成的SQL查询。
                - result: 查询SQL结果。
        """
        table_info = self.db.get_table_describe(self.include_tables, self.include_columns)
        if not sql_prompt_list:
            prompt = BasePromptFlow.formatted_list(
                prompt_list=self.sql_prompt,
                dbtype=self.db_type,
                question=question,
                table_info=table_info
            )
        else:
            prompt = BasePromptFlow.formatted_list(
                prompt_list=sql_prompt_list,
                dbtype=self.db_type,
                question=question,
                table_info=table_info
            )
        runnable_results = super().runnable(prompt_list=prompt, rollback_num=rollback_num)
        return runnable_results

    def invoke(self, question, rollback_num: int = 5, show_language='en', qa_result_num: int = 5,
               table_line: int = 10, sql_prompt_list: List = [], sql_qa_prompt_list: List = []) -> OutputFormat:
        """数据库问答

        :param question: str, 用户提出的问题，必选参数。
        :param rollback_num: int, 最大回滚数，用于控制历史记录的回溯，可选参数，默认为5。
        :param show_language: str, 选择展示的语言类型，可选值为'zh'（中文）或'en'（英文），默认为'en'。
        :param qa_result_num: int, 选择多少个记录参与数据库问答，可选参数，默认为5。
        :param table_line: int, 返回的表格的行数，可选参数，默认为10。
        :param sql_prompt_list: List[str], 生成SQL查询的提示词列表，可选参数，默认为空列表。
        :param sql_qa_prompt_list: List[str], 数据库问答的提示词列表，可选参数，默认为空列表。

        :return: OutputFormat, 返回一个OutputFormat类的实例，包含以下属性：
            - status: 状态信息，表示操作是否成功。
            - error: 错误信息，如果操作失败，将包含错误详情。
            - output: dict, 输出结果，包含以下键：
                - analysis: 分析结果。
                - sql: 生成的SQL查询。
                - table: 包含查询结果的表格。
        """
        logger.info("ChatDB invoke init ...")
        _results = OutputFormat()
        _results.output = _results.output.copy()
        logger.info("ChatDB invoke generate SQL ...")
        runnable_results = self.sql(question=question, rollback_num=rollback_num, sql_prompt_list=sql_prompt_list)
        if runnable_results.status:
            logger.info("ChatDB invoke run SQL successful ...")
            try:
                if sql_qa_prompt_list:
                    _sql_qa_prompt = sql_qa_prompt_list
                else:
                    _sql_qa_prompt = self.sql_qa_prompt
                _sql_qa_prompt.insert(len(_sql_qa_prompt), BasePromptFlow.set_language(lang=show_language))
                prompt = BasePromptFlow.formatted_list(
                    prompt_list=_sql_qa_prompt,
                    question=question,
                    query=runnable_results.output['sql'],
                    result=str(runnable_results.output['result'][:qa_result_num])
                )
                prompt = BasePromptFlow.formatted_str(prompt)
                answer = self.model.invoke(prompt)
                answer = answer if isinstance(answer, str) else answer.content
                _results.output['analysis'] = answer
                _results.output['sql'] = runnable_results.output['sql']
                _results.output['table'] = runnable_results.output['result'][:table_line]
                _results.status = True
                return _results
            except Exception as e:
                logger.info(f"ChatDB Model sql qa error：{e}")
                _results.error = f"Model sql qa error：{e}"
                return _results
        else:
            _results.error = runnable_results.error
            logger.info("ChatDB invoke generate SQL Fail ...")
            return _results

    def chart(self, question, rollback_num: int = 5, show_language='en', qa_result_num: int = 5,
              table_line: int = 10, sql_prompt_list: List = [], sql_qa_prompt_list: List = [],
              chart_prompt_list: List = [], use_select_tool: bool = True, select_tool_prompt: list = [], tool_list: list = []
              ) -> OutputFormat:
        """数据库问答多模态输出：图表分析。

        :param question: str, 用户提出的问题，必选参数。
        :param rollback_num: int, 最大回滚数，用于控制历史记录的回溯，可选参数，默认为5。
        :param show_language: str, 选择展示的语言类型，可选值为'zh'（中文）或'en'（英文），默认为'en'。
        :param qa_result_num: int, 选择多少个记录参与数据库问答，可选参数，默认为5。
        :param table_line: int, 返回的表格的行数，可选参数，默认为10。
        :param sql_prompt_list: List[str], 生成SQL查询的提示词列表，可选参数，默认为空列表。
        :param sql_qa_prompt_list: List[str], 数据库问答的提示词列表，可选参数，默认为空列表。
        :param chart_prompt_list: List[str], 生成图表的提示词列表，可选参数，默认为空列表。
        :param use_select_tool: bool，默认True。
        :param select_tool_prompt: List[str], 选择工具的提示词列表，可选参数，默认为空列表。
        :param tool_list: List[str], 可用的工具列表，可选参数，默认为空列表。

        :return: OutputFormat, 返回一个OutputFormat类的实例，包含以下属性：
            - status: 状态信息，表示操作是否成功。
            - error: 错误信息，如果操作失败，将包含错误详情。
            - output: dict, 输出结果，包含以下键：
                - analysis: 分析结果。
                - sql: 生成的SQL查询。
                - table: 包含查询结果的表格。
                - chart: 生成的图表。
        """
        logger.info("ChatDB chart init ...")
        logger.info("ChatDB chart generate SQL ...")
        runnable_results = self.invoke(
            question=question,
            rollback_num=rollback_num,
            show_language=show_language,
            table_line=table_line,
            qa_result_num=qa_result_num,
            sql_prompt_list=sql_prompt_list,
            sql_qa_prompt_list=sql_qa_prompt_list
        )
        _results = OutputFormat()
        _results.output = _results.output.copy()
        if runnable_results.status:
            logger.info("ChatDB chart Run SQL successful ...")
            _results.output['sql'] = runnable_results.output['sql']
            _results.output['table'] = runnable_results.output['table'][:table_line]
            _results.output['analysis'] = runnable_results.output['analysis']
            if _results.output['table']:
                if chart_prompt_list:
                    _chart_prompt = chart_prompt_list
                else:
                    _chart_prompt = self.chart_prompt.copy()
                _chart_prompt.insert(len(_chart_prompt), BasePromptFlow.set_language(lang=show_language))
                if use_select_tool:
                    if select_tool_prompt:
                        _select_tool_prompt = select_tool_prompt
                    else:
                        _select_tool_prompt = self.select_tool_prompt
                    if tool_list:
                        _tool_list = tool_list
                    else:
                        _tool_list = self.tool_list
                    _chart_sample = select_tool(
                        question=question,
                        model=self.model,
                        prompt_list=_select_tool_prompt,
                        tool_list=_tool_list,
                        rollback_num=rollback_num
                    )
                    if not _chart_sample.status:
                        _chart_sample.output = self.tool_list[0]()
                else:
                    _chart_sample = ''
                prompt = BasePromptFlow.formatted_list(
                    prompt_list=_chart_prompt,
                    question=question,
                    # query=_results.output['sql'],
                    result=str(_results.output['table'][:qa_result_num]),
                    chart=_chart_sample.output
                )
                _chart_body = self.valid(
                    prompt_list=prompt,
                    data=_results.output['table'],
                    rollback_num=rollback_num
                )
                _results.output['chart'] = _chart_body.output
                _results.status = _chart_body.status
            return _results
        else:
            _results.error = "**SQL generate fail**\n" + runnable_results.error
            logger.info("ChatDB chart generate SQL fail...")
            return _results

    def valid(self, prompt_list: list, data, rollback_num: int = 5, callback: str = ""):
        results = OutputFormat()
        results.output = ""
        if rollback_num:
            prompt = prompt_list.copy()
            if callback:
                prompt.insert(len(prompt), callback)
            prompt = BasePromptFlow.formatted_str(prompt, sep='\n\n')
            answer = self.model.invoke(prompt)
            answer = answer if isinstance(answer, str) else answer.content
            runnable_answer = ActionParse.codeblock(command=answer, formatter='python')
            if runnable_answer.status:
                try:
                    runnable_answer.output = runnable_answer.output[0]
                    locals().update({'result': data})
                    body = runnable_answer.output
                    exec(body + "\n_a=func(result)", globals(), locals())
                    results.output = locals().get('_a', {})
                    results.status = True
                    logger.info("ChatDB chart run python successful ...")
                    return results
                except Exception as e:
                    results.error = str(e)
                    logging.info(f'Run python error，RollBack：{e}')
                    return self.valid(
                        prompt_list=prompt_list,
                        data=data,
                        rollback_num=rollback_num - 1,
                        callback=RollBackAction._python(body=results.output, error=results.error)
                    )
            else:
                results.error = runnable_answer.error
                logging.info(f'Generate python error，RollBack：{results.error}')
                return self.valid(
                    prompt_list=prompt_list,
                    data=data,
                    rollback_num=rollback_num - 1,
                    callback=RollBackAction._python(body=results.output, error=results.error)
                )
        else:
            return results


class ChatTable(ChatDB):
    """和表格（csv,excel,txt,...）聊天，用于结构化数据问答
    """

    def __init__(self,
                 model,
                 table_paths: List[str] or str,
                 include_table_column_comments: Optional[Dict[str, Dict]] = None
                 ):
        """初始化参数

        ## input
            - model，大语言模型，必选
            - table_paths，list/str，数据表的路径，必选
            - include_table_column_comments，Dict[str, Dict]，需要包含哪些字段及字段含义，
                例子：{'表名1': {"name": "", "columns": {'字段1':'字段1含义','字段2':'字段2含义'}}, '表名2': {}，可选
        """
        logger.info("ChatTable init ...")
        import pandas as pd
        self.model = model
        self.table_infos = {}
        self.dfs = {}
        self.include_table_column_comments = include_table_column_comments
        if isinstance(table_paths, str):
            table_paths = [table_paths]
        for path in table_paths:
            if os.path.exists(path) and os.path.isfile(path):
                base_name, ext = os.path.splitext(path)
                ext = ext.lower()
                if ext == '.csv':
                    df = pd.read_csv(path)
                elif ext == '.txt':
                    # Assuming TXT files are CSV-like, but this can be adjusted
                    df = pd.read_csv(path, delimiter='\t' if '\t' in open(path).readline() else ',')
                elif ext == '.xlsx' or ext == '.xls':
                    df = pd.read_excel(path)
                else:
                    raise ValueError(f"Unsupported file format: {ext}")
                table_name = TableConnector.sanitize_table_name(os.path.basename(path).split('.')[0])
                table_columns = list(df.columns)
                self.dfs[table_name] = df
                self.table_infos[table_name] = dict(zip(table_columns, [''] * len(table_columns)))
                logger.info(f"{path} Load complete...")
            else:
                raise FileNotFoundError(f"File not found: {path}")
        # self.db = TableConnector(env=globals().update(self.dfs))
        ChatDB.__init__(self,
                        model=self.model,
                        init_db=TableConnector(env=globals().update(self.dfs))
                        )
        self.include_tables = self.table_infos
        self.include_columns = self.include_table_column_comments


class TableConnector(object):
    def __init__(self, env=None):
        self.env = env
        if self.env is None:
            self.env = globals()
        from pandasql import sqldf
        self.pysqldf = lambda q: sqldf(q, self.env)

    @classmethod
    def run(cls, command: str) -> OutputFormat:
        logger.info("ChatTable SQL: " + command)
        results = OutputFormat()
        results.output = None
        try:
            df = TableConnector(TableConnector().env).pysqldf(command)
            dict_from_df = df.to_dict(orient='split')
            results.output = dict_from_df['data']
            results.output.insert(0, list(dict_from_df['columns']))
            results.status = True
            return results
        except Exception as e:
            results.error = str(e)
            logger.error(f"ChatTable SQL: {e}")
            return results

    def extract_db_type(self):
        return 'SQLite'  # SQLite MySQL

    @classmethod
    def get_table_describe(cls, origin_, input_):
        column_comtents = ''
        for table_name, values in origin_.items():
            columns_dict = {}
            table_describe = ''
            if input_ and input_.get(table_name, False):
                columns_dict = {key: input_[table_name]["columns"][key] for key in
                                list(input_[table_name]["columns"].keys()) if key in list(values.keys())}
                table_describe = input_[table_name].get('name', False)
                if table_describe:
                    table_describe = f"({table_describe})"
            else:
                columns_dict = values
            # '数据库名称为{db_name},
            column_comtents += (f"表{table_describe}:{table_name}': 字段名" +
                                str(columns_dict).replace(' ', '') + '\n')
        return column_comtents

    @classmethod
    def sanitize_table_name(cls, name):
        """Sanitize the table name to be SQL compliant."""
        # Replace non-alphanumeric characters with underscores
        sanitized = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
        # Remove leading digits or underscores
        sanitized = ''.join(c for i, c in enumerate(sanitized) if c.isalpha() or (c == '_' and i > 0))
        return sanitized
