from pylmkit.core.prompt import *
from pylmkit.core.base import BasePromptFlow


class DBPromptFlow(BasePromptFlow):
    @classmethod
    def get_sql_prompt(cls, **kwargs):
        prompt = super().formatted_list(sql_prompt, **kwargs)
        return prompt

    @classmethod
    def get_sql_qa_prompt(cls, **kwargs):
        prompt = super().formatted_list(sql_qa_prompt, **kwargs)
        return prompt

    @classmethod
    def set_rollback(cls) -> list:
        return [
            "\nPlease run the following SQL statement and error message, combined with user problems to make SQL "
            "corrections and generate the correct SQL statement:",
            "Last SQL Query: {result}",
            "Error message: {error}"
        ]




