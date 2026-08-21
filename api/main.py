from contextlib import asynccontextmanager
from pathlib import Path
import shutil

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    UploadFile,
    File
)

from pydantic import BaseModel, Field

from src.agent import ResumeAgent
from src.text_cleaner import extract_and_clean_pdf
from src.chunker import create_section_chunks

from src.embeddings import (
    load_embedding_model,
    generate_embeddings
)

from src.jd_parser import (
    extract_jd_skills,
    extract_resume_skills
)

from src.matcher import match_skills
from src.skill_gap import analyze_skill_gap
from src.jd_analyzer import analyze_resume_jd


# ==========================================
# CONFIGURATION
# ==========================================

DEFAULT_PDF_PATH = Path(
    "Data/Resume/Aman_Dadhich_Resume.pdf"
)

UPLOAD_DIR = Path(
    "Data/Resume/uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# RESUME PROCESSING FUNCTION
# ==========================================

def build_resume_agent(
    pdf_path: Path,
    model
):
    """
    Extract, chunk and embed a resume,
    then create a ResumeAgent.
    """

    print(
        f"Processing resume: {pdf_path.name}"
    )

    # --------------------------------------
    # Extract resume text
    # --------------------------------------

    text = extract_and_clean_pdf(
        str(pdf_path)
    )

    if not text or not text.strip():

        raise ValueError(
            "No readable text was found in the PDF."
        )

    # --------------------------------------
    # Create resume chunks
    # --------------------------------------

    chunks = create_section_chunks(
        text
    )

    if not chunks:

        raise ValueError(
            "No resume sections could be created."
        )

    print(
        f"Resume sections: {len(chunks)}"
    )

    # --------------------------------------
    # Add source filename
    # --------------------------------------

    for chunk in chunks:

        chunk["source"] = pdf_path.name

    # --------------------------------------
    # Generate embeddings
    # --------------------------------------

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        model,
        texts
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    # --------------------------------------
    # Create Resume Agent
    # --------------------------------------

    agent = ResumeAgent(
        chunks=chunks,
        embeddings=embeddings,
        model=model
    )

    return {
        "agent": agent,
        "chunks": chunks,
        "text": text,
        "embeddings": embeddings
    }


# ==========================================
# APPLICATION LIFESPAN
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print(
        "Loading Resume Intelligence AI pipeline..."
    )

    # --------------------------------------
    # Initial application state
    # --------------------------------------

    app.state.ready = False

    app.state.agent = None

    app.state.resume_name = None

    app.state.resume_text = None

    app.state.chunks = None

    app.state.jd_name = None

    app.state.jd_text = None

    # --------------------------------------
    # Load embedding model once
    # --------------------------------------

    print(
        "Loading embedding model..."
    )

    model = load_embedding_model()

    app.state.model = model

    # --------------------------------------
    # Load default resume
    # --------------------------------------

    if DEFAULT_PDF_PATH.exists():

        try:

            result = build_resume_agent(
                DEFAULT_PDF_PATH,
                model
            )

            app.state.agent = result[
                "agent"
            ]

            app.state.chunks = result[
                "chunks"
            ]

            app.state.resume_text = result[
                "text"
            ]

            app.state.resume_name = (
                DEFAULT_PDF_PATH.name
            )

            app.state.ready = True

            print(
                "Default resume loaded successfully."
            )

        except Exception as exc:

            print(
                f"Unable to load default resume: "
                f"{exc}"
            )

    else:

        print(
            "Default resume was not found."
        )

    print(
        "Resume Intelligence AI API ready."
    )

    yield

    app.state.ready = False

    print(
        "Resume Intelligence AI API shutting down."
    )


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Resume Intelligence AI API",
    description=(
        "Upload resumes, ask questions, "
        "and analyze resumes against "
        "Job Descriptions."
    ),
    version="3.0.0",
    lifespan=lifespan
)


# ==========================================
# REQUEST MODEL
# ==========================================

