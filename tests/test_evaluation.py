import sys
from pathlib import Path


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ==========================================
# IMPORTS
# ==========================================

from src.text_cleaner import (
    extract_and_clean_pdf
)

from src.chunker import (
    create_section_chunks
)

from src.embeddings import (
    load_embedding_model,
    generate_embeddings
)

from src.agent import ResumeAgent

from src.evaluator import (
    evaluate_agent,
    save_evaluation_results
)


# ==========================================
# CONFIGURATION
# ==========================================

PDF_PATH = (
    "Data/Resume/Aman_Dadhich_Resume.pdf"
)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print("=" * 60)
    print("RESUME INTELLIGENCE AI")
    print("EVALUATION PIPELINE")
    print("=" * 60)


    # --------------------------------------
    # LOAD RESUME
    # --------------------------------------

    print("\nLoading resume...")

    text = extract_and_clean_pdf(
        PDF_PATH
    )

    chunks = create_section_chunks(
        text
    )

    print(
        f"Resume sections: {len(chunks)}"
    )


    # --------------------------------------
    # LOAD EMBEDDING MODEL
    # --------------------------------------

    print("\nLoading embedding model...")

    model = load_embedding_model()


    # --------------------------------------
    # CREATE EMBEDDINGS
    # --------------------------------------

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
        "Embedding shape:",
        embeddings.shape
    )


    # --------------------------------------
    # CREATE AGENT
    # --------------------------------------

    print("\nCreating Resume Agent...")

    agent = ResumeAgent(
        chunks,
        embeddings,
        model
    )

    print(
        "✅ Resume Agent created successfully"
    )


    # --------------------------------------
    # RUN EVALUATION
    # --------------------------------------

    print(
        "\nStarting evaluation..."
    )

    report = evaluate_agent(
        agent
    )


    # --------------------------------------
    # DISPLAY FINAL REPORT
    # --------------------------------------

    print("\n")
    print("=" * 60)
    print("FINAL EVALUATION REPORT")
    print("=" * 60)

    print(
        "\nTotal Questions:",
        report["total_questions"]
    )

    print(
        "Average Keyword Score:",
        f"{report['average_keyword_score']}%"
    )

    print(
        "Retrieval Accuracy:",
        f"{report['retrieval_accuracy']}%"
    )


    # --------------------------------------
    # DISPLAY INDIVIDUAL RESULTS
    # --------------------------------------

    print("\n")
    print("=" * 60)
    print("QUESTION RESULTS")
    print("=" * 60)

    for index, result in enumerate(
        report["results"],
        start=1
    ):

        print(
            f"\n{index}. "
            f"{result['question']}"
        )

        print(
            "Keyword Score:",
            f"{result['keyword_score']}%"
        )

        print(
            "Retrieval:",
            "PASS"
            if result["retrieval_success"]
            else "FAIL"
        )

        print(
            "Generated Answer:",
            result["generated_answer"]
        )


    # --------------------------------------
    # SAVE REPORT
    # --------------------------------------

    save_evaluation_results(
        report
    )


    print("\n")
    print("=" * 60)
    print("EVALUATION COMPLETED")
    print("=" * 60)