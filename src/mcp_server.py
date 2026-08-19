from mcp.server import MCPServer

from src.jd_parser import extract_jd_skills
from src.matcher import match_skills
from src.skill_gap import analyze_skill_gap


# ==========================================
# CREATE MCP SERVER
# ==========================================

mcp = MCPServer("Resume Intelligence AI")


# ==========================================
# TOOL 1 — EXTRACT JD SKILLS
# ==========================================

@mcp.tool()
def extract_job_description_skills(
    job_description: str
) -> list[str]:
    """
    Extract technical skills from a Job Description.
    """

    return extract_jd_skills(job_description)


# ==========================================
# TOOL 2 — MATCH RESUME WITH JD
# ==========================================

@mcp.tool()
def match_resume_with_job(
    resume_skills: list[str],
    job_description_skills: list[str]
) -> dict:
    """
    Compare resume skills with Job Description skills.
    """

    return match_skills(
        resume_skills,
        job_description_skills
    )


# ==========================================
# TOOL 3 — ANALYZE SKILL GAP
# ==========================================

@mcp.tool()
def analyze_resume_skill_gap(
    matched_skills: list[str],
    missing_skills: list[str],
    match_percentage: float
) -> dict:
    """
    Analyze the candidate's skill gaps.
    """

    match_result = {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }

    return analyze_skill_gap(match_result)


# ==========================================
# SERVER ENTRY POINT
# ==========================================

if __name__ == "__main__":
    mcp.run()