# 📄 Resume Intelligence AI

An **AI-powered Resume Intelligence platform** that allows users to upload a resume, ask questions about the candidate, compare the resume against a Job Description, identify skill gaps, and receive AI-generated improvement suggestions.

The application combines **FastAPI, Streamlit, FastEmbed, Hybrid RAG, Groq, Docker, and Render** to provide an end-to-end resume analysis experience.

---

## 🚀 Features

### 📄 Resume Upload & Processing

- Upload resume files in **PDF format**
- Extract and process resume content
- Automatically activate the uploaded resume for analysis
- Generate embeddings for resume sections
- Use the uploaded resume for question answering and Job Description analysis

### 💬 Chat with Resume

Ask natural-language questions about the uploaded resume.

**Example questions:**

- What are the candidate's strongest technical skills?
- Summarize the candidate's professional experience.
- What projects has the candidate worked on?
- What database technologies does the candidate know?
- What BI tools does the candidate use?
- What certifications does the candidate have?

The system uses **Hybrid Retrieval-Augmented Generation (RAG)** to retrieve relevant resume information before generating the answer.

### 🎯 Resume ↔ Job Description Matching

Upload a Job Description and compare its requirements against the currently active resume.

The system provides:

- Rule-based skill match percentage
- Matched skills
- Missing skills
- Skill coverage
- Skill-gap identification
- Resume improvement suggestions
- AI-powered candidate fit analysis

### 🤖 AI Candidate Analysis

The AI analysis generates:

1. **Overall Candidate Fit**
2. **Candidate Strengths**
3. **Skill Gaps**
4. **Resume Improvement Suggestions**
5. **Interview Preparation Topics**
6. **Final Recommendation**

---

## 🧠 System Architecture

```text
                    ┌──────────────────────┐
                    │    Streamlit UI      │
                    │       app.py         │
                    └──────────┬───────────┘
                               │
                               │ HTTP Requests
                               ▼
                    ┌──────────────────────┐
                    │   FastAPI Backend    │
                    │     api/main.py      │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       Resume Parser       FastEmbed        Skill Matching
             │             Embeddings             │
             │                 │                   │
             └────────────► Hybrid RAG ◄───────────┘
                               │
                               ▼
                         Groq LLM API
                               │
                               ▼
                      AI Generated Response
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application development |
| **Streamlit** | Frontend user interface |
| **FastAPI** | REST API backend |
| **FastEmbed** | Resume embedding generation |
| **Hybrid RAG** | Resume information retrieval |
| **Groq** | LLM inference |
| **Docker** | Backend containerization |
| **Render** | FastAPI backend deployment |
| **Streamlit Community Cloud** | Frontend deployment |
| **GitHub** | Version control and deployment integration |

---

## 📁 Project Structure

```text
Resume_Intelligence_AI/
│
├── api/
│   └── main.py
│
├── src/
│   ├── embeddings.py
│   ├── retriever.py
│   ├── agent.py
│   └── ...
│
├── Data/
│   └── Resume/
│
├── evaluation/
│
├── tests/
│
├── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔌 API Endpoints

The **FastAPI backend** provides the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API root |
| `GET` | `/health` | Check API and model health |
| `POST` | `/upload-resume` | Upload and process a resume |
| `POST` | `/ask` | Ask questions about the active resume |
| `POST` | `/analyze-job-description` | Compare the resume with a Job Description |

Interactive FastAPI documentation is available through:

```text
/docs
```

---

## ⚙️ Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/amandadhich18/Resume_Intelligence_AI.git
cd Resume_Intelligence_AI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

> **Important:** Never commit your `.env` file or API keys to GitHub.

---

## ▶️ Run the FastAPI Backend

Start the backend with:

```bash
uvicorn api.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🖥️ Run the Streamlit Frontend

Open another terminal and run:

```bash
streamlit run app.py
```

The Streamlit application will normally open at:

```text
http://localhost:8501
```

---

## 🐳 Docker

The FastAPI backend can also be run using Docker.

### Build the Docker Image

```bash
docker build -t resume-intelligence-ai .
```

### Run the Docker Container

```bash
docker run --env-file .env -p 8000:8000 --name resume-ai-api resume-intelligence-ai
```

The containerized API will then be available at:

```text
http://localhost:8000
```

---

## ☁️ Deployment

The project uses separate frontend and backend deployments.

### Backend

The **FastAPI backend** is:

- Containerized using **Docker**
- Deployed on **Render**
- Responsible for resume processing, embeddings, retrieval, skill matching, and LLM communication

### Frontend

The **Streamlit frontend** is:

- Built using **Streamlit**
- Deployed using **Streamlit Community Cloud**
- Connected to the production FastAPI backend

### Deployment Architecture

```text
                     User
                       │
                       ▼
              Streamlit Community Cloud
                       │
                       ▼
               FastAPI API on Render
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
   Resume Parser   FastEmbed    Skill Matching
          │            │            │
          └────────────┼────────────┘
                       ▼
                   Hybrid RAG
                       │
                       ▼
                    Groq LLM
                       │
                       ▼
               Generated Response
