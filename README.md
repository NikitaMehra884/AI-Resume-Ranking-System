# AI Resume Ranking System

## Overview
A full‑stack AI‑driven recruitment platform built with FastAPI (backend) and React + TypeScript (frontend).

## Quick Start (Windows)
1. **Install backend dependencies**
   ```powershell
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Install frontend dependencies**
   ```powershell
   cd ..\frontend
   npm install
   ```
3. **Run the services** (open two terminals)
   - Backend:
     ```powershell
     cd ..\backend
     uvicorn backend.app.main:app --reload
     ```
   - Frontend (development):
     ```powershell
     cd ..\frontend
     npm run dev
     ```
   Visit `http://localhost:5173`.

## Full verification script
A script `scripts/full_test.py` starts both services, registers a recruiter and a candidate, creates a job, uploads a dummy resume, applies, and verifies the applicant appears.
Run it with:
```powershell
cd scripts
python full_test.py
```
It prints **PASS** or **FAIL** and shuts down the services.

---
Enjoy building smarter hiring experiences!