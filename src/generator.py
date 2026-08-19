import os

from dotenv import load_dotenv
from groq import Groq


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
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ==========================================
# GENERATE ANSWER
# ==========================================

def generate_answer(
    query,
    retrieved_chunks,
    chat_history=None
):
    """
    Generate an answer using Groq based only
    on retrieved resume information.

    chat_history allows the model to understand
    previous conversation context.
    """

    # --------------------------------------
    # Build resume context
    # --------------------------------------

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"""
SECTION: {chunk['section']}
SOURCE: {chunk['source']}

CONTENT:
{chunk['text']}
"""
        )

    context = "\n".join(context_parts)


    # --------------------------------------
    # Build conversation history
    # --------------------------------------

    history_text = ""

    if chat_history:

        history_parts = []

        for message in chat_history:

            role = message["role"]
            content = message["content"]

            history_parts.append(
                f"{role.upper()}: {content}"
            )

        history_text = "\n".join(history_parts)


    # --------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------

    system_prompt = """
You are Resume Intelligence AI.

Your job is to answer questions about a candidate's
resume using ONLY the information provided in the
resume context.

IMPORTANT RULES:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not present in the resume context,
   say exactly:

   "I could not find this information in the resume."

4. Use previous conversation context to understand
   follow-up questions.

5. If the user says:
   - "he"
   - "his"
   - "that project"
   - "the first project"
   - "that company"
   - "there"

   use the conversation history to understand what
   they are referring to.

6. Give clear and concise answers.

7. If the question asks for a list, use numbered
   or bullet points.

8. Do not mention retrieval, embeddings, vectors,
   prompts, or internal system details.
"""


    # --------------------------------------
    # USER PROMPT
    # --------------------------------------

    user_prompt = f"""
CONVERSATION HISTORY:

{history_text}


RESUME CONTEXT:

{context}


CURRENT QUESTION:

{query}


Answer the current question using the resume
context and conversation history.
"""


    # --------------------------------------
    # GROQ REQUEST
    # --------------------------------------

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.1,

        max_tokens=500
    )


    # --------------------------------------
    # RETURN ANSWER
    # --------------------------------------

    return response.choices[0].message.content.strip()