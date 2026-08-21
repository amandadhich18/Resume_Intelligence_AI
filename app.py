import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

# PRODUCTION API
API_BASE_URL = "https://resume-intelligence-ai-duus.onrender.com"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Resume Intelligence AI",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_resume" not in st.session_state:
    st.session_state.active_resume = None

if "uploaded_resume_key" not in st.session_state:
    st.session_state.uploaded_resume_key = None

if "jd_result" not in st.session_state:
    st.session_state.jd_result = None

if "uploaded_jd_key" not in st.session_state:
    st.session_state.uploaded_jd_key = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def show_sources(sources):
    """
    Display retrieved resume chunks used by the RAG pipeline.
    """

    if not sources:
        return

    with st.expander("🔎 View Retrieved Sources"):

        for index, source in enumerate(sources, start=1):

            st.markdown(
                f"### Source {index}: "
                f"{source.get('section', 'Unknown')}"
            )

            source_name = source.get("source")

            if source_name:
                st.caption(
                    f"Resume: {source_name}"
                )

            if "score" in source:
                st.caption(
                    f"Overall Score: "
                    f"{source['score']:.4f}"
                )

            if "semantic_score" in source:
                st.caption(
                    f"Semantic Score: "
                    f"{source['semantic_score']:.4f}"
                )

            if "keyword_score" in source:
                st.caption(
                    f"Keyword Score: "
                    f"{source['keyword_score']:.4f}"
                )

            st.write(
                source.get(
                    "text",
                    "No source text available."
                )
            )

            st.divider()


def format_skill(skill):
    """
    Format skill names for UI display.
    """

    return skill.title()


def clean_pdf_filename(filename):
    """
    Ensure a PDF filename contains only one .pdf extension.

    Examples:
    resume.pdf.pdf -> resume.pdf
    resume.pdf     -> resume.pdf
    """

    if not filename:
        return "resume.pdf"

    filename = filename.strip()

    while filename.lower().endswith(".pdf.pdf"):
        filename = filename[:-4]

    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    return filename


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📄 Resume Intelligence AI")

    st.caption(
        "Upload a resume, chat with it, "
        "compare it with a Job Description, "
        "and identify skill gaps."
    )

    st.divider()

    # --------------------------------------------------------
    # API STATUS
    # --------------------------------------------------------

    st.subheader("🔌 API Status")

    if st.button(
        "Check API",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"{API_BASE_URL}/health",
                timeout=60
            )

            response.raise_for_status()

            health = response.json()

            if health.get("model_ready"):

                st.success("🟢 API Online")

                active = health.get("active_resume")

                if active:

                    # Clean old duplicate extension for display
                    active = clean_pdf_filename(active)

                    st.caption(
                        f"Active resume: {active}"
                    )

            else:

                st.warning("🟡 API Starting")

        except Exception:

            st.error("🔴 API Offline")

    st.divider()

    # --------------------------------------------------------
    # RESUME UPLOAD
    # --------------------------------------------------------

    st.subheader("📂 Upload Resume")

    resume_file = st.file_uploader(
        "Choose a Resume PDF",
        type=["pdf"],
        key="resume_uploader"
    )

    if resume_file is not None:

        # Clean the filename before sending it to FastAPI.
        safe_resume_name = clean_pdf_filename(
            resume_file.name
        )

        resume_key = (
            safe_resume_name,
            resume_file.size
        )

        if (
            resume_key
            != st.session_state.uploaded_resume_key
        ):

            with st.spinner(
                "Processing resume..."
            ):

                try:

                    response = requests.post(
                        f"{API_BASE_URL}/upload-resume",
                        files={
                            "file": (
                                safe_resume_name,
                                resume_file.getvalue(),
                                "application/pdf"
                            )
                        },
                        timeout=180
                    )

                    response.raise_for_status()

                    result = response.json()

                    returned_filename = result.get(
                        "filename",
                        safe_resume_name
                    )

                    # Clean filename returned by backend too.
                    st.session_state.active_resume = (
                        clean_pdf_filename(
                            returned_filename
                        )
                    )

                    st.session_state.uploaded_resume_key = (
                        resume_key
                    )

                    # New resume = reset previous chat/JD state
                    st.session_state.messages = []
                    st.session_state.jd_result = None
                    st.session_state.uploaded_jd_key = None

                    st.success(
                        "✅ Resume processed successfully"
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "Resume processing timed out."
                    )

                except requests.exceptions.RequestException as exc:

                    st.error(
                        "Could not upload the resume."
                    )

                    st.caption(str(exc))

                except Exception as exc:

                    st.error(
                        "Unexpected resume processing error."
                    )

                    st.caption(str(exc))

    if st.session_state.active_resume:

        st.info(
            f"Active Resume:\n\n"
            f"**{st.session_state.active_resume}**"
        )

    st.divider()

    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.title("📄 Resume Intelligence AI")

