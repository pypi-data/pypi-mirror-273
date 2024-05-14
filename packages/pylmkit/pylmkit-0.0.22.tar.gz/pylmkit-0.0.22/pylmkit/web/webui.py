import sqlparse
import time, logging, os
import uuid, glob
import pandas as pd
import streamlit as st
from pylmkit.core.base import BaseWebUI
import pyecharts.options as opts
from pyecharts.charts import *
from streamlit_echarts import st_pyecharts


def read_md(folder_path, file_type='*.md'):
    markdown_text = ''
    # 使用glob模式匹配所有.md文件
    try:
        md_files = glob.glob(os.path.join(folder_path, file_type))
        # 遍历所有找到的Markdown文件
        for md_file in md_files:
            # 读取Markdown文件内容
            with open(md_file, 'r', encoding='utf-8') as file:
                markdown_text += file.read()
    except Exception as e:
        logger.error(e)
    return markdown_text


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',  # 定义日期格式
                    )
logger = logging.getLogger(__name__)


class RAGWebUI(BaseWebUI):
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
        super().__init__(
            title=title,
            page_icon=page_icon,
            layout=layout,
            language=language,
            sidebar_title=sidebar_title,
            sidebar_describe=sidebar_describe,
            footer_describe=footer_describe,
            logo1=logo1,
            logo2=logo2,
            greetings=greetings,
            placeholder=placeholder,
            refer_name=refer_name
        )


