import functools
import logging
import multiprocessing
import sys
from io import StringIO
from typing import Dict, Optional
from pydantic import Field, BaseModel
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, cast

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )
logger = logging.getLogger(__name__)


class PythonExecutor(object):
    def __init__(self):
        pass

    @classmethod
    def run(cls, command: str):
        logger.warning("Python REPL can execute arbitrary code. Use with caution.")
        results = {'output': None, "status": False, "error": ''}
        if '```python' in command and '```' in command:
            command = str(command).split(f'```{command}')[1].split('```')[0]
        try:
            exec(command, globals(), locals())
            results['output'] = globals()['report_folder']
            results['status'] = True
        except Exception as e:
            results['error'] = str(e)
        return results

    @classmethod
    def run_mysql(cls, connect, code_text):
        results = {'output': {"data": None, "columns": []}, "status": False, "error": None}
        with connect.cursor() as cursor:
            try:
                # 执行SQL语句
                cursor.execute(code_text)
                results['output']['columns'] = [i[0] for i in cursor.description]
                # 获取所有记录列表
                results['output']['data'] = list(cursor.fetchall())
                results['status'] = True
            except Exception as e:
                results['error'] = str(e)
        return results


class Executor(object):
    def __init__(self):
        pass

    def runnable(self, executor, max_rollback_num: int = 5):
        results = {"status": False, "error": None, 'output': []}
        try:
            if max_rollback_num:
                respond = executor
                if respond['status']:
                    pass
                else:
                    results['error'] = respond.get('error', '')
                    logging.info(f'Generate {str(executor)} error，RollBack...')
                    return self.runnable()
            else:
                return results
        except Exception as e:
            # 这里可以添加更详细的错误处理逻辑
            logger.error("BaseChartRunnable runnable Fail: " + str(e))
            results['error'] = str(e)
            return results


class PythonREPL(BaseModel):
    """运行python代码"""
    globals: Optional[Dict] = Field(default_factory=dict, alias="_globals")
    locals: Optional[Dict] = Field(default_factory=dict, alias="_locals")

    def worker(
            self,
            command: str,
            globals: Optional[Dict],
            locals: Optional[Dict],
            queue: multiprocessing.Queue,
    ):
        results = {'output': "", "status": False, "error": None}
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, globals, locals)
            sys.stdout = old_stdout
            queue.put(mystdout.getvalue())
            results['status'] = True
            results['output'] = globals.get('report_folder', "")
            return results
        except Exception as e:
            sys.stdout = old_stdout
            queue.put(repr(e))
            results['error'] = str(e)
            return results

    def run(self, command: str, timeout: Optional[int] = None) -> str:
        """Run command with own globals/locals and returns anything printed.
        Timeout after the specified number of seconds."""

        # Warn against dangers of PythonREPL
        logger.warning("Python REPL can execute arbitrary code. Use with caution.")

        queue: multiprocessing.Queue = multiprocessing.Queue()

        # Only use multiprocessing if we are enforcing a timeout
        if timeout is not None:
            # create a Process
            p = multiprocessing.Process(
                target=self.worker, args=(command, self.globals, self.locals, queue)
            )
            # start it
            p.start()
            # wait for the process to finish or kill it after timeout seconds
            p.join(timeout)
            if p.is_alive():
                p.terminate()
                return "Execution timed out"
        else:
            return self.worker(command, self.globals, self.locals, queue)
        # get the result from the worker function
        return queue.get()
