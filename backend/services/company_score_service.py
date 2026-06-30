class CompanyScoreService:

    PRODUCT_COMPANIES = {

        "Google",
        "Microsoft",
        "Amazon",
        "Meta",
        "Apple",
        "Netflix",
        "Uber",
        "Adobe",
        "NVIDIA",
        "OpenAI",
        "Redrob",

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

        "LinkedIn",
        "Salesforce",
        "Atlassian",
        "Stripe",
        "Airbnb",
        "Spotify",
        "Intel",
        "AMD",
        "Qualcomm",
        "Oracle",
        "SAP"
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
        "L&T Technology Services",
        "Persistent",
        "Mphasis",
        "Virtusa",
        "Hexaware",
        "IBM",
        "DXC",
        "EPAM"
    }

    STARTUPS = {

        "Zepto",
        "Juspay",
        "Unacademy",
        "Upstox",
        "ShareChat",
        "Gupshup",
        "Acko",
        "BlackBuck",
        "Ninjacart"
    }

    def calculate_score(self, company):

        if not company:
            return 50

        company = company.strip()

        # Case-insensitive matching
        product = {c.lower() for c in self.PRODUCT_COMPANIES}
        service = {c.lower() for c in self.SERVICE_COMPANIES}
        startup = {c.lower() for c in self.STARTUPS}

        company_lower = company.lower()

        if company_lower in product:
            return 100

        if company_lower in startup:
            return 90

        if company_lower in service:
            return 70

        return 80