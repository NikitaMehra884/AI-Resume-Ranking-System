import csv
import os


class CSVExportService:

    def export_top_candidates(

        self,

        ranked_candidates,

        output_path="backend/outputs/top_candidates.csv"

    ):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        with open(

            output_path,

            "w",

            newline="",

            encoding="utf-8"

        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                "Rank",

                "Candidate ID",

                "Name",

                "Current Role",

                "Company",

                "Experience",

                "Final Score",

                "Skill Score",

                "Experience Score",

                "Education Score",

                "Career Score",

                "Semantic Score",

                "BM25 Score"

            ])

            for rank, result in enumerate(

                ranked_candidates,

                start=1

            ):

                candidate = result["candidate"]

                writer.writerow([

                    rank,

                    candidate.candidate_id,

                    candidate.name,

                    candidate.current_title,

                    candidate.current_company,

                    candidate.years_of_experience,

                    result["final_score"],

                    result["skill_score"],

                    result["experience_score"],

                    result["education_score"],

                    result["career_relevance"],

                    result["semantic_score"],

                    result["bm25_score"]

                ])

        print(
            f"\nCSV exported successfully -> {output_path}"
        )