from backend.services.semantic_service import SemanticService


class CareerRelevanceService:
    """
    Computes how relevant a candidate's past work
    experience is to the current Job Description.

    Improvements:
    - Job embedding computed once.
    - Career descriptions encoded in batch.
    - Recent jobs get higher weight.
    """

    def __init__(self, semantic_service=None):

        # reuse provided semantic service if available
        self.semantic_service = semantic_service or SemanticService()

    def calculate_score(
        self,
        career_history,
        job_embedding
    ):

        if not career_history:
            return 0.0

        descriptions = []

        for job in career_history:

            description = job.get("description", "").strip()

            if description:
                descriptions.append(description)

        if not descriptions:
            return 0.0

        # Encode all descriptions together (faster)
        description_embeddings = (
            self.semantic_service.batch_embedding(
                descriptions
            )
        )

        similarities = []

        for embedding in description_embeddings:

            score = self.semantic_service.similarity(
                embedding,
                job_embedding
            )

            similarities.append(score)

        # Recent experience gets more weight
        weights = [0.5, 0.3, 0.2]

        final_score = 0.0

        for i, score in enumerate(similarities):

            if i < len(weights):
                final_score += score * weights[i]
            else:
                final_score += score * 0.1

        return round(final_score * 100, 2)