st.write(
    "Upload a resume, ask questions about the candidate, "
    "compare the resume against a Job Description, and "
    "discover skill gaps and improvement opportunities."
)

st.caption(
    "FastEmbed • Hybrid RAG • Groq • "
    "FastAPI • Docker • Render"
)


# ============================================================
# SYSTEM INFORMATION
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Backend",
        "FastAPI"
    )

with col2:

    st.metric(
        "Embeddings",
        "FastEmbed"
    )

with col3:

    st.metric(
        "Retrieval",
        "Hybrid RAG"
    )

with col4:

    st.metric(
        "LLM",
        "Groq"
    )


st.divider()


# ============================================================
# RESUME CHAT
# ============================================================

st.header("💬 Chat with the Resume")

if not st.session_state.active_resume:

    st.info(
        "👈 Upload a Resume PDF from the sidebar "
        "before starting the chat."
    )

else:

    st.caption(
        f"Currently analyzing: "
        f"{st.session_state.active_resume}"
    )


# ------------------------------------------------------------
# DISPLAY CHAT HISTORY
# ------------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            show_sources(
                message["sources"]
            )


# ------------------------------------------------------------
# CHAT INPUT
# ------------------------------------------------------------

question = st.chat_input(
    "Ask something about the uploaded resume...",
    disabled=(
        st.session_state.active_resume
        is None
    )
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Analyzing the resume..."
        ):

            try:

                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                answer = result.get(
                    "answer",
                    "No answer was returned."
                )

                sources = result.get(
                    "sources",
                    []
                )

                st.markdown(answer)

                show_sources(sources)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    }
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The API took too long to respond."
                )

            except requests.exceptions.RequestException as exc:

                st.error(
                    "Could not connect to the Resume "
                    "Intelligence API."
                )

                st.caption(str(exc))

            except Exception as exc:

                st.error(
                    "An unexpected error occurred."
                )

                st.caption(str(exc))


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

if st.session_state.active_resume:

    with st.expander(
        "💡 Example Resume Questions"
    ):

        st.markdown(
            """
- What is the candidate's current role?
- What technical skills does the candidate have?
- What projects has the candidate worked on?
- What database technologies does the candidate know?
- What BI tools does the candidate use?
- What certifications does the candidate have?
- Summarize the candidate's professional experience.
"""
        )


# ============================================================
# JOB DESCRIPTION MATCHING
# ============================================================

st.divider()

st.header(
    "🎯 Resume ↔ Job Description Matching"
)

st.write(
    "Upload a Job Description to compare its requirements "
    "against the currently active resume."
)


if not st.session_state.active_resume:

    st.warning(
        "Upload a resume before analyzing "
        "a Job Description."
    )

