import logging
from pylmkit.tools import tool
from pylmkit.tools.parse import OutputFormat, ActionParse
from pylmkit.tools.action import RollBackAction
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )
logger = logging.getLogger(__name__)


def python_executor(var, code, **kwargs):
    exec(f"{var}={code}", **kwargs)
    return locals().get(f'{var}', None)


def select_tool(question, model, prompt_list: list, tool_list: list, rollback_num: int = 5, callback: str = ""):
    _results = OutputFormat()
    _results.output = None
    if rollback_num:
        _prompt_list = prompt_list.copy()
        if callback:
            _prompt_list.insert(len(_prompt_list), callback)
        from pylmkit.core.base import BasePromptFlow
        tool_content = '\n'.join([tool(i).all for i in tool_list])
        for i in tool_list:  # 注册变量
            globals().update({tool(i).name: i})
        _prompt = BasePromptFlow.formatted_list(
            prompt_list=_prompt_list,
            tool=tool_content,
            question=question,
        )
        _prompt = BasePromptFlow.formatted_str(_prompt, sep='\n\n')
        try:
            _response = model.invoke(_prompt)
            _response = _response if isinstance(_response, str) else _response.content
            response = ActionParse.xml(_response, formatter='tool')
            logger.info(f"Chart output modal：{response.output[0]}")
            if response.status and python_executor('aaa', response.output[0]):
                _results.output = python_executor('aaa', response.output[0])
                _results.status = True
                return _results
            else:
                return select_tool(
                    question=question,
                    model=model,
                    prompt_list=prompt_list,
                    rollback_num=rollback_num - 1,
                    tool_list=tool_list,
                    callback=RollBackAction.base(body=_response, error=response.error)
                )
        except Exception as e:
            _results.error = str(e)
            return select_tool(
                question=question,
                model=model,
                prompt_list=prompt_list,
                rollback_num=rollback_num-1,
                tool_list=tool_list,
                callback=RollBackAction.base(body=_results.output, error=_results.error)
            )
    else:
        return _results


