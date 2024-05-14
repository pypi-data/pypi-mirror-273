import logging
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, cast


class AgentAction(object):
    def __init__(self):
        pass


class RollBackAction(object):
    """回滚执行
    """
    @classmethod
    def base(cls, desc=None, body=None, error=None, **kwargs):
        from pylmkit.core.base import BasePromptFlow
        _desc = "Please reply based on the information provided and in conjunction with the error message below" if not desc else desc
        _body = "Last SQL Query: {body}"
        _error = "Error message: {error}"
        prompt = BasePromptFlow.formatted_list([_desc, _body, _error],
                                               desc=desc,
                                               body=body,
                                               error=error.replace('\n', ' ')
                                               )
        return BasePromptFlow.formatted_str(prompt)

    @classmethod
    def sql(cls, desc=None, body=None, error=None, **kwargs):
        from pylmkit.core.base import BasePromptFlow
        _desc = ("Please run the following SQL statement and error message, combined with user problems to make SQL "
                "corrections and generate the correct SQL statement:") if not desc else desc
        _body = "Last SQL Query: {body}"
        _error = "Error message: {error}"
        prompt = BasePromptFlow.formatted_list([_desc, _body, _error],
                                               desc=desc,
                                               body=body.replace('\n', ' '),
                                               error=error.replace('\n', ' ')
                                               )
        return BasePromptFlow.formatted_str(prompt)

    @classmethod
    def _python(cls, desc=None, body=None, error=None, **kwargs):
        from pylmkit.core.base import BasePromptFlow
        _desc = "Correct and regenerate the Python code based on the provided content and error messages:" if not desc else desc
        _body = '''Last python code:
```python
{body}
```'''
        _error = "Error message: {error}"
        prompt = BasePromptFlow.formatted_list([_desc, _body, _error],
                                               desc=desc,
                                               body=body,
                                               error=error.replace('\n', ' ')
                                               )
        return BasePromptFlow.formatted_str(prompt)



