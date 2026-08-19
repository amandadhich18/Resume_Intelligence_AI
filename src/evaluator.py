import json
import re
from pathlib import Path


# ==========================================
# LOAD EVALUATION DATASET
# ==========================================

def load_evaluation_dataset(
    dataset_path="evaluation/evaluation_dataset.json"
):
    """
    Load evaluation questions from JSON file.
    """

    path = Path(dataset_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {dataset_path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================
# NORMALIZE TEXT
# ==========================================

def normalize_text(text):
    """
    Normalize text for comparison.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# KEYWORD EVALUATION
# ==========================================

def evaluate_keywords(
    answer,
    expected_keywords
):
    """
    Check how many expected keywords
    appear in the generated answer.
    """

    normalized_answer = normalize_text(answer)

    matched_keywords = []
    missing_keywords = []

    for keyword in expected_keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        if normalized_keyword in normalized_answer:

            matched_keywords.append(keyword)

        else:

            missing_keywords.append(keyword)

    total = len(expected_keywords)

    if total == 0:
        score = 100.0

    else:
        score = (
            len(matched_keywords)
            / total
        ) * 100

    return {
        "score": round(score, 2),
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords
    }


# ==========================================
# RETRIEVAL EVALUATION
# ==========================================

def evaluate_retrieval(
    retrieved_chunks,
    expected_section
):
    """
    Check whether the expected resume section
    was retrieved.
    """

    retrieved_sections = [
        chunk.get("section", "")
        for chunk in retrieved_chunks
    ]

    expected = normalize_text(
        expected_section
    )

    normalized_sections = [
        normalize_text(section)
        for section in retrieved_sections
    ]

    section_found = (
        expected in normalized_sections
    )

    return {
        "section_found": section_found,
        "retrieved_sections": retrieved_sections
    }


# ==========================================
# SINGLE QUESTION EVALUATION
# ==========================================

def evaluate_question(
    question_data,
    agent
):
    """
    Evaluate one question using the Resume Agent.
    """

    question = question_data["question"]

    expected_answer = question_data[
        "expected_answer"
    ]

    expected_section = question_data[
        "expected_section"
    ]

    keywords = question_data[
        "keywords"
    ]

    # --------------------------------------
    # Run agent
    # --------------------------------------

    result = agent.answer_question(
        question
    )

    generated_answer = result[
        "answer"
    ]

    retrieved_chunks = result[
        "sources"
    ]

    # --------------------------------------
    # Evaluate answer
    # --------------------------------------

    keyword_result = evaluate_keywords(
        generated_answer,
        keywords
    )

    # --------------------------------------
    # Evaluate retrieval
    # --------------------------------------

    retrieval_result = evaluate_retrieval(
        retrieved_chunks,
        expected_section
    )

    # --------------------------------------
    # Final result
    # --------------------------------------

    return {
        "question": question,
        "expected_answer": expected_answer,
        "generated_answer": generated_answer,
        "keyword_score": keyword_result["score"],
        "matched_keywords": keyword_result[
            "matched_keywords"
        ],
        "missing_keywords": keyword_result[
            "missing_keywords"
        ],
        "retrieval_success": retrieval_result[
            "section_found"
        ],
        "retrieved_sections": retrieval_result[
            "retrieved_sections"
        ]
    }


# ==========================================
# FULL EVALUATION
# ==========================================

def evaluate_agent(
    agent,
    dataset_path="evaluation/evaluation_dataset.json"
):
    """
    Evaluate the Resume Agent on the complete
    evaluation dataset.
    """

    dataset = load_evaluation_dataset(
        dataset_path
    )

    results = []

    for question_data in dataset:

        print(
            "\n"
            + "=" * 60
        )

        print(
            "QUESTION:",
            question_data["question"]
        )

        result = evaluate_question(
            question_data,
            agent
        )

        results.append(result)

        print(
            "Keyword Score:",
            result["keyword_score"],
            "%"
        )

        print(
            "Retrieval Success:",
            result["retrieval_success"]
        )

    # ======================================
    # CALCULATE METRICS
    # ======================================

    total_questions = len(results)

    if total_questions == 0:
        return {
            "total_questions": 0,
            "average_keyword_score": 0,
            "retrieval_accuracy": 0,
            "results": []
        }

    average_keyword_score = (
        sum(
            result["keyword_score"]
            for result in results
        )
        / total_questions
    )

    successful_retrievals = sum(
        1
        for result in results
        if result["retrieval_success"]
    )

    retrieval_accuracy = (
        successful_retrievals
        / total_questions
    ) * 100

    # ======================================
    # FINAL REPORT
    # ======================================

    report = {
        "total_questions": total_questions,
        "average_keyword_score": round(
            average_keyword_score,
            2
        ),
        "retrieval_accuracy": round(
            retrieval_accuracy,
            2
        ),
        "results": results
    }

    return report


# ==========================================
# SAVE EVALUATION RESULTS
# ==========================================

def save_evaluation_results(
    report,
    output_path="evaluation/evaluation_results.json"
):
    """
    Save evaluation report as JSON.
    """

    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nEvaluation report saved to: {output_path}"
    )