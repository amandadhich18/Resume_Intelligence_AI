# ==========================================
# PHASE 4 - IMPROVED RETRIEVAL EVALUATION
# BASELINE VS IMPROVED RAG
# ==========================================

from src.text_cleaner import extract_and_clean_pdf
from src.chunker import create_section_chunks
from src.embeddings import load_embedding_model, generate_embeddings

from tests.evaluation_questions import EVALUATION_QUESTIONS

import numpy as np


# ==========================================
# CONFIGURATION
# ==========================================

PDF_PATH = "Data/Resume/Aman_Dadhich_Resume.pdf"
TOP_K = 3


# ==========================================
# LOAD RESUME
# ==========================================

print("=" * 60)
print("PHASE 4 - IMPROVED RETRIEVAL EVALUATION")
print("=" * 60)

print("\nLoading resume...")

text = extract_and_clean_pdf(PDF_PATH)
chunks = create_section_chunks(text)

print(f"Resume sections: {len(chunks)}")


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

print("\nLoading embedding model...")

model = load_embedding_model()

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = generate_embeddings(
    model,
    texts
)

print(f"Embedding shape: {embeddings.shape}")


# ==========================================
# SECTION KEYWORDS
# ==========================================

SECTION_KEYWORDS = {

    "EDUCATION": [
        "education",
        "educational",
        "degree",
        "qualification",
        "bachelor",
        "master",
        "college",
        "university",
        "graduation"
    ],

    "PROJECTS": [
        "project",
        "projects",
        "dashboard",
        "built",
        "developed",
        "created"
    ],

    "PROFESSIONAL EXPERIENCE": [
        "experience",
        "work",
        "worked",
        "job",
        "company",
        "employer",
        "employment",
        "currently",
        "role",
        "position"
    ],

    "TECHNICAL SKILLS": [
        "skill",
        "skills",
        "technical",
        "programming",
        "database",
        "sql",
        "python",
        "tools",
        "technology",
        "technologies",
        "visualization"
    ],

    "CERTIFICATIONS": [
        "certification",
        "certifications",
        "certificate",
        "certificates",
        "credential"
    ],

    "PROFESSIONAL SUMMARY": [
        "summary",
        "background",
        "professional background",
        "profile"
    ]
}


# ==========================================
# CREATE QUERY EMBEDDING
# ==========================================

def get_query_embedding(query, model):

    return model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]


# ==========================================
# BASELINE RETRIEVAL
# ==========================================

def baseline_retrieval(
    query,
    chunks,
    embeddings,
    model,
    top_k=3
):

    query_embedding = get_query_embedding(
        query,
        model
    )

    scores = np.dot(
        embeddings,
        query_embedding
    )

    indexes = np.argsort(
        scores
    )[::-1][:top_k]

    return [
        chunks[index]["section"]
        for index in indexes
    ]


# ==========================================
# IMPROVED RETRIEVAL
# ==========================================

def improved_retrieval(
    query,
    chunks,
    embeddings,
    model,
    top_k=3
):

    query_embedding = get_query_embedding(
        query,
        model
    )

    semantic_scores = np.dot(
        embeddings,
        query_embedding
    )

    final_scores = semantic_scores.copy()

    query_lower = query.lower()

    # --------------------------------------
    # SECTION-AWARE BOOST
    # --------------------------------------

    for index, chunk in enumerate(chunks):

        section = chunk["section"]

        keywords = SECTION_KEYWORDS.get(
            section,
            []
        )

        matches = 0

        for keyword in keywords:

            if keyword in query_lower:
                matches += 1

        if matches > 0:

            final_scores[index] += (
                0.05 * matches
            )

    indexes = np.argsort(
        final_scores
    )[::-1][:top_k]

    return [
        chunks[index]["section"]
        for index in indexes
    ]


# ==========================================
# METRICS
# ==========================================

def calculate_recall_at_1(results):

    correct = 0
    total = len(results)

    for result in results:

        expected = result["expected_sections"]
        retrieved = result["retrieved"]

        if not expected:
            continue

        if retrieved[0] in expected:
            correct += 1

    return correct / total if total else 0


