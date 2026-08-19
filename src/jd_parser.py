import re


def extract_jd_skills(jd_text):
    """
    Extract commonly used technical skills from a job description.
    """

    skills = [
        "Python",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "Azure SQL",
        "BigQuery",
        "Power BI",
        "Tableau",
        "Looker Studio",
        "Excel",
        "Pandas",
        "NumPy",
        "DAX",
        "Machine Learning",
        "Statistics",
        "Data Analysis",
        "Data Visualization",
        "ETL",
        "Power Query",
        "Azure",
        "AWS",
        "Docker",
        "FastAPI",
        "Git",
        "GitHub",
        "R",
        "Spark",
        "Databricks",
    ]

    jd_lower = jd_text.lower()

    found_skills = []

    for skill in skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, jd_lower):
            found_skills.append(skill)

    return found_skills


def extract_resume_skills(chunks):
    """
    Extract skills from the TECHNICAL SKILLS section
    of the uploaded resume.
    """

    technical_text = ""

    for chunk in chunks:
        if chunk.get("section", "").upper() == "TECHNICAL SKILLS":
            technical_text = chunk.get("text", "")
            break

    if not technical_text:
        return []

    skills = [
        "Python",
        "Pandas",
        "NumPy",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "Azure SQL",
        "BigQuery",
        "Power BI",
        "Tableau",
        "Looker Studio",
        "MicroStrategy",
        "Excel",
        "DAX",
        "Power Query",
    ]

    text_lower = technical_text.lower()

    detected_skills = []

    for skill in skills:
        if skill.lower() in text_lower:
            detected_skills.append(skill)

    return detected_skills