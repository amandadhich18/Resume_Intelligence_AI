from src.mcp_server import (
    extract_job_description_skills,
    match_resume_with_job,
    analyze_resume_skill_gap
)


print("=" * 60)
print("MCP TOOL TEST")
print("=" * 60)


# ==========================================
# TEST 1 — JD SKILL EXTRACTION
# ==========================================

jd_text = """
We are looking for a Data Analyst with Python,
SQL, Power BI, Excel and Tableau experience.
"""

print("\nTEST 1: JD SKILL EXTRACTION")

jd_skills = extract_job_description_skills(
    jd_text
)

print("Extracted skills:")
print(jd_skills)


# ==========================================
# TEST 2 — RESUME ↔ JD MATCHING
# ==========================================

print("\nTEST 2: RESUME ↔ JD MATCHING")

resume_skills = [
    "Python",
    "SQL",
    "Power BI",
    "Excel"
]

match_result = match_resume_with_job(
    resume_skills,
    jd_skills
)

print("Match result:")
print(match_result)


# ==========================================
# TEST 3 — SKILL GAP ANALYSIS
# ==========================================

print("\nTEST 3: SKILL GAP ANALYSIS")

gap_result = analyze_resume_skill_gap(
    match_result["matched_skills"],
    match_result["missing_skills"],
    match_result["match_percentage"]
)

print("Skill gap result:")
print(gap_result)


print("\n" + "=" * 60)
print("MCP TOOL TEST COMPLETED")
print("=" * 60)