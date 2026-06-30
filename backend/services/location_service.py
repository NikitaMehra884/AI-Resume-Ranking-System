class LocationService:

    PREFERRED = {
        "Pune",
        "Noida",
        "Delhi",
        "Delhi NCR",
        "Hyderabad",
        "Bangalore"
    }

    def calculate_score(
        self,
        candidate_location
    ):

        if not candidate_location:
            return 50

        if candidate_location in self.PREFERRED:
            return 100

        return 70