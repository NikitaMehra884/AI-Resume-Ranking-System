import os
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
import streamlit as st

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="AI Resume Ranking System",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# Constants
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent

OUTPUT_DIR = PROJECT_ROOT / "backend" / "outputs"

SUBMISSION_FILE = OUTPUT_DIR / "submission.csv"

TOP_FILE = OUTPUT_DIR / "top_candidates.csv"

# ==========================================
# Header
# ==========================================

st.title("🤖 AI Resume Ranking System")

st.markdown(
"""
### Semantic Search + FAISS + Hybrid AI Ranking

This system ranks candidates using:

- Semantic Embeddings
- FAISS Vector Search
- BM25
- Skill Matching
- Experience
- Education
- Career Relevance
- Explainable AI Scoring
"""
)

# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.header("⚙ Configuration")

    top_k = st.slider(
        "Top Candidates",
        min_value=10,
        max_value=100,
        value=100
    )

    st.divider()

    st.success("Dataset Job Description will be used.")

    st.info(
        "The ranking will use the provided "
        "job_description.docx from the dataset."
    )

    run_button = st.button(
        "🚀 Rank Candidates",
        use_container_width=True
    )

# ==========================================
# Main Placeholders
# ==========================================

status = st.empty()

progress = st.progress(0)

timer = st.empty()
# ==========================================
# Run Ranking Pipeline
# ==========================================

if run_button:

    status.info("🚀 Starting AI Resume Ranking...")

    progress.progress(10)

    start_time = time.perf_counter()

    try:

        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        hf_home = str(Path.home() / ".cache" / "huggingface")
        env["HF_HUB_OFFLINE"] = "1"
        env["HF_HOME"] = hf_home
        env["TRANSFORMERS_CACHE"] = str(Path(hf_home) / "transformers")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "backend.main"
            ],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            env=env,
        )

        progress.progress(80)

        if result.returncode != 0:

            st.error("❌ Backend execution failed")
            st.code(result.stdout)

            st.code(result.stderr)

            st.stop()

        end_time = time.perf_counter()

        runtime = end_time - start_time

        progress.progress(100)

        status.success("✅ Ranking Completed Successfully")

        timer.metric(

            "Execution Time",

            f"{runtime:.2f} sec"

        )

        with st.expander("Backend Console Output"):

            st.code(result.stdout)

    except Exception as e:

        st.error(str(e))

        st.stop()
        # ==========================================
# Display Results
# ==========================================

if run_button:

    if SUBMISSION_FILE.exists():

        st.divider()

        st.header("🏆 Top Ranked Candidates")

        try:

            df = pd.read_csv(SUBMISSION_FILE)

            st.dataframe(
                df,
                use_container_width=True,
                height=600
            )

            st.success(
                f"Showing Top {len(df)} Candidates"
            )

        except Exception as e:

            st.error(f"Unable to read submission.csv\n\n{e}")

    else:

        st.warning("submission.csv not found.")

# ==========================================
# Best Candidate
# ==========================================

if run_button and SUBMISSION_FILE.exists():

    df = pd.read_csv(SUBMISSION_FILE)

    if len(df):

        st.divider()

        st.header("🥇 Best Candidate")

        best = df.iloc[0]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Candidate ID",
            best["candidate_id"]
        )

        c2.metric(
            "Rank",
            best["rank"]
        )

        c3.metric(
            "Score",
            round(float(best["score"]), 2)
        )

        if "reasoning" in df.columns:

            st.subheader("AI Reasoning")

            st.info(best["reasoning"])

# ==========================================
# Downloads
# ==========================================

if run_button:

    st.divider()

    st.header("📥 Download Results")

    if SUBMISSION_FILE.exists():

        with open(SUBMISSION_FILE, "rb") as f:

            st.download_button(

                label="⬇ Download submission.csv",

                data=f,

                file_name="submission.csv",

                mime="text/csv",

                use_container_width=True

            )

    if TOP_FILE.exists():

        with open(TOP_FILE, "rb") as f:

            st.download_button(

                label="⬇ Download top_candidates.csv",

                data=f,

                file_name="top_candidates.csv",

                mime="text/csv",

                use_container_width=True

            )

# ==========================================
# Score Chart
# ==========================================

if run_button and SUBMISSION_FILE.exists():

    df = pd.read_csv(SUBMISSION_FILE)

    if "score" in df.columns:

        st.divider()

        st.header("📈 AI Score Distribution")

        chart = df[["candidate_id", "score"]].copy()

        chart = chart.set_index("candidate_id")

        st.line_chart(chart)

# ==========================================
# Footer
# ==========================================

st.divider()

st.caption(
    "AI Resume Ranking System • Semantic Search + FAISS + Hybrid AI Ranking"
)