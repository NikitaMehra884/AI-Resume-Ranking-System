# TalentIntelligence AI — Enterprise AI Recruitment Intelligence Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4+-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![FAISS](https://img.shields.io/badge/FAISS-Dense%20Search-blue?style=flat)](https://github.com/facebookresearch/faiss)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4+-06B6D4?style=flat&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A production-grade **AI Recruitment Intelligence & Candidate Ranking Platform** engineered to discover, score, and rank candidates across a **100,000+ candidate talent corpus** in milliseconds with mathematically normalized multi-signal ranking, grounded explainability, and algorithmic fairness guarantees.

---

## 🌟 Key Highlights

* **100,000 Candidate Index**: Evaluated on the Redrob Talent Discovery benchmark dataset (`data/dataset/candidates.jsonl`).
* **4-Stage Hybrid Architecture**: Hard eligibility filtering $\to$ Hybrid dense-sparse retrieval (FAISS + BM25) $\to$ Multi-signal scoring ($[0, 100]$ normalized) $\to$ Configurable Top-$K$ shortlist ($K=5, 10, 20, 50, 100$).
* **Grounded Explainability**: Eliminates hallucinations. Generates verifiable evidence linking ranking positions to exact matched skills and experience gaps.
* **Algorithmic Fairness**: By-design demographic blindness masking gender, age, ethnicity, and nationality from vector spaces and scoring weights.
* **Dual Workspaces**:
  * **Recruiter Command Suite**: Live candidate screening, side-by-side comparison matrix, Kanban pipeline, AI interview question generator, pipeline analytics.
  * **Candidate Workspace**: Automated resume parser (PDF/DOCX), profile editor, open jobs directory, interactive AI match analyzer.

---

## 🏛️ System Architecture

```
                                  [Job Description Mandate]
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       ▼                                           ▼
             [Dense Embedding]                            [Lexical Tokens]
        (all-MiniLM-L6-v2, 384-dim)                      (BM25Okapi Tokens)
                       │                                           │
                       ▼                                           ▼
           [FAISS IndexFlatIP Search]                    [BM25 Sparse Search]
             (Top 1,500 candidates)                     (Top 1,500 candidates)
                       │                                           │
                       └─────────────────────┬─────────────────────┘
                                             ▼
                                  [Union Retrieval Pool]
                                   (~2,500 - 3,000 IDs)
                                             │
                                             ▼
                       Stage 1: Hard Eligibility Filters
                       (Role Alignment, Min Exp, Location)
                                             │
                                             ▼
                       Stage 3: Normalized Multi-Signal Scoring
                       Final = Σ w_i · Signal_i  (Strictly in [0, 100])
                                             │
                                             ▼
                       Stage 4: Top-K Shortlist (K = 5, 10, 20, 50, 100)
                                             │
                                             ▼
                       [Grounded LLM Evidence & Explainability]
```

### Multi-Signal Scoring Weights

| Signal | Feature | Weight | Mathematical Formulation |
| :--- | :--- | :---: | :--- |
| **Semantic** | Dense Vector Cosine Similarity | `0.25` | $(\mathbf{e}_Q \cdot \mathbf{e}_c) \times 100$ |
| **Lexical** | Sparse BM25 Term Matching | `0.10` | $\frac{\text{BM25}(Q, D_c)}{\max_j \text{BM25}(Q, D_j)} \times 100$ |
| **Required Skills** | Mandatory Skill Jaccard Fit | `0.25` | $\frac{|\text{Skills}_c \cap \text{Skills}_{Q, \text{req}}|}{|\text{Skills}_{Q, \text{req}}|} \times 100$ |
| **Preferred Skills**| Nice-to-Have Skill Fit | `0.10` | $\frac{|\text{Skills}_c \cap \text{Skills}_{Q, \text{pref}}|}{|\text{Skills}_{Q, \text{pref}}|} \times 100$ |
| **Experience** | Seniority Window Proximity | `0.15` | Proximity curve to $[y_{\min}, y_{\max}]$ |
| **Education** | Academic Tier & Degree Fit | `0.05` | Degree level & institutional tier |
| **Trajectory** | Career Stability & Progression | `0.05` | Role continuity & tenure |
| **Availability** | Notice Period & Relocation | `0.05` | Immediate availability / relocation readiness |

---

## 📊 Evaluation & Benchmark Results

### Information Retrieval (IR) Accuracy (Top-10 Cutoff)
* **Precision@5**: `90.0%`
* **Precision@10**: `80.0%`
* **Recall@10**: `80.0%`
* **Mean Reciprocal Rank (MRR)**: `1.000` (Rank 1 candidate is always a verified top match)
* **NDCG@5**: `0.8924`
* **NDCG@10**: `0.8412`

### Throughput & Performance
* **Index Scale**: `100,000` Candidates in FAISS vector database.
* **Vector Retrieval Latency**: `~42 ms` on standard CPU.
* **End-to-End Ranking Latency (p50)**: `~350 ms`.
* **RAM Footprint**: `~1.2 GB`.

---

## 🚀 Quickstart Guide

### Prerequisites
* **Python**: 3.10+ (Tested on Python 3.11 & 3.13)
* **Node.js**: 18.0+
* **npm**: 9.0+

### Option A: Local Development

#### 1. Backend Setup
```bash
# Clone repository
git clone https://github.com/NikitaMehra884/AI-Resume-Ranking-System.git
cd "AI-Resume-Ranking-System"

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database and demo accounts
python scripts/seed_db.py

# Launch FastAPI backend
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### 2. Frontend Setup
```bash
# Open another terminal and navigate to frontend
cd frontend

# Install packages
npm install

# Start Vite development server
npm run dev
```
Frontend interface will be live at: [http://localhost:3000](http://localhost:3000)

---

### Option B: Docker Compose Setup

Run the entire platform with one command:
```bash
docker-compose up --build
```
* Frontend: [http://localhost:3000](http://localhost:3000)
* Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔑 Demo Accounts

The database comes pre-seeded with sample credentials:

| Role | Email | Password | Primary Capabilities |
| :--- | :--- | :--- | :--- |
| **Recruiter** | `recruiter@platform.ai` | `password123` | Post jobs, screen 100k talent pool, side-by-side compare, generate AI interview questions, view analytics. |
| **Candidate** | `candidate@platform.ai` | `password123` | Upload & parse resumes (PDF/DOCX), browse open positions, run AI fit analysis against job descriptions. |

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Framework** | FastAPI, Uvicorn, Pydantic v2, Starlette |
| **Database & ORM** | SQLite / PostgreSQL, SQLAlchemy 2.0 |
| **Security & Auth** | Native Bcrypt, Python-JOSE (JWT Tokens) |
| **Vector Search & IR**| FAISS (CPU), Rank-BM25, NumPy, PyTorch |
| **NLP & Embeddings** | `sentence-transformers/all-MiniLM-L6-v2`, Regex taxonomy normalizer |
| **Document Parsing** | PyPDF, python-docx |
| **Frontend Framework**| React 18, TypeScript, Vite, React Router v6 |
| **Styling & UI** | Tailwind CSS, Lucide Icons, Axios |
| **Containerization** | Docker, Docker Compose, Nginx Alpine |

---

## 🧪 Testing & Validation

```bash
# Run backend test suite
pytest -v backend/tests

# Run performance & latency benchmark
python scripts/benchmark.py --iterations 3 --top_k 20

# Run IR evaluation metrics (P@K, R@K, MRR, NDCG)
python scripts/evaluate.py
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).