```

---

## 🔍 Resume Question-Answering Workflow

```text
1. User uploads Resume PDF
             ↓
2. Resume text is extracted and processed
             ↓
3. Resume is divided into relevant sections
             ↓
4. Embeddings are generated using FastEmbed
             ↓
5. Resume becomes the active resume
             ↓
6. User asks a question
             ↓
7. Hybrid RAG retrieves relevant resume sections
             ↓
8. Retrieved context is provided to the LLM
             ↓
9. Groq generates the contextual answer
```

---

## 🎯 Job Description Analysis Workflow

```text
Resume + Job Description
          │
          ▼
    Skill Extraction
          │
          ▼
    Skill Comparison
          │
          ▼
 ┌───────────────────┐
 │ Matched Skills    │
 │ Missing Skills    │
 └─────────┬─────────┘
           │
           ▼
   Match Percentage
           │
           ▼
    Skill Gap Analysis
           │
           ▼
      AI Fit Analysis
           │
           ▼
 Improvement Suggestions
           │
           ▼
 Interview Preparation
```

---

## 📊 Current Capabilities

The application currently supports:

- ✅ Resume PDF processing
- ✅ Dynamic resume upload
- ✅ Resume question answering
- ✅ FastEmbed embeddings
- ✅ Hybrid resume retrieval
- ✅ Retrieval-Augmented Generation
- ✅ Job Description upload
- ✅ Job Description analysis
- ✅ Technical skill extraction
- ✅ Resume ↔ JD skill matching
- ✅ Match percentage calculation
- ✅ Skill-gap identification
- ✅ Resume improvement recommendations
- ✅ AI candidate-fit analysis
- ✅ Interview preparation recommendations
- ✅ FastAPI REST API
- ✅ Streamlit web interface
- ✅ Dockerized backend
- ✅ Render backend deployment
- ✅ Streamlit Community Cloud frontend deployment

---

## 💡 Example Use Case

Suppose a Job Description requires:

```text
Python
SQL
Power BI
Tableau
Excel
Data Analysis
Data Visualization
```

The application analyzes the active resume and separates the requirements into:

### ✅ Matched Skills

Skills found in both the resume and Job Description.

### ⚠️ Missing Skills

Skills detected in the Job Description but not explicitly detected in the resume.

The application then calculates a **rule-based skill match percentage** and uses the LLM to perform a broader candidate-fit analysis.

This distinction helps avoid treating exact keyword overlap and AI-based contextual evaluation as the same measurement.

---

## 🤖 AI Analysis Output

The AI-powered Resume ↔ Job Description analysis can provide:

### 1. Overall Candidate Fit

An overall assessment of how closely the candidate aligns with the Job Description.

### 2. Candidate Strengths

Highlights relevant technical skills, projects, tools, and experience.

### 3. Skill Gaps

Identifies requirements that are missing or weakly represented in the resume.

### 4. Resume Improvement Suggestions

Provides practical recommendations for improving alignment with the target role.

### 5. Interview Preparation

Suggests technical and business topics that the candidate should prepare for.

### 6. Final Recommendation

The candidate can be classified as:

- **Strong Fit**
- **Good Fit**
- **Partial Fit**
- **Low Fit**

---

## 🔮 Future Improvements

Potential future improvements include:

- [ ] Support for DOCX resumes
- [ ] Multiple resume comparison
- [ ] Semantic Job Description skill matching
- [ ] ATS compatibility scoring
- [ ] Resume scoring dashboard
- [ ] Resume keyword recommendations
- [ ] Improved skill taxonomy
- [ ] Candidate ranking
- [ ] Persistent vector database
- [ ] User authentication
- [ ] Resume analysis history
- [ ] Exportable PDF analysis reports
- [ ] Advanced evaluation pipeline
- [ ] Automated resume improvement recommendations
- [ ] Multi-candidate recruitment dashboard

---

## 🎯 Project Goal

The goal of **Resume Intelligence AI** is to demonstrate how modern **Data Analytics, Generative AI, Retrieval-Augmented Generation, API development, and cloud deployment** technologies can be combined to build a practical resume intelligence application.

The project combines:

```text
Resume Processing
        +
Embedding Generation
        +
Hybrid Retrieval
        +
Skill Matching
        +
Retrieval-Augmented Generation
        +
LLM Analysis
        +
FastAPI
        +
Streamlit
        +
Docker
        +
Cloud Deployment
```

into a complete **end-to-end AI application**.

---

## 👨‍💻 Author

### **Aman Dadhich**

***Data Analyst | Generative AI (GenAI) Enthusiast***

Passionate about building **data-driven** and **AI-powered solutions** using **Python, SQL, Power BI, Machine Learning, RAG, and Generative AI**.

---

## ⭐ Support

If you find this project useful, consider giving the repository a **⭐ Star on GitHub**.

Contributions, suggestions, and feedback are welcome.
