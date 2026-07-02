# 🤖 AI Resume Ranking System

> **Beyond Keywords. Intelligent Hiring with Semantic AI.**

An Explainable AI-powered Resume Ranking System that intelligently matches candidates to job descriptions using **Semantic Search, FAISS Vector Search, and Hybrid AI Scoring**.

Built for the **India.Runs AI Hiring Challenge** by Redrob & H2S.

---

## 🌐 Live Demo

🚀 **Streamlit Demo**

https://nikitamehra884-ai-resume-ranking-system-app-n4rqzk.streamlit.app/

---

## 📂 GitHub Repository

https://github.com/NikitaMehra884/AI-Resume-Ranking-System

---

# 📖 Overview

Recruiters often review thousands of resumes while traditional ATS systems rely primarily on keyword matching. This frequently causes highly qualified candidates to be overlooked.

Our solution introduces an **Explainable AI Resume Ranking System** capable of understanding the semantic meaning of a Job Description instead of simply matching keywords.

The system combines multiple AI techniques to evaluate candidate relevance and generates a trusted Top-100 candidate shortlist.

---

# 🎯 Problem Statement

Traditional hiring systems rely heavily on keyword matching and manual resume screening, making it difficult to identify the best candidates from large talent pools.

Our solution uses **Semantic Search + FAISS + Hybrid AI Scoring** to intelligently understand candidate profiles and produce transparent, explainable rankings.

---

# ✨ Key Features

- 🔍 Semantic Job Description Understanding
- 🤖 AI-powered Resume Ranking
- ⚡ FAISS Vector Search
- 📄 Explainable Candidate Recommendations
- 🧠 Sentence Transformer Embeddings
- 📊 Hybrid AI Scoring
- 📥 CSV Export
- 🌐 Streamlit Web Interface
- 💻 CPU Optimized
- 🚀 Scalable Architecture

---

# 🏗 System Architecture

```
                Job Description
                        │
                        ▼
               JD Understanding
                        │
                        ▼
          Sentence Transformer Embeddings
                        │
                        ▼
               FAISS Vector Retrieval
                        │
                        ▼
          Hybrid AI Scoring Engine
      ┌────────┬────────┬────────┐
      │Skills  │Experience│Education│
      └────────┴────────┴────────┘
                        │
                        ▼
            Explainable AI Reasoning
                        │
                        ▼
            Top-100 Ranked Candidates
```

---

# ⚙ AI Pipeline

### Step 1

Read Job Description

↓

### Step 2

Generate Semantic Embeddings

↓

### Step 3

Retrieve Similar Candidates using FAISS

↓

### Step 4

Compute Hybrid AI Scores

↓

### Step 5

Generate Explainable Rankings

↓

### Step 6

Export submission.csv

---

# 🧠 AI Models Used

| Model | Purpose |
|--------|----------|
| Sentence Transformers (MiniLM) | Semantic Embeddings |
| FAISS | Vector Similarity Search |
| BM25 | Lexical Matching |
| Hybrid AI Ranking | Candidate Scoring |
| Explainability Engine | Ranking Justification |

---

# 📊 Hybrid Ranking Signals

The final AI score combines multiple recruiter-inspired signals:

- Semantic Similarity
- Technical Skills
- Experience
- Education
- Career Progression
- Behavioral Signals
- Recruiter Preferences

---

# 📁 Project Structure

```
AI-Resume-Ranking-System/

│
├── backend/
│   ├── models/
│   ├── modules/
│   ├── parsers/
│   ├── pipelines/
│   ├── preprocessing/
│   ├── retrieval/
│   ├── services/
│   ├── utils/
│   ├── outputs/
│   └── main.py
│
├── data/
│
├── cache/
│
├── docs/
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Technologies Used

### Programming

- Python

### Frontend

- Streamlit

### Backend

- FastAPI
- Python

### Machine Learning

- Sentence Transformers
- Scikit-learn
- NumPy
- Pandas

### Vector Search

- FAISS

### Information Retrieval

- BM25

### NLP

- Hugging Face Transformers

### Visualization

- Streamlit Components

---

# 💻 Installation

Clone the repository

```bash
git clone https://github.com/NikitaMehra884/AI-Resume-Ranking-System.git
```

Move inside project

```bash
cd AI-Resume-Ranking-System
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Project

Run backend

```bash
python -m backend.main
```

Run Streamlit App

```bash
streamlit run app.py
```

---

# 📈 Output

The system generates

- submission.csv
- top_candidates.csv
- Top 100 Ranked Candidates
- Explainable AI Scores

---

# 🌟 Advantages

✔ Understands semantic meaning instead of keywords

✔ Faster candidate retrieval using FAISS

✔ Explainable AI recommendations

✔ Recruiter-inspired hybrid ranking

✔ Production-ready modular architecture

✔ Scalable for large datasets

---

# 📸 Demo

Live Demo

👉 https://nikitamehra884-ai-resume-ranking-system-app-n4rqzk.streamlit.app/

---

# 🎥 Demo Video

(Add YouTube or Google Drive demo link here)

---

# 📄 Presentation

India.Runs Final Presentation

(Add PDF Link)

---

# 🔮 Future Scope

- LLM-powered Resume Understanding
- Interview Recommendation Engine
- Skill Gap Analysis
- ATS Integration
- Recruiter Dashboard
- Real-time Hiring Analytics
- Cloud Deployment
- Multi-language Resume Support

---

# 👩‍💻 Team

## Team Name

**ERROR__**

### Team Leader

**Nikita Mehra**

Graphic Era Hill University

---

# 🏆 Built For

**India.Runs Hackathon**

Powered by

- Redrob
- H2S

---

## ⭐ If you like this project, please give it a Star!
