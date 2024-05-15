import enum


class EmbeddingModel(enum.Enum):
    """
    Enum for supported embedding models. Used to specify the model used to generate embeddings for document and text indices.
    """

    ROBERTA = "roberta"
    SENTENCE_TRANSFORMER = "sentence_transformer"
