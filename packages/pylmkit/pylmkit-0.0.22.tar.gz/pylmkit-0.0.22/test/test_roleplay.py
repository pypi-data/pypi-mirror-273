# main.py
from pylmkit import BaseWebUI
from dotenv import load_dotenv
from pylmkit.app import RolePlay
from pylmkit.llms import ChatOpenAI
from pylmkit.memory import MemoryHistoryLength
from pylmkit.llms import ChatQianfan


load_dotenv()
web = BaseWebUI(language='zh')  # 中文网站


model = ChatQianfan(model="ERNIE-Bot-turbo")
memory = MemoryHistoryLength(memory_length=web.param(label="记忆长度", type='int', value=500),  # 添加页面交互参数
                             streamlit_web=True
                            )
role_template = "{memory}\n 请为我推荐{query}的{topic}"
rp = RolePlay(
    role_template=role_template,  # 角色模板
    llm_model=model,  # 大语言模型
    memory=memory,  # 记忆
    # online_search_kwargs={},
    online_search_kwargs={'topk': 2, 'timeout': 20},  # 搜索引擎配置，不开启则可以设置为 online_search_kwargs={}
    return_language="中文"
)

web.run(
    obj=rp.invoke,
    input_param=[{"name": "query", "label": "地点", "type": "chat"},
                 {"name": "topic", "label": "主题", "type": "text"},
                 ],
    output_param=[{'label': '结果', 'name': 'response', 'type': 'chat'},
                  {'label': '参考', 'name': 'refer', 'type': 'refer'}
                  ]
)


