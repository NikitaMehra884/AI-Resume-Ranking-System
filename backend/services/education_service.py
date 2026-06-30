class EducationService:

    def calculate_score(self, education):

        if not education:
            return 0

        score = 0

        for degree in education:

            field = degree.get("field_of_study", "").lower()
            tier = degree.get("tier", "").lower()

            if any(keyword in field for keyword in [
                "computer",
                "artificial intelligence",
                "machine learning",
                "data science",
                "information technology",
                "software"
            ]):
                score += 60
            else:
                score += 30

            if tier == "tier_1":
                score += 40
            elif tier == "tier_2":
                score += 30
            elif tier == "tier_3":
                score += 20
            else:
                score += 10

        return round(min(score / len(education), 100), 2)