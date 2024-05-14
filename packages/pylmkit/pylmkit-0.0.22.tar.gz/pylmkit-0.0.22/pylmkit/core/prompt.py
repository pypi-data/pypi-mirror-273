from datetime import datetime


def input_prompt(**kwargs):
    return kwargs


def return_language(language='English'):
    return f"\nReply in {language}"


def get_summary_default_prompt():
    _prompt = "提取下面内容的摘要：\n\ncontent: {content}"
    return _prompt


sql_prompt = [
    """你是一个{dbtype}数据库专家，你需要根据给定一个输入问题和所提供的信息，思考并生成语法正确的{dbtype}语法。
永远不要查询表中的所有列。您必须只查询回答问题所需的列。注意，只使用您可以在下面的表中看到的列名。注意不要查询不存在的列。另外，要注意哪个列在哪个表中。"""+f"当前日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}。",
    """使用以下格式:
```sql
SELECT col1 FROM database.table WHERE col2 = 'Jacky'
```""",
    """注意，如果用户问题涉及多表关联查询，则需要多表关联查询，例如:
```sql
SELECT pi.name
FROM tabel1 AS pi
INNER JOIN tabel2 AS pm ON pi.id = pm.id
WHERE pm.age = 26;
```""",
    """只使用以下表格:
{table_info}""",
    """Question: {question}""",

]

table_list_prompt = """当用户问题适合使用Table显示时，使用下面格式返回```python\ncode\n```：
- question: 蔡文姬负责的项目清单情况
- result: "result=[('member_name','project_name'),('蔡文姬','智能体研究'),('蔡文姬','知识库问答')]"
注意result[0]是字段名称，result[1:]才是对应的数据。
```python
def func(result):
    dict_data = {
      "type": "Table",
      "table_title": "蔡文姬负责的项目清单",
      "table_desc": "该表格展示蔡文姬所负责的项目名称清单",
      "table_values": [dict(zip(result[0], i)) for i in result[1:]]
    }
    return dict_data
```
"""

text_answer_prompt = """当用户问题不涉及Chart,Table等，适合直接用文本回答和罗列内容时，使用下面格式返回```python\ncode\n```：
- question: 小明哪一年出生？
- result: "result=[('date','name'),('2001','小明')]"
注意result[0]是字段名称，result[1:]才是对应的数据。
```python
def func(result):
    dict_data = {
      "type": "Text",
      "question": "小明哪一年出生？",
      "answer": "小明出生于2001年。"
    }
    return dict_data
```
"""

sql_qa_prompt = [
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
]

chart_prompt = [
    '''根据用户问题和提供的结果，以下面格式生成答案，生成格式如下样例所示：
{chart}
>>>如果上面样例不适合，则默认使用文本回答生成答案，使用下面格式返回```python\ncode\n```：
''' + f"{text_answer_prompt}",
    '''- question: {question}
- result: "result={result}"
注意result[0]是字段名称，result[1:]才是对应的数据。
```python

```
''',

]

line_chart_prompt = """当用户问题适合使用BarChart、LineChart,ScatterChart显示时，使用下面格式返回```python\ncode\n```：
- question: 每年的学生教师数量以及趋势情况
- result: "result=[('year','student','teacher'),(2023,1000,120),(2024,120,130)]"
注意result[0]是字段名称，result[1:]才是对应的数据。
```python
def func(result):
    dict_data = {
        "type": "{type}",
        "chart_title": "每年的学生教师数量",
        "chart_desc": "该图表将显示学生教师每年的变化趋势，有助于直观反映在不同年份的增长情况。",
        "chart_values": {
            "x_name": "年份",
            "y_name": "数量",
            "x_labels": [str(i[0]) for i in result[1:]],  # x轴标签，格式：[str, str, ...]
            "datasets": [
                {
                    "label": "学生",  # 数据集的标签
                    "data": [i[1] for i in result[1:]]  # y轴数据点
                },
                {
                    "label": "教师",  # 数据集的标签
                    "data": [i[2] for i in result[1:]]  # y轴数据点
                }
            ]
        },
    }
    return dict_data
```
"""

pie_chart_prompt = """当用户问题适合使用PieChart,FunnelChart显示时，使用下面格式返回```python\ncode\n```：
- question: 学生性别比例
- result: "result=[('gender', 'count', 'rate'),('男性', 1500, 0.6),('女性',1000, 0.4)]"
注意result[0]是字段名称，result[1:]才是对应的数据。
```python
def func(result):
    dict_data = {
      "type": "{type}", 
      "chart_title": "学生性别比例",  
      "chart_desc": "该图表将显示学生性别比例情况，有助于直观反映学生性别平衡性。",  
      "labels": [str(i[0]) for i in result[1:]],  # 格式：[str, str, ...]
      "values": [i[1] for i in result[1:]]  # 根据result情况可自适应生成列表
    }
    return dict_data
```
"""

select_tool_prompt = [
    "根据用户问题和提供的结果进行深度思考，思考该问题适合使用哪种工具类型。",
    "你只能从下面给出的工具类型中选择最合适用户问题的工具：\n{tool}",
    "例如用户问题是'每一年学生数量'，那么此时应该选择`line_chart()`，你只需要返回 '<tool>工具类型</tool>' 即可，不需要做其他解释和回答，如：\n<tool>line_chart()</tool>",
    "question: {question}"
]
