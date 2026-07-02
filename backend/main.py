import importlib
import sys
import time


TOP_K = 100
BATCH_SIZE = 512


def check_dependencies():
    required_modules = [
        ("numpy", "numpy"),
        ("faiss", "faiss-cpu (or faiss)"),
        ("sentence_transformers", "sentence-transformers"),
        ("sklearn", "scikit-learn"),
        ("rank_bm25", "rank_bm25"),
    ]

    missing = []

    for module_name, display_name in required_modules:
        try:
            importlib.import_module(module_name)
        except (ImportError, ModuleNotFoundError):
            missing.append(display_name)

    if missing:
        print("Missing Python packages:", ", ".join(missing))
        print("Please install dependencies:")
        print("    pip install -r requirements.txt")
        print(f"Interpreter: {sys.executable}")
        sys.exit(1)


def main():

    # ensure dependencies are present before importing project modules
    check_dependencies()

    # local imports to avoid ModuleNotFoundError during module import
    from backend.modules.candidate_loader import CandidateLoader
    from backend.modules.job_loader import JobLoader

    from backend.pipelines.ranking_pipeline import RankingPipeline
    from backend.pipelines.report_pipeline import ReportPipeline
    from backend.services.csv_export_service import CSVExportService
    from backend.services.submission_service import SubmissionService

    start_time = time.perf_counter()

    print("=" * 70)
    print("AI Resume Ranking System")
    print("=" * 70)

    # =====================================
    # Load Job
    # =====================================

    job_loader = JobLoader()
    job = job_loader.load_job()

    # =====================================
    # Load Candidates
    # =====================================

    loader = CandidateLoader()

    # =====================================
    # Pipelines
    # =====================================

    ranking_pipeline = RankingPipeline(

        top_k=TOP_K,

        batch_size=BATCH_SIZE

    )

    report_pipeline = ReportPipeline()
    csv_service = CSVExportService()
    submission_service = SubmissionService()

    # =====================================
    # Rank Candidates
    # =====================================

    result = ranking_pipeline.rank_candidates(

        loader,

        job

    )

    ranked_candidates = result["ranked_candidates"]

    # =====================================
    # Top Candidates
    # =====================================

    report_pipeline.print_top_candidates(

        ranked_candidates

    )

    # =====================================
    # Best Candidate Report
    # =====================================

    report_pipeline.print_best_candidate(

        ranked_candidates,

        ranking_pipeline.candidate_ranker,

        job

    )
    csv_service.export_top_candidates(
        ranked_candidates
    )
    submission_service.export_submission(
        ranked_candidates
    )

    # =====================================
    # Execution Time
    # =====================================

    end_time = time.perf_counter()

    print("\n")
    print("=" * 70)
    print(
        f"Execution Time : "
        f"{end_time - start_time:.2f} seconds"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()