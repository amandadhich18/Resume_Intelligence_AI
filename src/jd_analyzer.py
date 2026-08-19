import os
from groq import Groq


def analyze_resume_jd(resume_text, jd_text):
    """
    Analyze a resume against a job description using Groq LLM.
    """

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""
You are an expert technical recruiter and resume analyst.

Analyze the candidate's resume against the job description.

========================
CANDIDATE RESUME
========================
{resume_text}

========================
JOB DESCRIPTION
========================
{jd_text}

========================
TASK
========================

Provide a structured analysis containing:

1. Overall Candidate Fit
   - Give a percentage from 0 to 100.
   - Briefly explain the score.

2. Candidate Strengths
   - Identify the strongest skills and experience
     relevant to the job description.

3. Skill Gaps
   - Identify important skills from the job description
     that are missing or weak in the resume.

4. Resume Improvement Suggestions
   - Suggest specific areas the candidate could improve.
   - Do not invent experience or skills.

5. Interview Preparation
   - Suggest important technical areas the candidate
     should prepare for based on the job description.

6. Final Recommendation
   - Strong Fit
   - Good Fit
   - Partial Fit
   - Low Fit

Important rules:

- Use ONLY information present in the resume and job description.
- Do not invent experience, projects, companies, education,
  certifications, or skills.
- Clearly distinguish between skills that are present and
  skills that are missing.
- Keep the analysis practical and concise.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content