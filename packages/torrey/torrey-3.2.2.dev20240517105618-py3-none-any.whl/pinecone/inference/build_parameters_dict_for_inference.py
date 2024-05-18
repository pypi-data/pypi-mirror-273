from pinecone.core.client.model.embeddings_parameters import EmbeddingsParameters


def build_parameters_dict_for_inference(params: dict):
    """
    Builds the parameters dictionary passed to the `pinecone.inference.embeddings.Embeddings.create` method.

    :param params: A dictionary of parameters.
    :type params: dict, required
    """
    if not params.get("input_type") is None and not params.get("truncate") is None:
        return EmbeddingsParameters(input_type=params.get("input_type"), truncate=params.get("truncate"))

    if not params.get("input_type") is None and params.get("truncate") is None:
        return EmbeddingsParameters(input_type=params.get("input_type"))

    if not params.get("truncate") is None and params.get("input_type") is None:
        return EmbeddingsParameters(truncate=params.get("truncate"))