class ChatDBWebUI(BaseWebUI):
    def __init__(self,
                 language='zh',
                 avatar_input="😄",
                 avatar_output="🤖",
                 layout='wide',
                 **kwargs
                 ):

        super().__init__(language=language, layout=layout, **kwargs)
        self.avatar_output = avatar_output
        st.sidebar.title('ChatDBAgent')
        st.sidebar.markdown("与你的结构化数据聊天：支持主流数据库、表格型excel等数据！")
        if language in ['zh', '中文']:
            # self.tabs = ["图表", '数据集', "数据库", '日志']
            self.tabs = ["Report", "Chart", 'Data', "SQL", 'Log']
            self.spinner_report_text = "PyLMKit：报告生成中，请稍候..."
        else:
            self.tabs = ["Report", "Chart", 'Data', "SQL", 'Log']
            self.spinner_report_text = "PyLMKit: Report generation, please wait..."

        if "chart_messages" not in st.session_state:
            st.session_state["chart_messages"] = []
        for msg in st.session_state.chart_messages:
            if msg.get("content", False):
                st.chat_message(msg["role"], avatar=avatar_input).write(msg["content"])
            else:
                self.chart_output(msg, review=True)
            # refer setting
            refer = msg.get("refer", False)
            if refer:
                with st.expander(label=self.refer_name, expanded=False):
                    st.markdown(refer, unsafe_allow_html=True)

    def chart_output(self, chart_data: dict, refer=None, role="assistant", review=False):
        if not isinstance(chart_data, dict):
            chart_data = chart_data.output
        if not chart_data.get('role', False):
            chart_data.update({"role": role})
        else:
            role = chart_data.get('role')

        content = chart_data.get('analysis', '暂无分析描述')  # question analysis
        with st.chat_message(chart_data.get('role', role), avatar=self.avatar_output):
            # 分析描述
            content_placeholder = st.empty()
            full_content = ""
            for chunk in str(content):
                full_content += chunk + ""
                time.sleep(0.01)
                content_placeholder.markdown(full_content + "▌")
            content_placeholder.markdown(full_content)
            # tabs
            if chart_data.get('chart', False) and chart_data['chart']['type'] in ['LineChart', 'BarChart', 'ScatterChart', 'PieChart', 'FunnelChart']:
                Chart_tab, DataFrame_tab, SQL_tab, Log_tab = st.tabs(self.tabs[1:])
                with Chart_tab:
                    chart_plot = chart_data['chart']
                    chart_type = {"LineChart": Line(), "BarChart": Bar(), "ScatterChart": Scatter(),
                                  "PieChart": Pie(), "FunnelChart": Funnel()
                                  }
                    if chart_plot['type'] in ['LineChart', 'BarChart', 'ScatterChart']:
                        c = (
                            chart_type[chart_plot['type']]
                            .add_xaxis(chart_plot['chart_values']['x_labels'])
                            .set_global_opts(
                                title_opts=opts.TitleOpts(title=chart_plot['chart_title'], subtitle=chart_plot['chart_desc'], padding=[5, 10]),  # 标题设置
                                yaxis_opts=opts.AxisOpts(
                                    name=chart_plot['chart_values']['y_name'],
                                    name_location='middle',  # 将Y轴名称放置在中间
                                    name_gap=80,  # 调整名称与轴之间的距离
                                    # position="right"  # Y轴名称在右侧
                                ),  # Y轴名称设置
                                xaxis_opts=opts.AxisOpts(name=chart_plot['chart_values']['x_name']),  # X轴名称设置
                                toolbox_opts=opts.ToolboxOpts(is_show=True),
                            )
                        )
                        for i in chart_plot['chart_values']['datasets']:
                            c.add_yaxis(i['label'], i['data'])
                        st_pyecharts(
                            c,
                            height="500px",
                            width="100%",
                            key=str(uuid.uuid4())
                        )
                    elif chart_plot['type'] == 'PieChart':
                        c = (
                            chart_type[chart_plot['type']]
                            .add("", [list(z) for z in zip(chart_plot['labels'], chart_plot['values'])])
                            .set_global_opts(
                                title_opts=opts.TitleOpts(title=chart_plot['chart_title'],
                                                          subtitle=chart_plot['chart_desc'], padding=[5, 10]),  # 标题设置
                                toolbox_opts=opts.ToolboxOpts(is_show=True),
                            )
                        )
                        st_pyecharts(
                            c,
                            height="500px",
                            width="100%",
                            key=str(uuid.uuid4())
                        )
                    elif chart_plot['type'] == 'FunnelChart':
                        c = (
                            chart_type[chart_plot['type']]
                            .add("", [list(z) for z in zip(chart_plot['labels'], chart_plot['values'])])
                            .set_global_opts(
                                title_opts=opts.TitleOpts(title=chart_plot['chart_title'],
                                                          subtitle=chart_plot['chart_desc'], padding=[5, 10]),  # 标题设置
                                toolbox_opts=opts.ToolboxOpts(is_show=True),
                            )
                        )
                        st_pyecharts(
                            c,
                            height="500px",
                            width="100%",
                            key=str(uuid.uuid4())
                        )
            else:
                DataFrame_tab, SQL_tab, Log_tab = st.tabs(self.tabs[2:])
            with SQL_tab:
                st.code(
                    f"""
                    {sqlparse.format(chart_data.get('sql', ''), reindent=True, keyword_case='upper')}
                    """, language='sql'
                )
            with DataFrame_tab:
                st.markdown("""默认展示前10条记录，查看全部记录请到`[SQL]->[Run]`""",
                            unsafe_allow_html=True)
                table_data = list(chart_data.get('table', []))
                if table_data:
                    df = pd.DataFrame(
                        data=table_data[1:],
                        columns=table_data[0],
                    )
                    st.dataframe(df, use_container_width=True)
            with Log_tab:
                if not chart_data.get('error', False):
                    st.code('暂无日志', language='text')
                else:
                    st.code(chart_data.get('error', ''), language='text')

            if refer:  # refer setting
                with st.expander(label=self.refer_name, expanded=False):
                    st.markdown(refer, unsafe_allow_html=True)

            # st.write_stream(chart_layout(chart_data))
            # chart_layout(chart_data)
            if not review:
                st.session_state.chart_messages.append(chart_data)

    def chart_run(self, obj, input_param: list[dict]):
        result = super().base_run(obj, input_param, message_type="chart_messages")
        if result:
            self.chart_output(chart_data=result[0])