else:

    jd_file = st.file_uploader(
        "📁 Upload Job Description (.txt)",
        type=["txt"],
        key="jd_uploader"
    )

    if jd_file is not None:

        jd_key = (
            jd_file.name,
            jd_file.size
        )

        if (
            jd_key
            != st.session_state.uploaded_jd_key
        ):

            with st.spinner(
                "Analyzing Resume ↔ Job Description..."
            ):

                try:

                    response = requests.post(
                        f"{API_BASE_URL}/analyze-job-description",
                        files={
                            "file": (
                                jd_file.name,
                                jd_file.getvalue(),
                                "text/plain"
                            )
                        },
                        timeout=180
                    )

                    response.raise_for_status()

                    st.session_state.jd_result = (
                        response.json()
                    )

                    st.session_state.uploaded_jd_key = (
                        jd_key
                    )

                    st.success(
                        "✅ Job Description analyzed successfully"
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "Job Description analysis timed out."
                    )

                except requests.exceptions.RequestException as exc:

                    st.error(
                        "Could not analyze the "
                        "Job Description."
                    )

                    st.caption(str(exc))

                except Exception as exc:

                    st.error(
                        "Unexpected JD analysis error."
                    )

                    st.caption(str(exc))


# ============================================================
# JD RESULTS
# ============================================================

result = st.session_state.jd_result


if result:

    st.divider()

    st.subheader(
        "📊 Match Summary"
    )

    match_percentage = result.get(
        "match_percentage",
        0
    )

    coverage = result.get(
        "coverage",
        "Unknown"
    )

    total_skills = result.get(
        "total_skills",
        0
    )

    matched_skills = result.get(
        "matched_skills",
        []
    )

    missing_skills = result.get(
        "missing_skills",
        []
    )


    # --------------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------------

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )

    with metric1:

        st.metric(
            "Rule-Based Skill Match",
            f"{match_percentage:.2f}%"
        )

    with metric2:

        st.metric(
            "Coverage",
            coverage
        )

    with metric3:

        st.metric(
            "Matched Skills",
            len(matched_skills)
        )

    with metric4:

        st.metric(
            "Missing Skills",
            len(missing_skills)
        )


    st.progress(
        min(
            max(
                match_percentage / 100,
                0.0
            ),
            1.0
        )
    )

    st.caption(
        f"Detected {total_skills} relevant "
        f"skills in the Job Description."
    )


    # --------------------------------------------------------
    # SKILL COMPARISON
    # --------------------------------------------------------

    st.subheader(
        "🧩 Skill Comparison"
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            "### ✅ Matched Skills"
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    format_skill(skill)
                )

        else:

            st.info(
                "No matched skills detected."
            )


    with right:

        st.markdown(
            "### ⚠️ Missing Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.warning(
                    format_skill(skill)
                )

        else:

            st.success(
                "No major technical skill gaps detected."
            )


    # --------------------------------------------------------
    # IMPROVEMENT SUGGESTIONS
    # --------------------------------------------------------

    st.subheader(
        "📈 Skill Gap & Improvement Suggestions"
    )

    suggestions = result.get(
        "improvement_suggestions",
        []
    )

    if suggestions:

        for suggestion in suggestions:

            st.markdown(
                f"- {suggestion}"
            )

    else:

        st.info(
            "No improvement suggestions were generated."
        )


    # --------------------------------------------------------
    # DETECTED SKILLS
    # --------------------------------------------------------

    with st.expander(
        "🔍 View Detected Skills"
    ):

        col_a, col_b = st.columns(2)

        with col_a:

            st.markdown(
                "### Resume Skills"
            )

            resume_skills = result.get(
                "resume_skills",
                []
            )

            for skill in resume_skills:

                st.write(
                    f"• {skill}"
                )


        with col_b:

            st.markdown(
                "### Job Description Skills"
            )

            jd_skills = result.get(
                "jd_skills",
                []
            )

            for skill in jd_skills:

                st.write(
                    f"• {skill}"
                )


    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    st.subheader(
        "🤖 AI Resume ↔ Job Description Analysis"
    )

    st.caption(
        "The rule-based percentage above measures exact "
        "detected skill overlap. The AI analysis below "
        "evaluates the broader candidate fit."
    )

    ai_analysis = result.get(
        "ai_analysis"
    )

    if ai_analysis:

        st.markdown(
            ai_analysis
        )

    else:

        st.warning(
            "AI analysis was not available."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Resume Intelligence AI • "
    "Resume RAG + JD Matching + Skill Gap Analysis • "
    "FastEmbed + Groq + FastAPI"
)
