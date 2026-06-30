import csv
import os


class SubmissionService:

    def export_submission(
        self,
        ranked_candidates,
        output_path="backend/outputs/submission.csv"
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
                "candidate_id",
                "rank",
                "score",
                "reasoning"
            ])

            for rank, result in enumerate(
                ranked_candidates,
                start=1
            ):

                candidate = result["candidate"]

                # -----------------------------
                # Normalize score (0-1)
                # -----------------------------

                score = round(
                    result["final_score"] / 100,
                    4
                )

                # -----------------------------
                # AI Skill Count
                # -----------------------------

                skill_count = len(
                    result["matched_skills"]
                )

                # -----------------------------
                # Response Rate
                # -----------------------------

                response_rate = (
                    candidate.redrob_signals.get(
                        "recruiter_response_rate",
                        0
                    )
                )

                if response_rate > 1:
                    response_rate /= 100

                # -----------------------------
                # Reasoning
                # -----------------------------

                reasoning = (

                    f"{candidate.current_title} "

                    f"with "

                    f"{candidate.years_of_experience:.1f} yrs; "

                    f"{skill_count} AI core skills; "

                    f"response rate "

                    f"{response_rate:.2f}."

                )

                writer.writerow([

                    candidate.candidate_id,

                    rank,

                    f"{score:.4f}",

                    reasoning

                ])

        print("\nSubmission CSV Generated Successfully!")
        print(f"Saved to : {output_path}")