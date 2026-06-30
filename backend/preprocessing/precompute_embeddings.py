import pickle
from pathlib import Path

import numpy as np

from backend.modules.candidate_loader import CandidateLoader
from backend.services.semantic_service import SemanticService
from backend.services.document_builder import DocumentBuilder

class PrecomputeEmbeddings:

    def __init__(self):

        self.loader = CandidateLoader()

        self.semantic_service = SemanticService()

        self.document_builder = DocumentBuilder()

        self.project_root = Path(__file__).resolve().parents[2]

        self.cache_dir = (

            self.project_root

            / "cache"

        )

        self.cache_dir.mkdir(

            exist_ok=True

        )

    # =====================================
    # Generate Candidate Documents
    # =====================================

    def generate_documents(

        self,

        batch

    ):

        documents = []

        candidate_ids = []

        for candidate in batch:

            document = (

                self.document_builder
                .build_candidate_document(

                    candidate

                )

            )

            documents.append(

                document

            )

            candidate_ids.append(

                candidate.candidate_id

            )

        return (

            candidate_ids,

            documents

        )

    # =====================================
    # Precompute
    # =====================================

    def build(

        self,

        batch_size=512

    ):

        all_embeddings = []

        all_candidate_ids = []

        all_documents = []

        processed = 0

        print("=" * 70)
        print("PRECOMPUTING CANDIDATE EMBEDDINGS")
        print("=" * 70)

        for batch in self.loader.load_candidate_batches(

            batch_size=batch_size

        ):

            candidate_ids, documents = (

                self.generate_documents(

                    batch

                )

            )

            embeddings = (

                self.semantic_service.batch_embedding(

                    documents

                )

            )
            all_embeddings.append(
                embeddings
            )

            all_candidate_ids.extend(
                candidate_ids
            )

            all_documents.extend(
                documents
            )

            processed += len(batch)

            print(
                f"Processed : {processed}"
            )

        # =====================================
        # Merge Embeddings
        # =====================================

        print("\nSaving Cache...")

        all_embeddings = np.vstack(
            all_embeddings
        )

        # =====================================
        # Save Embeddings
        # =====================================

        np.save(

            self.cache_dir
            / "candidate_embeddings.npy",

            all_embeddings

        )

        # =====================================
        # Save Candidate IDs
        # =====================================

        with open(

            self.cache_dir
            / "candidate_ids.pkl",

            "wb"

        ) as file:

            pickle.dump(

                all_candidate_ids,

                file

            )

        # =====================================
        # Save Candidate Documents
        # =====================================

        with open(

            self.cache_dir
            / "candidate_documents.pkl",

            "wb"

        ) as file:

            pickle.dump(

                all_documents,

                file

            )

        print("\nCache Generated Successfully")

        print(
            f"Total Candidates : {processed}"
        )

        print(
            f"Embeddings Shape : "
            f"{all_embeddings.shape}"
        )


# ===========================================
# Main
# ===========================================

def main():

    precompute = PrecomputeEmbeddings()

    precompute.build()


if __name__ == "__main__":

    main()