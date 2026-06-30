class RedrobService:

    def calculate_score(self, signals):

        score = 0.0

        # =====================================
        # Profile Completeness (20)
        # =====================================

        profile = signals.get(
            "profile_completeness_score",
            0
        )

        profile = max(0, min(profile, 100))

        score += (profile / 100) * 20

        # =====================================
        # Recruiter Response Rate (20)
        # Handles both 0-1 and 0-100 values
        # =====================================

        response = signals.get(
            "recruiter_response_rate",
            0
        )

        if response > 1:
            response /= 100

        response = max(0, min(response, 1))

        score += response * 20

        # =====================================
        # GitHub Activity (15)
        # =====================================

        github = signals.get(
            "github_activity_score",
            0
        )

        github = max(0, min(github, 10))

        score += (github / 10) * 15

        # =====================================
        # Skill Assessments (20)
        # =====================================

        assessments = signals.get(
            "skill_assessment_scores",
            {}
        )

        if assessments:

            avg = (
                sum(assessments.values())
                / len(assessments)
            )

            avg = max(0, min(avg, 100))

            score += (avg / 100) * 20

        # =====================================
        # Open To Work (10)
        # =====================================

        if signals.get("open_to_work_flag", False):
            score += 10

        # =====================================
        # Verified Email (5)
        # =====================================

        if signals.get("verified_email", False):
            score += 5

        # =====================================
        # Verified Phone (5)
        # =====================================

        if signals.get("verified_phone", False):
            score += 5

        # =====================================
        # LinkedIn Connected (5)
        # =====================================

        if signals.get("linkedin_connected", False):
            score += 5

        # =====================================
        # Clamp Final Score
        # =====================================

        score = max(0, min(score, 100))

        return round(score, 2)