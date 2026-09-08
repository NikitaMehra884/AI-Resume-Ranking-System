import argparse
import json
import random
import sys
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[1]

FIRST_NAMES = ["Aarav", "Aditi", "Ananya", "Dev", "Diya", "Ishaan", "Kavya", "Manish", "Neha", "Pooja", "Rahul", "Riya", "Rohan", "Siddharth", "Tanvi", "Varun", "Vikram", "Zara", "Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Mehra", "Gupta", "Kapoor", "Sethi", "Nair", "Iyer", "Rao", "Reddy", "Singh", "Das", "Menon", "Joshi", "Choudhury", "Bose", "Miller", "Smith", "Johnson", "Williams", "Brown"]

DOMAINS = [
    {
        "domain": "AI/ML",
        "titles": ["Senior AI Engineer", "AI Engineer", "Machine Learning Engineer", "NLP Scientist", "Computer Vision Engineer", "Lead Data Scientist", "Data Scientist"],
        "skills": ["python", "pytorch", "tensorflow", "scikit-learn", "faiss", "llm", "rag", "transformers", "langchain", "huggingface", "fastapi", "docker", "sql", "fine-tuning"]
    },
    {
        "domain": "Backend",
        "titles": ["Senior Backend Engineer", "Backend Developer", "Staff Software Engineer", "Distributed Systems Engineer", "API Engineer"],
        "skills": ["python", "go", "java", "fastapi", "django", "spring boot", "postgresql", "redis", "kafka", "docker", "kubernetes", "aws", "git", "microservices"]
    },
    {
        "domain": "Data Engineering",
        "titles": ["Senior Data Engineer", "Data Infrastructure Engineer", "Big Data Engineer", "Analytics Engineer"],
        "skills": ["python", "sql", "spark", "airflow", "kafka", "snowflake", "databricks", "postgresql", "dbt", "aws", "hadoop", "docker"]
    },
    {
        "domain": "Frontend/Fullstack",
        "titles": ["Full Stack Engineer", "Senior Frontend Engineer", "Frontend Developer", "Web Applications Engineer"],
        "skills": ["typescript", "javascript", "react", "next.js", "node.js", "tailwind", "html", "css", "postgresql", "rest api", "git", "redux"]
    },
    {
        "domain": "DevOps/Cloud",
        "titles": ["DevOps Engineer", "Site Reliability Engineer", "Cloud Architect", "Infrastructure Engineer"],
        "skills": ["linux", "docker", "kubernetes", "terraform", "aws", "gcp", "ci/cd", "git", "python", "bash", "prometheus", "ansible"]
    }
]

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Meta", "Apple", "Uber", "Adobe", "Salesforce", "Atlassian", "Stripe",
    "Swiggy", "Zomato", "Flipkart", "Razorpay", "PhonePe", "Groww", "CRED", "Meesho", "Postman", "BrowserStack",
    "TCS", "Infosys", "Wipro", "Capgemini", "Accenture", "Cognizant", "Mindtree", "Persistent", "LTIMindtree"
]

LOCATIONS = [
    ("Pune", "India"), ("Noida", "India"), ("Bangalore", "India"), ("Hyderabad", "India"),
    ("Delhi NCR", "India"), ("Mumbai", "India"), ("San Francisco", "USA"), ("Toronto", "Canada"),
    ("London", "UK"), ("Berlin", "Germany")
]

UNIVERSITIES = [
    ("IIT Bombay", "tier_1"), ("IIT Delhi", "tier_1"), ("IIT Madras", "tier_1"), ("BITS Pilani", "tier_1"),
    ("IIIT Hyderabad", "tier_1"), ("NIT Trichy", "tier_2"), ("DTU", "tier_2"), ("VIT Vellore", "tier_2"),
    ("Manipal University", "tier_2"), ("SRM University", "tier_3"), ("Pune University", "tier_3"),
    ("Stanford University", "tier_1"), ("UC Berkeley", "tier_1"), ("University of Toronto", "tier_1")
]

DEGREES = [
    ("B.Tech", "Computer Science"), ("B.E.", "Information Technology"), ("M.Tech", "Artificial Intelligence"),
    ("M.S.", "Computer Science"), ("B.S.", "Data Science"), ("Ph.D.", "Computer Science & Machine Learning")
]

