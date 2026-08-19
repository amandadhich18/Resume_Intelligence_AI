def analyze_skill_gap(match_result):
    """
    Analyze matched and missing skills from JD matching result.
    """

    matched_skills = match_result.get("matched_skills", [])
    missing_skills = match_result.get("missing_skills", [])
    match_percentage = match_result.get("match_percentage", 0)

    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills == 0:
        coverage = "No skills detected"
    elif match_percentage >= 80:
        coverage = "Strong Match"
    elif match_percentage >= 60:
        coverage = "Good Match"
    elif match_percentage >= 40:
        coverage = "Moderate Match"
    else:
        coverage = "Low Match"

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "coverage": coverage,
        "total_skills": total_skills
    }