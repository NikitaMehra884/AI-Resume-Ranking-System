# 🤖 AI Recruitment & Resume Ranking Intelligence Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4+-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Sentence-Transformers](https://img.shields.io/badge/AI_Model-all--MiniLM--L6--v2-orange?style=flat)](https://www.sbert.net)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4+-06B6D4?style=flat&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite_3-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org)

An intelligent, full-stack hiring platform that replaces slow manual resume screening with **multi-signal AI ranking**. 

Recruiters post jobs and instantly see applicants ranked from best to least fit. Candidates apply with their resume (PDF/DOCX/TXT) and track their shortlisting status in real time.

---

## 🔄 Complete Workflow (How It Works)

```
┌─────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐       ┌────────────────────────┐
│ 1. POST JOB     │       │ 2. CANDIDATE APPLIES │       │ 3. AI EVALUATES      │       │ 4. SHORTLIST & TALENT  │
│ Recruiter posts │ ────> │ Candidate uploads    │ ────> │ AI calculates        │ ────> │ Recruiter shortlists,  │
│ job opening     │       │ resume & submits     │       │ Match Score (0-100%) │       │ views resume & creates │
│ with skills     │       │ profile details      │       │ based on 3 signals   │       │ tailored interview Qs  │
└─────────────────┘       └──────────────────────┘       └──────────────────────┘       └────────────────────────┘
```

1. **Job Creation**: Recruiter posts a role with required skills, minimum experience, and department.
2. **Application Submission**: Candidate uploads their resume (PDF, Word DOCX, or text). The system parses contact info, skills, and experience without page freezing.
3. **Multi-Signal AI Ranking**: The AI compares the resume against the job description and computes an instant **Match Score (0–100%)**.
4. **Recruiter Actions**: The recruiter opens the job, reviews applicants sorted by score (#1, #2, #3...), shortlists candidates with one click, and generates tailored AI interview questions.
5. **Real-Time Tracking**: Candidate portal immediately reflects the updated status (*Shortlisted*, *Interview*, *Under Review*, or *Rejected*).

---

## ✨ Key Features (Everything Included)

### 👔 For Recruiters
- **Live Applicant Badges**: Job cards show live counters (e.g. `4 Applied • 2 Shortlisted`).
- **AI-Ranked Applicant List**: Candidates are automatically sorted by match percentage.
- **1-Click Auto-Shortlist**: Instantly shortlist all applicants scoring **$\ge$ 75%**.
- **Status Controls**: Update status (`Shortlist`, `Interview`, `Reject`) with one click.
- **AI Interview Questions**: Generates 3 categories of custom questions (Technical, Behavioral, Resume Project) with a 1-click **Copy** button.
- **In-App Resume Reader**: Inspect candidate resume text, phone, email, and skills inside a clean modal.
- **Grounded Match Evidence**: Explains *Why Ranked*, *Key Strengths*, and *Missing Skills* without AI hallucinations.
- **Add Demo Applicants**: Click `+ Add 4 Demo Applicants` to inject realistic sample profiles for instant testing.

### 🎓 For Candidates
- **Browse Open Roles**: Search open positions by title, department, or location.
- **Fast Resume Upload**: Upload `.pdf`, `.docx`, or `.txt` with automatic details pre-fill.
- **Live Application Tracking**: See real-time badges (*Under Review*, *Shortlisted*, *Interview Scheduled*, *Not Selected*).
- **Instant AI Match Score**: Get immediate feedback on how well your resume matches the job.
- **Interactive Match Analyzer**: Compare any resume against any job description to view skill gaps.

---

## 🧠 The AI Ranking Engine (Explained Simply)

Instead of naive keyword matching or hallucinating chatbots, the platform uses a **transparent 3-signal formula**:

```
Final Fit Score = (Skills Match × 40%) + (Semantic Meaning × 30%) + (Experience Alignment × 30%)
```

| Signal | Weight | How It Works | Why It's Powerful |
| :--- | :---: | :--- | :--- |
| **1. Skills Match** | **40%** | Checks candidate skills against mandatory job requirements. | Ensures core technical stack is met. |
| **2. Semantic Context** | **30%** | Uses `sentence-transformers/all-MiniLM-L6-v2` (384-dim dense vectors) to evaluate resume meaning. | Detects synonyms (e.g. understands *"cloud APIs"* matches *"backend microservices"*). |
| **3. Experience Fit** | **30%** | Compares candidate years of experience against the role's target bracket. | Rewards target experience; prevents unfair over-qualification penalties. |

> **Explainable AI (XAI)**: Every score includes verifiable proof (exact matched skills and missing skill gaps) so recruiters understand exactly why a candidate was ranked #1.

---

## 💡 AI Interview Question Generator (Special Feature)

Clicking **"AI Questions"** on any candidate dynamically generates questions in 3 areas:
1. **Technical & Architecture**: Targeted questions based on the candidate's verified skills (e.g. PyTorch, FastAPI, SQL).
2. **Behavioral & Culture**: Seniority-calibrated teamwork and conflict resolution scenarios.
3. **Resume Project Probing**: Deep-dive questions testing the authenticity of projects listed on their resume.

---

## 🗄️ Database & Storage

All data is stored in a clean, relational **SQLite database** located at:
```text
c:\Projects\AI Resume Ranking System\data\platform.db
```
- **`jobs` & `job_skills`**: Job titles, requirements, and minimum experience.
- **`candidate_profiles`**: Candidate contact info, experience, and uploaded resume text.
- **`applications`**: Links candidate to job, saves the AI match score, application status, and explainability report.
- **`users`**: Secure user accounts with bcrypt hashed passwords and JWT authentication.

---

## 🚀 How to Run (2 Simple Steps)

### Step 1: Start Backend (Terminal 1)
```powershell
# Activate virtual environment
.\venv\Scripts\activate

# (Optional) Seed initial users & jobs
python scripts/seed_db.py

# Run FastAPI backend server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
📍 **Backend API & Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Step 2: Start Frontend (Terminal 2)
```powershell
# Navigate to frontend
cd frontend

# Run Vite dev server
npm run dev
```
📍 **Frontend Website**: [http://localhost:3000](http://localhost:3000)

---

## 🔑 Demo Login Accounts

| Role | Email | Password | What You Can Test |
| :--- | :--- | :--- | :--- |
| **Recruiter** | `recruiter@platform.ai` | `password123` | Post jobs, review ranked applicants, shortlist, generate AI interview questions |
| **Candidate** | `candidate@platform.ai` | `password123` | Browse jobs, apply with resume, view match score, track application status |

---

## 🛠️ Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Axios
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy ORM, Pydantic v2
- **AI & NLP**: Sentence-Transformers (`all-MiniLM-L6-v2`), PyPDF, python-docx
- **Database**: SQLite 3 (`data/platform.db`)
- **Security**: JWT Bearer Tokens, Bcrypt password hashing, Role-Based Access Control

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).