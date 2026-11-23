# HUMEXA – Hire People, Not Just Profiles

## Overview
HUMEXA is a **modern AI‑powered recruitment SaaS platform** that helps companies find the right talent faster and more fairly.  It combines human‑first design with sophisticated machine‑learning models for resume analysis, semantic matching, and candidate ranking.

The project is built with a **React + Vite + TypeScript** front‑end and a **FastAPI** back‑end (Python).  All data is stored in a SQLite database via SQLAlchemy, but the codebase can be switched to Postgres or MySQL with minimal changes.

---

## Table of Contents
1. [Branding – HUMEXA](#branding---humexa)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [Running the Application](#running-the-application)
6. [Backend Details](#backend-details)
7. [Frontend Details](#frontend-details)
8. [API Endpoints](#api-endpoints)
9. [Database Schema](#database-schema)
10. [Testing](#testing)
11. [Deployment](#deployment)
12. [Contribution Guide](#contribution-guide)
13. [License](#license)

---

## Branding – HUMEXA
- **Name**: **HUMEXA**
- **Tagline**: *"Hire People, Not Just Profiles."*
- **Logo**: `frontend/public/humexa-logo.svg` (a minimal abstract human figure with a subtle sparkle to suggest AI).
- **Favicon**: `frontend/public/humexa-favicon.ico`
- **Colors** (defined in `frontend/tailwind.config.js`):
  - Background: `#090D1A`
  - Surface: `#111827`
  - Primary: `#6957F5`
  - Secondary: `#8B7CFF`
  - Accent: `#A78BFA`
  - Text: `#F8FAFC`
  - Muted text: `#94A3B8`
  - Success: `#22C55E`
  - Error: `#EF4444`

All UI components now use these colors to give a premium dark‑navy look with purple gradients and glass‑morphism effects.

---

## Tech Stack
| Layer | Technology | Why we chose it |
|-------|------------|----------------|
| Front‑end | React, Vite, TypeScript, Tailwind CSS | Fast development, hot‑module reloading, type safety, modern utility‑first styling |
| Back‑end | Python 3.11, FastAPI, SQLAlchemy | High performance, automatic OpenAPI docs, easy async support |
| Database | SQLite (dev) – can be swapped to Postgres/MySQL | Simple for local development; SQLAlchemy abstracts the DB |
| Authentication | JWT (Bearer tokens) | Stateless, works well with SPA front‑ends |
| AI / Ranking | Custom Python modules (`backend/app/services/ranking.py`) | Demonstrates how to plug in any ML model |
| Build / Run | npm scripts, pip, uvicorn | Standard tooling for each language |

---

## Project Structure
```
AI Resume Ranking System/      (root)
├─ backend/                    # FastAPI server
│   ├─ app/
│   │   ├─ api/v1/            # Routers (auth, ranking, etc.)
│   │   ├─ core/              # Settings, security helpers
│   │   ├─ models/            # SQLAlchemy ORM models (User, CandidateProfile, RecruiterProfile)
│   │   ├─ schemas/           # Pydantic request/response schemas
│   │   └─ main.py            # Application entry point
│   └─ requirements.txt       # Python dependencies
│
├─ frontend/                   # React SPA
│   ├─ src/
│   │   ├─ components/        # Re‑usable UI components (Button, Navbar, Footer, etc.)
│   │   ├─ pages/             # Page components (LandingPage, Login, Register, CandidateDashboard, RecruiterDashboard)
│   │   ├─ context/           # AuthContext – handles login, token storage, logout
│   │   ├─ services/          # `api.ts` – axios instance pointing to backend
│   │   └─ types/             # TypeScript enums & interfaces
│   ├─ public/                # Static assets (logo, favicon, index.html)
│   ├─ tailwind.config.js    # Custom color palette
│   └─ package.json           # npm scripts, dependencies
│
├─ scripts/                    # Helper scripts (full_test.py, search_branding.py, etc.)
├─ .gitignore
└─ README.md                  # THIS FILE
```

---

## Setup & Installation
### Prerequisites
- **Node.js** (>=18) and **npm**
- **Python** 3.11 and **pip**
- **Git** for version control
- (Optional) **virtualenv** or **conda** for isolated Python env

### 1. Clone the repository
```bash
git clone https://github.com/your‑org/humexa.git
cd "AI Resume Ranking System"
```

### 2. Set up the Python back‑end
```bash
# Create and activate a virtual environment
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Set up the React front‑end
```bash
cd frontend
npm install
```

### 4. Environment variables (optional)
Create a `.env` file in `backend/` if you need to override defaults (e.g., JWT secret, DB path).
```env
# backend/.env
SECRET_KEY=your‑super‑secret‑key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./data/humexa.db
```

---

## Running the Application
### Start the back‑end (development mode)
```bash
# From the project root
.\.venv\Scripts\activate   # PowerShell
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8001
```
The API docs are available at `http://127.0.0.1:8001/docs`.

### Start the front‑end (development mode)
```bash
cd frontend
npm run dev   # Vite dev server, usually http://localhost:3001
```
The UI will automatically proxy API calls to the back‑end because the axios `baseURL` is set to `http://127.0.0.1:8001/api/v1`.

---

## Backend Details
- **Entry point**: `backend/app/main.py` creates the FastAPI app, adds CORS middleware (allowing all origins in dev), and includes the API routers.
- **Auth router** (`backend/app/api/v1/auth.py`):
  - `POST /auth/register` – registers candidates or recruiters, creates related profile rows, returns a JWT.
  - `POST /auth/login` – validates credentials and returns a JWT.
  - `GET /auth/me` – returns current user data (used for role‑based UI).
- **Ranking router** (`backend/app/api/v1/ranking.py` – not shown here but part of the original repo): handles resume upload, AI analysis, and returns ranked candidate lists.
- **Security** (`backend/app/core/security.py`): functions for password hashing (`bcrypt`), verification, and JWT generation.
- **Database** (`backend/app/models/`):
  - `User` – core auth table (`id`, `email`, `hashed_password`, `role`, `is_active`).
  - `CandidateProfile` – stores candidate‑specific fields.
  - `RecruiterProfile` – stores recruiter‑specific fields.

---

## Frontend Details
- **Routing** (`src/App.tsx`): React‑Router v6 defines routes for `/`, `/login`, `/register`, `/candidate`, `/recruiter`.
- **AuthContext** (`src/context/AuthContext.tsx`):
  - Stores JWT in `localStorage`.
  - Provides `login`, `register`, `logout` functions used by pages.
  - Persists the decoded user role for navigation decisions.
- **Pages** (`src/pages/`):
  - `LandingPage.tsx` – hero section with HUMEXA branding.
  - `Login.tsx` – split‑screen design, password visibility toggle, loading spinner.
  - `Register.tsx` – role selection (candidate / recruiter) with inline validation.
  - `CandidateDashboard.tsx` – resume upload, analysis status, matched jobs.
  - `RecruiterDashboard.tsx` – job description input, AI ranking table, filters.
- **Components** (`src/components/common/`):
  - `Button`, `Navbar`, `Footer`, `Alert`, `LoadingSpinner` – all styled with the new palette and glass‑morphism.
- **API client** (`src/services/api.ts`):
  ```ts
  import axios from 'axios';
  const api = axios.create({
    baseURL: 'http://127.0.0.1:8001/api/v1',
    headers: { 'Content-Type': 'application/json' },
  });
  export default api;
  ```
- **Tailwind config** (`tailwind.config.js`): custom colors are added under `theme.extend.colors` – use them as `bg-primary`, `text-accent`, etc.

---

## API Endpoints
| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| `POST` | `/auth/register` | Register a new user (candidate or recruiter) | `{email, password, role, full_name?, company_name?}` | JWT token + user data |
| `POST` | `/auth/login` | Log in and receive a JWT | `{email, password}` | JWT token + user data |
| `GET`  | `/auth/me` | Get current user (requires `Authorization: Bearer <token>`) | – | User object |
| `POST` | `/ranking/upload` | Upload a resume (multipart/form‑data) | `file` | Upload status ID |
| `GET`  | `/ranking/status/<id>` | Check AI analysis status | – | `{status, result}` |
| `GET`  | `/ranking/candidates` | Get list of ranked candidates for a recruiter | – | Array of candidate objects |

All endpoints return proper HTTP status codes (`400` for validation errors, `401` for auth problems, `200` for success). Errors are displayed in the UI via toast notifications.

---

## Database Schema
Key tables (generated by SQLAlchemy):
- **users** (`id`, `email`, `hashed_password`, `role`, `is_active`)
- **candidate_profiles** (`id`, `user_id`, `candidate_id`, `full_name`, `headline`, `years_of_experience`)
- **recruiter_profiles** (`id`, `user_id`, `company_name`, `industry`)
- **resumes**, **jobs**, **rankings** (used by the AI pipeline – not shown in this README but present in `backend/app/models/`)

Migrations are handled by Alembic (if you add new models, run `alembic revision --autogenerate`).

---

## Testing
- **Backend**: Run `pytest` inside the `backend/` folder.  A sample integration test (`scripts/full_test.py`) registers a user, logs in, and checks the token.
- **Frontend**: Use `npm test` (Jest + React Testing Library).  Critical components like `AuthContext`, `Login`, and `Register` have unit tests.
- **End‑to‑end**: Start both servers and visit the UI.  Try registering a candidate, uploading a resume, and confirming the ranking appears.

---

## Deployment
1. **Docker** – two Dockerfiles are provided (`Dockerfile.backend`, `Dockerfile.frontend`). Build images and run with Docker‑Compose.
2. **Cloud** – the backend can be deployed to any platform that supports ASGI (e.g., Cloud Run, AWS Lambda with Mangum). The static front‑end can be hosted on Vercel, Netlify, or S3 + CloudFront.
3. **Environment variables** must be set in production (secure JWT secret, proper CORS origins, database URL).

---

## Contribution Guide
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your‑feature`.
3. Make changes, run linting (`npm run lint`, `ruff check` for Python).
4. Write tests for new code.
5. Submit a Pull Request with a clear description.
6. Ensure CI passes before merging.

---

## License
This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

*Enjoy building with HUMEXA! If you run into any issues, open an issue on the GitHub repository or contact the maintainers.*