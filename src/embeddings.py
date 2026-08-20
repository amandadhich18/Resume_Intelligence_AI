import numpy as np
from fastembed import TextEmbedding


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load the FastEmbed embedding model.
    """
    model = TextEmbedding(
        model_name=MODEL_NAME
    )

    return model


def generate_embeddings(model, texts):
    """
    Convert text chunks into normalized embedding vectors.
    """
    embeddings = list(
        model.embed(texts)
    )

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    # Normalize embeddings
    norms = np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )

    norms[norms == 0] = 1.0

    embeddings = embeddings / norms

    return embeddings
