import json
import mlflow


print("=" * 60)
print("RESUME INTELLIGENCE AI")
print("MLFLOW EXPERIMENT TRACKING")
print("=" * 60)


# ==========================================
# 1. MLFLOW SETUP
# ==========================================

mlflow.set_tracking_uri("sqlite:///mlflow.db")

mlflow.set_experiment(
    "Resume_Intelligence_AI"
)


# ==========================================
# 2. LOAD EVALUATION RESULTS
# ==========================================

print("\nLoading evaluation results...")

with open(
    "evaluation/evaluation_results.json",
    "r",
    encoding="utf-8"
) as f:

    evaluation_data = json.load(f)


results = evaluation_data["results"]

print(
    f"Total evaluation questions: {len(results)}"
)


# ==========================================
# 3. START MLFLOW RUN
# ==========================================

with mlflow.start_run(
    run_name="resume_agent_evaluation"
):

    print("\nMLflow run started...")


    # ======================================
    # 4. LOG PARAMETERS
    # ======================================

    mlflow.log_param(
        "total_questions",
        evaluation_data["total_questions"]
    )


    mlflow.log_param(
        "evaluation_type",
        "Resume QA Evaluation"
    )


    # ======================================
    # 5. LOG OVERALL METRICS
    # ======================================

    mlflow.log_metric(
        "average_keyword_score",
        evaluation_data["average_keyword_score"]
    )


    mlflow.log_metric(
        "retrieval_accuracy",
        evaluation_data["retrieval_accuracy"]
    )


    # ======================================
    # 6. CALCULATE ANSWER SUCCESS
    # ======================================

    answerable_questions = 0
    successful_answers = 0


    for result in results:

        answerable_questions += 1

        if result.get("keyword_score", 0) >= 50:

            successful_answers += 1


    answer_success_rate = (
        successful_answers /
        answerable_questions
    ) * 100


    mlflow.log_metric(
        "answer_success_rate",
        answer_success_rate
    )


    # ======================================
    # 7. RETRIEVAL SUCCESS RATE
    # ======================================

    retrieval_successes = sum(
        1
        for result in results
        if result.get("retrieval_success") is True
    )


    retrieval_success_rate = (
        retrieval_successes /
        len(results)
    ) * 100


    mlflow.log_metric(
        "retrieval_success_rate",
        retrieval_success_rate
    )


    # ======================================
    # 8. LOG INDIVIDUAL QUESTION METRICS
    # ======================================

    for index, result in enumerate(results, start=1):

        mlflow.log_metric(
            f"question_{index}_keyword_score",
            result.get("keyword_score", 0)
        )


    # ======================================
    # 9. DISPLAY RESULTS
    # ======================================

    print("\n" + "=" * 60)
    print("MLFLOW RUN RESULTS")
    print("=" * 60)

    print(
        f"\nAverage Keyword Score: "
        f"{evaluation_data['average_keyword_score']}%"
    )

    print(
        f"Retrieval Accuracy: "
        f"{evaluation_data['retrieval_accuracy']}%"
    )

    print(
        f"Answer Success Rate: "
        f"{answer_success_rate:.2f}%"
    )

    print(
        f"Retrieval Success Rate: "
        f"{retrieval_success_rate:.2f}%"
    )

    print(
        f"\nQuestions tracked: "
        f"{len(results)}"
    )


print("\n" + "=" * 60)
print("MLFLOW TRACKING COMPLETED")
print("=" * 60)

print("\nExperiment:")
print("Resume_Intelligence_AI")

print("\nTracking database:")
print("mlflow.db")