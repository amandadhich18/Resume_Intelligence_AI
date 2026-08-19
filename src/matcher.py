def match_skills(resume_skills, jd_skills):
    """
    Compare resume skills with job description skills.
    """

    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    jd_set = {
        skill.lower()
        for skill in jd_skills
    }

    matched = sorted(
        resume_set.intersection(jd_set)
    )

    missing = sorted(
        jd_set - resume_set
    )

    if len(jd_set) > 0:
        match_percentage = (
            len(matched) / len(jd_set)
        ) * 100
    else:
        match_percentage = 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": round(
            match_percentage,
            2
        )
    }