class NoticePeriodService:

    def calculate_score(self, signals):

        days = signals.get(
            "notice_period_days",
            90
        )

        if days <= 30:
            return 100

        if days <= 60:
            return 80

        if days <= 90:
            return 60

        return 40