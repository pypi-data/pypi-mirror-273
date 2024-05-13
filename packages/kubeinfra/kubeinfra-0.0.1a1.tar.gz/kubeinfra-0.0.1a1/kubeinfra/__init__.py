import os
import sys
import urllib.parse
from typing import Type

from .version import VERSION


version = VERSION

user_agent = f"KubeInfraPythonOfficial/{version}"

api_key = os.environ.get("KUBEINFRA_API_KEY", None)

# api_base = "http://127.0.0.1:8000/"
api_base = "http://45.120.216.143:13811/"
api_base_openai = urllib.parse.urljoin(api_base, "/v1")
api_base_complete = urllib.parse.urljoin(api_base, "/v1/chat/completions")
api_base_files = urllib.parse.urljoin(api_base, "/v1/files/")
api_base_finetune = urllib.parse.urljoin(api_base, "/v1/fine-tunes/")
api_base_instances = urllib.parse.urljoin(api_base, "instances/")
api_base_embeddings = urllib.parse.urljoin(api_base, "api/v1/embeddings")

print("############")
default_text_model = "mistralai/Mistral-7B-Instruct-v0.2"
default_image_model = "runwayml/stable-diffusion-v1-5"
default_embedding_model = "kubeinfracomputer/bert-base-uncased"
log_level = "WARNING"

MISSING_API_KEY_MESSAGE = """KUBEINFRA_API_KEY not found.
Please set it as an environment variable or set it as kubeinfra.api_key
Find your KUBEINFRA_API_KEY at https://api.kubeinfra.xyz/settings/api-keys"""

MAX_CONNECTION_RETRIES = 2
BACKOFF_FACTOR = 0.2

min_samples = 100

from .complete import AsyncComplete, Complete, Completion
from .embeddings import Embeddings
from .error import *
from .files import Files
from .finetune import Finetune
from .image import Image
from .models import Models


class KubeInfra:
    complete: Type[Complete]
    completion: Type[Completion]
    embeddings: Type[Embeddings]
    files: Type[Files]
    finetune: Type[Finetune]
    image: Type[Image]
    models: Type[Models]

    def __init__(
        self,
    ) -> None:
        self.complete = Complete
        self.completion = Completion
        self.embeddings = Embeddings
        self.files = Files
        self.finetune = Finetune
        self.image = Image
        self.models = Models


__all__ = [
    "api_key",
    "api_base",
    "api_base_complete",
    "api_base_files",
    "api_base_finetune",
    "api_base_instances",
    "api_base_embeddings",
    "default_text_model",
    "default_image_model",
    "default_embedding_model",
    "Models",
    "Complete",
    "Completion",
    "AsyncComplete",
    "Files",
    "Finetune",
    "Image",
    "Embeddings",
    "MAX_CONNECTION_RETRIES",
    "MISSING_API_KEY_MESSAGE",
    "BACKOFF_FACTOR",
    "min_samples",
    "KubeInfra",
]
