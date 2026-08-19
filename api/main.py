from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from src.agent import ResumeAgent
from src.text_cleaner import extract_and_clean_pdf
from src.chunker import create_section_chunks
from src.embeddings import load_embedding_model, generate_embeddings


# ==========================================
# CONFIGURATION
# ==========================================

PDF_PATH = "Data/Resume/Aman_Dadhich_Resume.pdf"


# ==========================================
# APPLICATION LIFESPAN
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading Resume Intelligence AI pipeline...")

    text = extract_and_clean_pdf(PDF_PATH)

    chunks = create_section_chunks(text)

    print(f"Resume sections: {len(chunks)}")

    print("Loading embedding model...")

    model = load_embedding_model()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        model,
        texts
    )

    print(f"Embedding shape: {embeddings.shape}")

    app.state.agent = ResumeAgent(
        chunks=chunks,
        embeddings=embeddings,
        model=model
    )

    app.state.ready = True

    print("Resume Intelligence AI API ready.")

    yield

    app.state.ready = False

    print("Resume Intelligence AI API shutting down.")


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Resume Intelligence AI API",
    description="API for asking questions about a resume",
    version="1.0.0",
    lifespan=lifespan
)


# ==========================================
# REQUEST MODEL
# ==========================================

class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Question about the resume"
    )


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():

    return {
        "status": "ok",
        "message": "Resume Intelligence AI API is running"
    }


# ==========================================
# HEALTH ENDPOINT
# ==========================================

@app.get("/health")
def health(request: Request):

    ready = getattr(
        request.app.state,
        "ready",
        False
    )

    return {
        "status": "healthy" if ready else "starting",
        "model_ready": ready
    }


# ==========================================
# RESUME QUESTION ANSWERING
# ==========================================

@app.post("/ask")
def ask_resume(
    request: QuestionRequest,
    http_request: Request
):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    agent = getattr(
        http_request.app.state,
        "agent",
        None
    )

    if agent is None:

        raise HTTPException(
            status_code=503,
            detail="Resume Intelligence AI is not ready."
        )

    try:

        result = agent.answer_question(
            question
        )

        return {
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as exc:

        print(
            f"Error while answering question: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to process the question."
        ) from exc