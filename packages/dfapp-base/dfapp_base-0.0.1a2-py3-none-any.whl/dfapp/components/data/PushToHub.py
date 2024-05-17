from dfapp.interface.custom.custom_component import CustomComponent
from datasets import DatasetDict


class PushToHubComponent(CustomComponent):
    display_name = "Push Dataset to HuggingFace Hub"
    description = "Pushes a dataset to the Hugging Face Hub."

    def build_config(self):
        return {
            "dataset_name": {"display_name": "Dataset Name", "info": "Name of the dataset to push."},
            "huggingface_token": {
                "display_name": "Hugging Face Token",
                "password": True,
                "info": "Token for Hugging Face API authentication.",
                "required": True,
            },
        }

    def build(self, dataset: DatasetDict, dataset_name: str, huggingface_token: str):
        dataset.push_to_hub(dataset_name, token=huggingface_token)
