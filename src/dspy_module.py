import os

import dspy
from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file"
    )


# ==========================================
# DSPy + GROQ CONFIGURATION
# ==========================================

lm = dspy.LM(
    "groq/openai/gpt-oss-20b",
    api_key=GROQ_API_KEY
)

dspy.configure(lm=lm)


# ==========================================
# DSPy SIGNATURE
# ==========================================

class ResumeQuestionAnswer(dspy.Signature):
    """
    Answer a question using only the supplied
    resume context.
    """

    resume_context = dspy.InputField(
        desc="Relevant information retrieved from the resume"
    )

    question = dspy.InputField(
        desc="User's question about the resume"
    )

    answer = dspy.OutputField(
        desc="Clear and concise answer based only on the resume context"
    )


# ==========================================
# DSPy MODULE
# ==========================================

class ResumeDSPyModule(dspy.Module):

    def __init__(self):
        super().__init__()

        self.answer_question = dspy.Predict(
            ResumeQuestionAnswer
        )

    def forward(self, resume_context, question):

        result = self.answer_question(
            resume_context=resume_context,
            question=question
        )

        return result.answer