def generate_candidate(idx: int) -> Dict[str, Any]:
    cid = f"CAND_{idx:07d}"
    dom = random.choice(DOMAINS)
    title = random.choice(dom["titles"])
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    name = f"{fname} {lname}"

    yoe = round(random.uniform(1.0, 15.0), 1)
    loc, country = random.choice(LOCATIONS)
    company = random.choice(COMPANIES)

    # Sample skills from domain and general pool
    cand_skills_names = random.sample(dom["skills"], k=min(len(dom["skills"]), random.randint(4, 9)))
    # Add 1-2 random secondary skills
    other_skills = ["git", "linux", "sql", "rest", "docker"]
    for s in other_skills:
        if s not in cand_skills_names and random.random() > 0.6:
            cand_skills_names.append(s)

    skills = [{
        "name": s,
        "proficiency": random.choice(["intermediate", "advanced", "expert"]),
        "endorsements": random.randint(5, 75),
        "duration_months": int(random.uniform(0.3, 1.0) * yoe * 12)
    } for s in cand_skills_names]

    # Education
    uni, tier = random.choice(UNIVERSITIES)
    deg, field = random.choice(DEGREES)
    grad_year = 2024 - int(yoe)
    education = [{
        "institution": uni,
        "degree": deg,
        "field_of_study": field,
        "start_year": grad_year - 4,
        "end_year": grad_year,
        "grade": f"{round(random.uniform(7.5, 9.8), 2)} CGPA",
        "tier": tier
    }]

    # Career history
    num_jobs = min(4, max(1, int(yoe // 2.5)))
    career = []
    curr_date = 2024
    for j_idx in range(num_jobs):
        dur_months = int((yoe * 12) // num_jobs)
        c_name = random.choice(COMPANIES)
        c_title = title if j_idx == 0 else f"Junior {title.replace('Senior ', '').replace('Lead ', '')}"
        is_curr = (j_idx == 0)
        career.append({
            "company": c_name,
            "title": c_title,
            "start_date": f"{curr_date - 2}-01-01",
            "end_date": None if is_curr else f"{curr_date}-01-01",
            "duration_months": dur_months,
            "is_current": is_curr,
            "industry": "Technology",
            "company_size": "10001+",
            "description": f"Architected high-throughput services using {', '.join(cand_skills_names[:3])}. Improved query response times by 35% and maintained 99.9% uptime."
        })
        curr_date -= 2

    # Redrob engagement signals
    redrob = {
        "profile_completeness_score": random.randint(75, 100),
        "signup_date": "2023-01-15",
        "last_active_date": "2024-03-01",
        "open_to_work_flag": random.choice([True, True, True, False]),
        "profile_views_received_30d": random.randint(5, 65),
        "applications_submitted_30d": random.randint(1, 15),
        "recruiter_response_rate": round(random.uniform(0.4, 0.95), 2),
        "avg_response_time_hours": random.randint(2, 48),
        "skill_assessment_scores": {s: random.randint(65, 98) for s in cand_skills_names[:3]},
        "notice_period_days": random.choice([15, 30, 60, 90]),
        "preferred_work_mode": random.choice(["remote", "hybrid", "flexible"]),
        "willing_to_relocate": random.choice([True, False]),
        "github_activity_score": random.randint(20, 95),
        "verified_email": True,
        "verified_phone": True,
        "linkedin_connected": True
    }

    summary = (
        f"{title} with {yoe:.1f} years of experience designing and implementing scalable {dom['domain']} systems. "
        f"Specialized in {', '.join(cand_skills_names[:4])}. Proven track record across product companies."
    )

    return {
        "candidate_id": cid,
        "profile": {
            "anonymized_name": name,
            "headline": f"{title} | {', '.join(cand_skills_names[:3])}",
            "summary": summary,
            "location": loc,
            "country": country,
            "years_of_experience": yoe,
            "current_title": title,
            "current_company": company,
            "current_company_size": "10001+",
            "current_industry": "Technology"
        },
        "skills": skills,
        "career_history": career,
        "education": education,
        "redrob_signals": redrob
    }

def main():
    parser = argparse.ArgumentParser(description="Synthetic Candidate Dataset Generator for 1K, 10K, 100K Candidates")
    parser.add_argument("--count", type=int, default=1000, help="Number of candidate records to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--output", type=str, default="data/dataset/synthetic_candidates.jsonl", help="Output path")
    args = parser.parse_args()

    random.seed(args.seed)
    out_path = ROOT / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating {args.count:,} candidates with seed {args.seed}...")
    with open(out_path, "w", encoding="utf-8") as f:
        for i in range(1, args.count + 1):
            cand = generate_candidate(i)
            f.write(json.dumps(cand) + "\\n")
            if i % 25000 == 0:
                print(f"Progress: {i:,} / {args.count:,}")

    print(f"Dataset successfully written to: {out_path}")
    print(f"Total size: {out_path.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
