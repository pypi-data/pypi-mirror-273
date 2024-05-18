from typing import Optional, Dict, List

from pinecone.config.config import OpenApiConfiguration, Config
from pinecone.core.client.api.inference_api import InferenceApi
from pinecone.core.client.model.embeddings_inputs import EmbeddingsInputs
from pinecone.core.client.model.inline_object import InlineObject
from pinecone.inference.build_parameters_dict_for_inference import build_parameters_dict_for_inference
from pinecone.utils import setup_openapi_client

from pinecone.models import EmbeddingsList 

from pinecone.interfaces import PineconePlugin

class Embeddings(PineconePlugin):
    """
    The `Embeddings` class configures and utilizes the Pinecone Inference API to generate embeddings.

    :param config: A `pinecone.config.Config` object, configured and built in the Pinecone class.
    :type config: `pinecone.config.Config`, required

    :param openapi_config: A `pinecone.config.openapi.OpenApiConfiguration` object, configured and built in the
    Pinecone class.
    :type openapi_config: `pinecone.config.openapi.OpenApiConfiguration`, required

    :param pool_threads: Number of threads to use for the connection pool, as declared in the Pinecone class.
    :type pool_threads: int, required (but optional in the Pinecone class)
    """

    def __init__(self, plugin_client_builder, config: Config):
        self.config = config
        self.inference_api = plugin_client_builder(InferenceApi)

    def create(
        self, model: str, inputs: List[str], parameters: Optional[Dict[str, str]] = None, async_req=False
    ) -> EmbeddingsList:
        """
        Generates embeddings for the provided inputs using the specified model and (optional) parameters.

        :param model: The model to use for generating embeddings.
        :type model: str, required

        :param inputs: A list of items to generate embeddings for.
        :type inputs: list, required

        :param parameters: A dictionary of parameters to use when generating embeddings.
        :type parameters: dict, optional

        :param async_req: If True, the method will return a list of futures that can be used to retrieve the results.
        :type async_req: bool, optional

        :return: EmbeddingsList object with keys `data`, `model`, and `usage`. The `data` key contains a list of
        `n` embeddings, where `n` = len(inputs) and type(n) = Embedding. Precision of returned embeddings is either 
        int16 or int32, with int32 being the default. `model` key is the model used to generate the embeddings. 
        `usage` key contains the total number of tokens used at request-time.

        Example:
        >>> in = ["Who created the first computer?"]
        >>> out = (...).create(model="multilingual-e5-large", inputs=input, parameters={"input_type": "query", "truncate": "END"})
        >>> print(out)
         [{'data': [{'index': 0, 'values': [0.2, 0.1, ...]}],
         'model': 'multilingual-e5-large',
         'usage': {'total_tokens': 15}
         }]
        """
        embeddings_inputs = [EmbeddingsInputs(text=i) for i in inputs]

        if parameters:
            embeddings_parameters = build_parameters_dict_for_inference(parameters)
            inline_objects = InlineObject(model=model, inputs=embeddings_inputs, parameters=embeddings_parameters)
        else:
            inline_objects = InlineObject(
                model=model,
                inputs=embeddings_inputs,
            )

        embeddings_list = self.inference_api.generate_embeddings(inline_object=inline_objects, async_req=async_req)
        return EmbeddingsList(embeddings_list=embeddings_list)
