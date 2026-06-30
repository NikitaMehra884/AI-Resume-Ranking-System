import re


class JobService:

    def extract_experience(self, text):

        text = text.lower()

        text = (
            text.replace("–", "-")
                .replace("—", "-")
        )

        match = re.search(r"(\d+)\s*-\s*(\d+)", text)

        if match:
            return float(match.group(1))

        return 0.0