def calculate_recall_at_3(results):

    correct = 0
    total = len(results)

    for result in results:

        expected = result["expected_sections"]
        retrieved = result["retrieved"]

        if not expected:
            continue

        if any(
            section in expected
            for section in retrieved
        ):
            correct += 1

    return correct / total if total else 0


def calculate_mrr(results):

    reciprocal_ranks = []

    for result in results:

        expected = result["expected_sections"]
        retrieved = result["retrieved"]

        rank = 0

        for position, section in enumerate(
            retrieved,
            start=1
        ):

            if section in expected:

                rank = position
                break

        if rank > 0:
            reciprocal_ranks.append(
                1 / rank
            )
        else:
            reciprocal_ranks.append(0)

    return (
        sum(reciprocal_ranks)
        / len(reciprocal_ranks)
        if reciprocal_ranks
        else 0
    )


# ==========================================
# EVALUATION
# ==========================================

baseline_results = []
improved_results = []


print("\n")
print("=" * 60)
print("EVALUATING RETRIEVAL")
print("=" * 60)


question_number = 0


for item in EVALUATION_QUESTIONS:

    # Only evaluate answerable questions
    if item["type"] != "answerable":
        continue

    question_number += 1

    question = item["question"]

    expected = item["expected_sections"]


    # ======================================
    # BASELINE
    # ======================================

    baseline = baseline_retrieval(
        question,
        chunks,
        embeddings,
        model,
        TOP_K
    )


    # ======================================
    # IMPROVED
    # ======================================

    improved = improved_retrieval(
        question,
        chunks,
        embeddings,
        model,
        TOP_K
    )


    # ======================================
    # SAVE RESULTS
    # ======================================

    baseline_results.append({

        "question": question,

        "expected_sections": expected,

        "retrieved": baseline

    })


    improved_results.append({

        "question": question,

        "expected_sections": expected,

        "retrieved": improved

    })


    # ======================================
    # DISPLAY
    # ======================================

    print("\n" + "-" * 60)

    print(
        f"QUESTION {question_number}"
    )

    print(
        f"Question: {question}"
    )

    print(
        f"Expected: {expected}"
    )

    print(
        f"Baseline : {baseline}"
    )

    print(
        f"Improved : {improved}"
    )


# ==========================================
# BASELINE METRICS
# ==========================================

baseline_recall_1 = calculate_recall_at_1(
    baseline_results
)

baseline_recall_3 = calculate_recall_at_3(
    baseline_results
)

baseline_mrr = calculate_mrr(
    baseline_results
)


# ==========================================
# IMPROVED METRICS
# ==========================================

improved_recall_1 = calculate_recall_at_1(
    improved_results
)

improved_recall_3 = calculate_recall_at_3(
    improved_results
)

improved_mrr = calculate_mrr(
    improved_results
)


# ==========================================
# FINAL COMPARISON
# ==========================================

print("\n")
print("=" * 60)
print("BASELINE VS IMPROVED RAG")
print("=" * 60)

print(
    "\nMetric              Baseline       Improved"
)

print("-" * 60)

print(
    f"Recall@1            "
    f"{baseline_recall_1:.2%}          "
    f"{improved_recall_1:.2%}"
)

print(
    f"Recall@3            "
    f"{baseline_recall_3:.2%}         "
    f"{improved_recall_3:.2%}"
)

print(
    f"MRR                 "
    f"{baseline_mrr:.2%}         "
    f"{improved_mrr:.2%}"
)


# ==========================================
# IMPROVEMENT
# ==========================================

print("\n")
print("=" * 60)
print("IMPROVEMENT")
print("=" * 60)

print(
    f"\nRecall@1 improvement: "
    f"{improved_recall_1 - baseline_recall_1:+.2%}"
)

print(
    f"Recall@3 improvement: "
    f"{improved_recall_3 - baseline_recall_3:+.2%}"
)

print(
    f"MRR improvement: "
    f"{improved_mrr - baseline_mrr:+.2%}"
)


print("\nEvaluation completed.")