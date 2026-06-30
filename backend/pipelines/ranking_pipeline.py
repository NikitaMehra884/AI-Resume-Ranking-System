import heapq
import time

from backend.services.semantic_service import SemanticService
from backend.services.candidate_ranker import CandidateRanker
from backend.services.document_builder import DocumentBuilder
from backend.retrieval.faiss_service import FAISSService
from backend.services.bm25_service import BM25Service


class RankingPipeline:

    def __init__(

        self,

        top_k=100,

        batch_size=512

    ):

        self.TOP_K = top_k

        self.BATCH_SIZE = batch_size

        self.semantic_service = SemanticService()

        self.document_builder = DocumentBuilder()

        # shared services (singletons where applicable)
        self.faiss_service = FAISSService()
        self.bm25_service = BM25Service()

        # CandidateRanker should reuse the semantic and bm25 services
        self.candidate_ranker = CandidateRanker(
            semantic_service=self.semantic_service,
            bm25_service=self.bm25_service,
        )

    # ==========================================
    # Generate Job Embedding
    # ==========================================

    def build_job_embedding(

        self,

        job

    ):

        print("\nGenerating Job Embedding...")

        return self.semantic_service.embedding(

            job.description

        )

    # ==========================================
    # Rank All Candidates
    # ==========================================

    def rank_candidates(

        self,

        loader,

        job

    ):

        top_candidates = []

        processed = 0

        job_embedding = self.build_job_embedding(job)

        print("\nSearching FAISS for candidate shortlist...\n")
        faiss_start = time.perf_counter()

        # retrieve a shortlist using FAISS (semantic only)
        faiss_results = self.faiss_service.search_candidates(
            job_embedding,
            top_k=1500
        )

        faiss_time = time.perf_counter() - faiss_start

        candidate_ids = [r["candidate_id"] for r in faiss_results]

        # load only shortlisted candidates
        load_start = time.perf_counter()
        candidates = loader.load_candidates_by_ids(candidate_ids)
        load_time = time.perf_counter() - load_start

        # map id -> candidate object
        id_to_candidate = {c.candidate_id: c for c in candidates}

        # cache job skills once
        job_skills = self.candidate_ranker.skill_service.extract_skills(
            job.description
        )

        print("\nRanking Shortlisted Candidates...\n")

        ranking_start = time.perf_counter()

        for r in faiss_results:

            candidate_id = r["candidate_id"]
            embedding_index = r["embedding_index"]

            candidate = id_to_candidate.get(candidate_id)

            if candidate is None:
                continue

            processed += 1

            # build document and fetch cached candidate embedding
            document = self.document_builder.build_candidate_document(candidate)

            candidate_embedding = self.semantic_service.get_candidate_embedding_by_index(
                embedding_index
            )

            result = self.candidate_ranker.rank_candidate(
                candidate,
                document,
                candidate_embedding,
                job,
                job_embedding,
                job_skills=job_skills,
                semantic_service=self.semantic_service,
                candidate_index=embedding_index,
            )

            # ==========================================
            # Maintain Top-K Heap
            # ==========================================

            entry = (
                result["final_score"],
                processed,          # unique tie-breaker
                result
            )

            if len(top_candidates) < self.TOP_K:

                heapq.heappush(
                    top_candidates,
                    entry
                )

            else:

                heapq.heappushpop(
                    top_candidates,
                    entry
                )

            # ==========================================
            # Progress
            # ==========================================

            if processed % 1000 == 0:

                print(
                    f"Processed : {processed}"
                )

        ranking_time = time.perf_counter() - ranking_start

        print(f"\nTotal Candidates Processed : {processed}")
        print(f"FAISS search time     : {faiss_time:.2f} sec")
        print(f"Candidate load time   : {load_time:.2f} sec")
        print(f"Rerank time           : {ranking_time:.2f} sec")

        # ==========================================
        # Sort Top Candidates
        # ==========================================

        ranked_candidates = [

            item[2]

            for item in sorted(
                top_candidates,
                key=lambda x: x[0],
                reverse=True
            )

        ]

        return {

            "ranked_candidates": ranked_candidates,

            "processed": processed,

            "job_embedding": job_embedding

        }