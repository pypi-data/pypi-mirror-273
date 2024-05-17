from dfapp.base.models.model import LCModelComponent
from dfapp.field_typing import BaseLanguageModel


class SimpleGeneratorComponent(LCModelComponent):
    display_name = "Simple Generator"
    description = "Generate responses using a model and output text data."

    def build_config(self):
        return {"model": {"display_name": "Model", "info": "Input BaseLanguageModel.", "required": True}}

    def build(self, text: str, model: BaseLanguageModel) -> str:
        return self.get_chat_result(model, False, text)