class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description=(
            "Question about the active resume"
        )
    )


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():

    return {
        "status": "ok",
        "message": (
            "Resume Intelligence AI API "
            "is running"
        ),
        "version": "3.0.0"
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

    resume_name = getattr(
        request.app.state,
        "resume_name",
        None
    )

    jd_name = getattr(
        request.app.state,
        "jd_name",
        None
    )

    return {
        "status": (
            "healthy"
            if ready
            else "starting"
        ),
        "model_ready": ready,
        "active_resume": resume_name,
        "active_job_description": jd_name
    }


# ==========================================
# RESUME UPLOAD ENDPOINT
# ==========================================

@app.post("/upload-resume")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...)
):

    # --------------------------------------
    # Validate filename
    # --------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail=(
                "No filename was provided."
            )
        )

    # --------------------------------------
    # Validate PDF
    # --------------------------------------

    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF resumes are supported."
            )
        )

    # --------------------------------------
    # Check embedding model
    # --------------------------------------

    model = getattr(
        request.app.state,
        "model",
        None
    )

    if model is None:

        raise HTTPException(
            status_code=503,
            detail=(
                "Embedding model is not ready."
            )
        )

    # --------------------------------------
    # Create safe filename
    # --------------------------------------

    safe_filename = Path(
        file.filename
    ).name

    pdf_path = (
        UPLOAD_DIR
        / safe_filename
    )

    # --------------------------------------
    # Save uploaded PDF
    # --------------------------------------

    try:

        with pdf_path.open(
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to save uploaded resume."
            )
        ) from exc

    finally:

        await file.close()

    # --------------------------------------
    # Process uploaded resume
    # --------------------------------------

    try:

        result = build_resume_agent(
            pdf_path,
            model
        )

    except Exception as exc:

        if pdf_path.exists():

            pdf_path.unlink()

        print(
            f"Resume processing error: "
            f"{exc}"
        )

        raise HTTPException(
            status_code=400,
            detail=(
                "Unable to process the uploaded "
                "resume PDF."
            )
        ) from exc

    # --------------------------------------
    # Replace active resume
    # --------------------------------------

    request.app.state.agent = result[
        "agent"
    ]

    request.app.state.chunks = result[
        "chunks"
    ]

    request.app.state.resume_text = result[
        "text"
    ]

    request.app.state.resume_name = (
        safe_filename
    )

    request.app.state.ready = True

    # Clear old JD whenever resume changes
    request.app.state.jd_name = None
    request.app.state.jd_text = None

    print(
        f"Active resume changed to: "
        f"{safe_filename}"
    )

    # --------------------------------------
    # Response
    # --------------------------------------

    return {
        "status": "success",
        "message": (
            "Resume uploaded and indexed "
            "successfully."
        ),
        "filename": safe_filename,
        "sections": len(
            result["chunks"]
        ),
        "embedding_dimensions": int(
            result["embeddings"].shape[1]
        )
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
            detail=(
                "Question cannot be empty."
            )
        )

    agent = getattr(
        http_request.app.state,
        "agent",
        None
    )

    resume_name = getattr(
        http_request.app.state,
        "resume_name",
        None
    )

    if agent is None:

        raise HTTPException(
            status_code=503,
            detail=(
                "No resume is currently loaded."
            )
        )

    try:

        result = agent.answer_question(
            question
        )

        return {
            "question": question,
            "resume": resume_name,
            "answer": result[
                "answer"
            ],
            "sources": result[
                "sources"
            ]
        }

    except Exception as exc:

        print(
            f"Error while answering question: "
            f"{exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process "
                "the question."
            )
        ) from exc


# ==========================================
# JOB DESCRIPTION ANALYSIS
# ==========================================

@app.post(
    "/analyze-job-description"
)
async def analyze_job_description(
    request: Request,
    file: UploadFile = File(...)
):

    # --------------------------------------
    # Make sure resume exists
    # --------------------------------------

    resume_text = getattr(
        request.app.state,
        "resume_text",
        None
    )

    chunks = getattr(
        request.app.state,
        "chunks",
        None
    )

    resume_name = getattr(
        request.app.state,
        "resume_name",
        None
    )

    if (
        resume_text is None
        or chunks is None
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Upload a resume before "
                "analyzing a Job Description."
            )
        )

    # --------------------------------------
    # Validate JD file
    # --------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail=(
                "No Job Description filename "
                "was provided."
            )
        )

    if not file.filename.lower().endswith(
        ".txt"
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Only TXT Job Description "
                "files are supported."
            )
        )

    # --------------------------------------
    # Read JD text
    # --------------------------------------

    try:

        raw_content = await file.read()

        jd_text = raw_content.decode(
            "utf-8",
            errors="ignore"
        )

    finally:

        await file.close()

    if not jd_text.strip():

        raise HTTPException(
            status_code=400,
            detail=(
                "The Job Description file "
                "is empty."
            )
        )

    safe_jd_name = Path(
        file.filename
    ).name

    # --------------------------------------
    # Extract JD skills
    # --------------------------------------

    jd_skills = extract_jd_skills(
        jd_text
    )

    # --------------------------------------
    # Extract resume skills
    # --------------------------------------

    resume_skills = (
        extract_resume_skills(
            chunks
        )
    )

    # --------------------------------------
    # Match resume and JD
    # --------------------------------------

    match_result = match_skills(
        resume_skills,
        jd_skills
    )

    # --------------------------------------
    # Skill gap analysis
    # --------------------------------------

    skill_gap = analyze_skill_gap(
        match_result
    )

    # --------------------------------------
    # Improvement suggestions
    # --------------------------------------

    missing_skills = skill_gap[
        "missing_skills"
    ]

    improvement_suggestions = []

    for skill in missing_skills:

        improvement_suggestions.append(
            (
                f"Consider strengthening "
                f"your knowledge of {skill}."
            )
        )

    if not missing_skills:

        improvement_suggestions.append(
            (
                "No major technical skill gaps "
                "were detected for this "
                "Job Description."
            )
        )

    # --------------------------------------
    # AI Resume ↔ JD analysis
    # --------------------------------------

    try:

        ai_analysis = analyze_resume_jd(
            resume_text,
            jd_text
        )

    except Exception as exc:

        print(
            f"AI JD analysis error: {exc}"
        )

        ai_analysis = (
            "AI analysis could not be "
            "generated at this time."
        )

    # --------------------------------------
    # Save active JD
    # --------------------------------------

    request.app.state.jd_name = (
        safe_jd_name
    )

    request.app.state.jd_text = (
        jd_text
    )

    # --------------------------------------
    # Final response
    # --------------------------------------

    return {
        "status": "success",

        "resume": resume_name,

        "job_description": (
            safe_jd_name
        ),

        "resume_skills": (
            resume_skills
        ),

        "jd_skills": (
            jd_skills
        ),

        "match_percentage": (
            skill_gap[
                "match_percentage"
            ]
        ),

        "coverage": (
            skill_gap[
                "coverage"
            ]
        ),

        "total_skills": (
            skill_gap[
                "total_skills"
            ]
        ),

        "matched_skills": (
            skill_gap[
                "matched_skills"
            ]
        ),

        "missing_skills": (
            skill_gap[
                "missing_skills"
            ]
        ),

        "improvement_suggestions": (
            improvement_suggestions
        ),

        "ai_analysis": (
            ai_analysis
        )
    }
