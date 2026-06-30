class CareerService:

    PRODUCT_COMPANIES = {

        "Google",
        "Microsoft",
        "Amazon",
        "Meta",
        "Apple",
        "Netflix",
        "Uber",
        "Airbnb",
        "Stripe",
        "Adobe",
        "Salesforce",
        "Atlassian",
        "Redrob",

        # Indian Product Companies
        "Swiggy",
        "Zomato",
        "Flipkart",
        "PhonePe",
        "Meesho",
        "Razorpay",
        "Groww",
        "Dream11",
        "CRED",
        "Myntra",
        "Ola",
        "Freshworks",
        "BrowserStack",
        "Postman",
        "InMobi",

        # Others
        "Oracle",
        "SAP",
        "NVIDIA",
        "Intel",
        "AMD",
        "Qualcomm",
        "PayPal",
        "LinkedIn"
    }

    SERVICE_COMPANIES = {

        "TCS",
        "Infosys",
        "Wipro",
        "HCL",
        "Tech Mahindra",
        "Capgemini",
        "Accenture",
        "Cognizant",
        "Mindtree",
        "LTIMindtree",
        "IBM",
        "DXC",
        "EPAM",
        "Virtusa",
        "Persistent",
        "Hexaware",
        "Mphasis"
    }

    STARTUPS = {

        "Mad Street Den",
        "Zepto",
        "Juspay",
        "ShareChat",
        "BlackBuck",
        "Ninjacart",
        "Acko",
        "Gupshup",
        "Unacademy"
    }

    # =====================================
    # Company Type
    # =====================================

    def company_type(self, company: str):

        if not company:
            return "Unknown"

        company = company.strip().lower()

        product = {
            c.lower() for c in self.PRODUCT_COMPANIES
        }

        service = {
            c.lower() for c in self.SERVICE_COMPANIES
        }

        startup = {
            c.lower() for c in self.STARTUPS
        }

        if company in product:
            return "Product"

        if company in startup:
            return "Startup"

        if company in service:
            return "Service"

        return "Other"

    # =====================================
    # Experience
    # =====================================

    def calculate_total_experience(
        self,
        career_history
    ):

        total_months = sum(

            job.get(
                "duration_months",
                0
            )

            for job in career_history

        )

        return round(
            total_months / 12,
            2
        )

    # =====================================
    # Current Company
    # =====================================

    def current_company(
        self,
        career_history
    ):

        for job in career_history:

            if job.get("is_current"):

                return job.get(
                    "company",
                    "Unknown"
                )

        return "Unknown"

    # =====================================
    # Current Role
    # =====================================

    def current_role(
        self,
        career_history
    ):

        for job in career_history:

            if job.get("is_current"):

                return job.get(
                    "title",
                    "Unknown"
                )

        return "Unknown"

    # =====================================
    # Total Jobs
    # =====================================

    def total_jobs(
        self,
        career_history
    ):

        return len(career_history)

    # =====================================
    # Average Job Duration
    # =====================================

    def average_job_duration(
        self,
        career_history
    ):

        if not career_history:
            return 0

        total_months = sum(

            job.get(
                "duration_months",
                0
            )

            for job in career_history

        )

        return round(
            total_months /
            len(career_history),
            2
        )