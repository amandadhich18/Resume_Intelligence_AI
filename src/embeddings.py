import numpy as np
from fastembed import TextEmbedding


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load a lightweight ONNX embedding model.
    """
    model = TextEmbedding(
        model_name=MODEL_NAME
    )

    return model


def _normalize(vector):
    """
    L2 normalize a vector.
    """
    vector = np.asarray(
        vector,
        dtype=np.float32
    )

    norm = np.linalg.norm(vector)

    if norm == 0:
        return vector

    return vector / norm


def generate_embeddings(model, texts):
    """
    Convert text chunks into normalized embedding vectors.
    """
    embeddings = list(
        model.embed(texts)
    )

    embeddings = np.asarray(
        [
            _normalize(vector)
            for vector in embeddings
        ],
        dtype=np.float32
    )

    return embeddings


def generate_query_embedding(model, query):
    """
    Generate one normalized query embedding.
    """
    embedding = next(
        model.query_embed(query)
    )

    return _normalize(embedding)
