import os

from src.text_cleaner import extract_and_clean_pdf
from src.chunker import create_section_chunks
from src.embeddings import load_embedding_model, generate_embeddings
from src.retriever import retrieve_chunks
from src.dspy_module import ResumeDSPyModule


# ============================================================
# CONFIGURATION
# ============================================================

PDF_PATH = "Data/Resume/Aman_Dadhich_Resume.pdf"


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("DSPy RESUME QUESTION ANSWERING TEST")
print("=" * 60)


# ============================================================
# LOAD RESUME
# ============================================================

print("\nLoading resume...")

text = extract_and_clean_pdf(PDF_PATH)

chunks = create_section_chunks(text)

print(f"Resume sections: {len(chunks)}")


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

model = load_embedding_model()


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

print("\nCreating embeddings...")

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = generate_embeddings(
    model,
    texts
)

print(
    f"Embedding shape: {embeddings.shape}"
)


# ============================================================
# CREATE DSPy MODULE
# ============================================================

print("\nCreating DSPy module...")

dspy_module = ResumeDSPyModule()

print("✅ DSPy module created successfully")


# ============================================================
# QUESTION
# ============================================================

question = "Where does Aman currently work?"


print("\n" + "-" * 60)
print("QUESTION")
print("-" * 60)

print(question)


# ============================================================
# RETRIEVE RELEVANT RESUME INFORMATION
# ============================================================

print("\nRetrieving relevant resume information...")

retrieved_chunks = retrieve_chunks(
    question,
    chunks,
    embeddings,
    model,
    top_k=3
)


# ============================================================
# BUILD CONTEXT
# ============================================================

context_parts = []

for chunk in retrieved_chunks:

    context_parts.append(
        f"""
SECTION: {chunk['section']}

SOURCE: {chunk['source']}

CONTENT:
{chunk['text']}
"""
    )


resume_context = "\n".join(
    context_parts
)


# ============================================================
# DSPy GENERATION
# ============================================================

print("\nRunning DSPy...")

answer = dspy_module(
    resume_context=resume_context,
    question=question
)


# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 60)
print("DSPy RESULT")
print("=" * 60)

print("\nAnswer:")
print(answer)


# ============================================================
# SOURCES
# ============================================================

print("\n" + "-" * 60)
print("RETRIEVED SOURCES")
print("-" * 60)

for i, chunk in enumerate(
    retrieved_chunks,
    start=1
):

    print(
        f"\nSource {i}: {chunk['section']}"
    )

    print(
        f"Score: {chunk['score']:.4f}"
    )


print("\n" + "=" * 60)
print("DSPy TEST COMPLETED")
print("=" * 60)