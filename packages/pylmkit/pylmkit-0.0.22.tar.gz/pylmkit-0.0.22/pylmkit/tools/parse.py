import re
import ast
import logging
from pylmkit.core.base import BaseAgentParse
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, cast

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(filename)s - %(levelname)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )
logger = logging.getLogger(__name__)


class OutputFormat(object):
    status: bool = False
    error: str = ""
    output = {}

    def __str__(self):
        return f"PyLMKitOutput(status='{self.status}', output={self.output}, error={self.error})"

    @property
    def to_dict(self):
        return {
            'status': self.status,
            'output': self.output,
            'error': self.error
        }


class ActionParse(BaseAgentParse):
    def __init__(self):
        super().__init__()

    @classmethod
    def xml(cls, command, formatter):
        return cls().base(command=command, formatter=formatter, parse_type='xml')

    @classmethod
    def codeblock(cls, command, formatter):
        results = cls().base(command=command, formatter=formatter, parse_type='codeblock')
        results.output = results.output.copy()
        if formatter == 'sql':
            _output = []
            for i in results.output:
                _output.append(i.replace('\n', ' ').strip())
            results.output = _output
        return results

    @classmethod
    def parse_chart(cls, command, result):
        results = {"status": False, "error": None, 'output': []}
        string_dict = command.replace('\t', '').replace('//', '#').strip()
        # try:
        real_dict = ast.literal_eval(string_dict)
        if real_dict['type'] not in ['Table', 'Text']:
            real_dict['values']['labels'] = cls().chart_exec(
                'x',
                real_dict['values']['labels'],
                result
            )
            for k in range(len(real_dict['values']['datasets'])):
                real_dict['values']['datasets'][k]['data'] = cls().chart_exec(
                    f'y{k}',
                    real_dict['values']['datasets'][k]['data'],
                    result
                )
        elif real_dict['type'] == 'Table':
            real_dict['values'] = cls().chart_exec(
                'values',
                real_dict['values'],
                result
            )
        else:
            pass
        results['output'] = real_dict
        results['status'] = True
        # except Exception as e:
        #     raise ValueError(e)
        # results['error'] = str(e)
        return results

    def chart_exec(self, var, body, result):
        exec(f"""{var}={body}""")
        return locals().get(var, [])
