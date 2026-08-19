# ==========================================
# PHASE 4 - RETRIEVAL EVALUATION
# ==========================================

from src.text_cleaner import extract_and_clean_pdf
from src.chunker import create_section_chunks
from src.embeddings import load_embedding_model, generate_embeddings
from src.retriever import retrieve_chunks

from tests.evaluation_questions import EVALUATION_QUESTIONS


# ==========================================
# CONFIGURATION
# ==========================================

PDF_PATH = "Data/Resume/Aman_Dadhich_Resume.pdf"

TOP_K = 3


# ==========================================
# LOAD RESUME
# ==========================================

print("=" * 50)
print("PHASE 4 - RAG RETRIEVAL EVALUATION")
print("=" * 50)

print("\nLoading resume...")

text = extract_and_clean_pdf(PDF_PATH)

chunks = create_section_chunks(text)

print(f"Resume sections: {len(chunks)}")


# ==========================================
# CREATE EMBEDDINGS
# ==========================================

print("\nLoading embedding model...")

model = load_embedding_model()

texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(model, texts)

print(f"Embedding shape: {embeddings.shape}")


# ==========================================
# EVALUATION VARIABLES
# ==========================================

recall_at_1 = 0
recall_at_3 = 0

reciprocal_ranks = []


# ==========================================
# RUN EVALUATION
# ==========================================

print("\n")
print("=" * 50)
print("EVALUATING QUESTIONS")
print("=" * 50)


for number, item in enumerate(EVALUATION_QUESTIONS, start=1):

    question = item["question"]
    expected_sections = item["expected_sections"]

    print("\n" + "-" * 50)
    print(f"QUESTION {number}")
    print("-" * 50)

    print(f"Question: {question}")

    print(f"Expected: {expected_sections}")

    retrieved = retrieve_chunks(
        question,
        chunks,
        embeddings,
        model,
        top_k=TOP_K
    )

    retrieved_sections = [
        chunk["section"]
        for chunk in retrieved
    ]

    print(f"Retrieved: {retrieved_sections}")


    # ======================================
    # CHECK TOP 1
    # ======================================

    top_1_correct = (
        retrieved_sections[0] in expected_sections
    )

    if top_1_correct:
        recall_at_1 += 1


    # ======================================
    # CHECK TOP 3
    # ======================================

    top_3_correct = any(
        section in expected_sections
        for section in retrieved_sections
    )

    if top_3_correct:
        recall_at_3 += 1


    # ======================================
    # CALCULATE RECIPROCAL RANK
    # ======================================

    reciprocal_rank = 0

    for rank, section in enumerate(
        retrieved_sections,
        start=1
    ):

        if section in expected_sections:

            reciprocal_rank = 1 / rank

            break

    reciprocal_ranks.append(reciprocal_rank)


# ==========================================
# FINAL METRICS
# ==========================================

total_questions = len(EVALUATION_QUESTIONS)

recall_at_1_score = recall_at_1 / total_questions

recall_at_3_score = recall_at_3 / total_questions

mrr_score = sum(reciprocal_ranks) / total_questions


# ==========================================
# RESULTS
# ==========================================

print("\n")
print("=" * 50)
print("RAG RETRIEVAL EVALUATION RESULTS")
print("=" * 50)

print(f"\nTotal questions : {total_questions}")

print(
    f"Recall@1        : {recall_at_1_score:.2%}"
)

print(
    f"Recall@3        : {recall_at_3_score:.2%}"
)

print(
    f"MRR             : {mrr_score:.2%}"
)

print("\nEvaluation completed.")