import logging
from . import tool
from functools import partial
from .executor import Executor
from .parse import OutputFormat, ActionParse
from .action import AgentAction, RollBackAction

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)


@tool
def wrapper(fun):
    return partial(fun)


class SQLToolKit(object):
    @classmethod
    def sql_executor(
            cls,
            model,
            prompt_list: list,
            db,
            rollback_num: int = 5,
            connector: dict = {},
            callback: str = ""
    ):
        from decimal import Decimal
        from pylmkit.core.base import BasePromptFlow
        results = OutputFormat()
        results.output = results.output.copy()
        if rollback_num:
            try:
                prompt = prompt_list.copy()
                if callback:
                    prompt.insert(-1, callback)
                prompt = BasePromptFlow.formatted_str(
                        prompt,
                        sep='\n\n'
                    )
                model_respond = model.invoke(prompt)
                model_respond = model_respond if isinstance(model_respond, str) else model_respond.content
                respond = ActionParse.codeblock(model_respond, 'sql')
                if respond.status:
                    respond.output = respond.output[0]  # 取第一个sql
                    results.output['sql'] = respond.output
                    if connector.get('obj', False):
                        connector['kwargs'] = connector.get('kwargs', {})
                        obj = wrapper(connector['obj'])
                        connector['kwargs'].update({"command": respond.output})
                        code_result = obj(**connector['kwargs'])
                        logging.info(f'Use custom connector...')
                    else:
                        code_result = db.run(respond.output)  # sql [(列名),(数值记录)]
                        logging.info(f'Use default connector...')
                    if code_result.status:
                        # results.output['result'] = code_result.output
                        results.output['result'] = [[float(item) if isinstance(item, Decimal) else item for item in row] for row in code_result.output]
                        results.status = True
                        results.error = ''
                        return results
                    else:
                        results.error = code_result.error
                        logging.info(f'Run sql error，RollBack：{results.error}')
                        return cls.sql_executor(
                            model=model,
                            prompt_list=prompt_list,
                            rollback_num=rollback_num - 1,
                            db=db,
                            connector=connector,
                            callback=RollBackAction.sql(body=respond.output, error=results.error)
                        )
                else:
                    results.error = respond.error
                    logging.info(f'Generate sql error，RollBack...')
                    return cls.sql_executor(
                        model=model,
                        prompt_list=prompt_list,
                        rollback_num=rollback_num - 1,
                        db=db,
                        connector=connector,
                        callback=RollBackAction.sql(body=model_respond, error=results.error)
                    )
            except Exception as e:
                logger.info("BaseChartRunnable runnable Fail: " + str(e))
                results.error = str(e)
                return results
        else:
            return results

