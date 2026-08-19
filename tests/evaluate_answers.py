# ==========================================
# PHASE 4 - ANSWER QUALITY & HALLUCINATION
# EVALUATION
# ==========================================

from src.text_cleaner import extract_and_clean_pdf
from src.chunker import create_section_chunks
from src.embeddings import load_embedding_model, generate_embeddings
from src.retriever import retrieve_chunks
from src.generator import generate_answer

from tests.evaluation_questions import EVALUATION_QUESTIONS


# ==========================================
# CONFIGURATION
# ==========================================

PDF_PATH = "Data/Resume/Aman_Dadhich_Resume.pdf"

TOP_K = 3

REFUSAL_PHRASE = "I could not find this information in the resume."


# ==========================================
# LOAD RESUME
# ==========================================

print("=" * 60)
print("PHASE 4 - ANSWER QUALITY & HALLUCINATION EVALUATION")
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

texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(
    model,
    texts
)

print(f"Embedding shape: {embeddings.shape}")


# ==========================================
# EVALUATION COUNTERS
# ==========================================

answerable_total = 0
answerable_correct = 0

unanswerable_total = 0
hallucination_safe = 0


# ==========================================
# RUN QUESTIONS
# ==========================================

for number, item in enumerate(
    EVALUATION_QUESTIONS,
    start=1
):

    question = item["question"]
    question_type = item["type"]

    print("\n" + "=" * 60)
    print(f"QUESTION {number}")
    print("=" * 60)

    print(f"\nQuestion: {question}")
    print(f"Type: {question_type}")


    # ======================================
    # RETRIEVAL
    # ======================================

    retrieved_chunks = retrieve_chunks(
        question,
        chunks,
        embeddings,
        model,
        top_k=TOP_K
    )


    print("\nRetrieved sections:")

    for chunk in retrieved_chunks:

        print(
            f"- {chunk['section']} "
            f"(score: {chunk['score']:.4f})"
        )


    # ======================================
    # GROQ ANSWER
    # ======================================

    print("\nGenerating answer...")

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    print("\nAnswer:")
    print(answer)


    # ======================================
    # ANSWERABLE QUESTION
    # ======================================

    if question_type == "answerable":

        answerable_total += 1

        # Basic validation:
        # The answer should NOT be the refusal response.

        if (
            answer.strip()
            and REFUSAL_PHRASE.lower()
            not in answer.lower()
        ):

            answerable_correct += 1

            print("\nResult: PASS")

        else:

            print("\nResult: FAIL")


    # ======================================
    # UNANSWERABLE QUESTION
    # ======================================

    elif question_type == "unanswerable":

        unanswerable_total += 1

        # For information that isn't in the resume,
        # the chatbot should refuse instead of inventing it.

        if REFUSAL_PHRASE.lower() in answer.lower():

            hallucination_safe += 1

            print("\nResult: SAFE - No hallucination")

        else:

            print("\nResult: WARNING - Possible hallucination")


# ==========================================
# CALCULATE METRICS
# ==========================================

if answerable_total > 0:

    answer_accuracy = (
        answerable_correct /
        answerable_total
    )

else:

    answer_accuracy = 0


if unanswerable_total > 0:

    hallucination_safety = (
        hallucination_safe /
        unanswerable_total
    )

else:

    hallucination_safety = 0


# ==========================================
# FINAL RESULTS
# ==========================================

print("\n")
print("=" * 60)
print("FINAL ANSWER QUALITY RESULTS")
print("=" * 60)

print(
    f"\nAnswerable questions : "
    f"{answerable_total}"
)

print(
    f"Answerable passed    : "
    f"{answerable_correct}"
)

print(
    f"Answer accuracy      : "
    f"{answer_accuracy:.2%}"
)

print(
    f"\nUnanswerable questions : "
    f"{unanswerable_total}"
)

print(
    f"Safe refusals          : "
    f"{hallucination_safe}"
)

print(
    f"Hallucination safety   : "
    f"{hallucination_safety:.2%}"
)

print("\nEvaluation completed.")