from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load the sentence-transformer embedding model.
    """
    model = SentenceTransformer(MODEL_NAME)

    return model


def generate_embeddings(model, texts):
    """
    Convert text chunks into embedding vectors.
    """
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings