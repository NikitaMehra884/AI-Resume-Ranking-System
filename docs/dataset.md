# Dataset Architecture & Preprocessing Methodology

## 1. Dataset Overview

The platform is designed and evaluated on the **Redrob Intelligent Candidate Discovery & Ranking Corpus**, consisting of **100,000 real-world candidate profiles** in JSON Lines format (`data/dataset/candidates.jsonl`, 487 MB).

Each record represents a complete professional candidate profile containing:
* **Identification & Demographics**: `candidate_id` (`CAND_0000001` through `CAND_00100000`), `full_name`, `location`, `country`.
* **Professional Summary**: `headline`, `summary`, `years_of_experience`, `current_title`, `current_company`.
* **Skills Taxonomy**: Extracted technical skills list with proficiency, endorsements, and duration.
* **Career History**: Chronological sequence of previous roles, start/end dates, duration in months, job descriptions.
* **Education**: Degree, institution, field of study, graduation year, academic tier.

---

## 2. Pre-Computed Index Files & Artifacts

To achieve sub-second search over 100,000 candidate profiles without loading the entire 487MB corpus into memory on every request, the platform utilizes pre-indexed binary cache files in `cache/`:

| Artifact | File Size | Description |
| :--- | :--- | :--- |
| `candidate.index` | 153.6 MB | FAISS `IndexFlatIP` containing 100,000 384-dimensional dense vectors. |
| `candidate_embeddings.npy` | 153.6 MB | Raw float32 NumPy matrix of normalized embeddings (`all-MiniLM-L6-v2`). |
| `candidate_ids.pkl` | 1.5 MB | Pickled list of 100,000 ordered `candidate_id` strings matching vector row indices. |
| `candidate_documents.pkl` | 231.2 MB | Pickled list of 100,000 standardized candidate document strings for BM25 indexing. |
| `candidate_offsets.pkl` | 2.0 MB | Byte offset map allowing $O(1)$ random-access file seeks into `candidates.jsonl`. |
| `candidate_bm25.pkl` | Cached | Pickled BM25Okapi inverted index for sparse lexical retrieval. |

---

## 3. High-Throughput Dataset Generator (`scripts/generate_dataset.py`)

For synthetic benchmarking, testing, or environment initialization without external downloads, `scripts/generate_dataset.py` generates thousands of realistic candidate profiles adhering to the Redrob JSONL schema.

### Generating Synthetic Profiles
```bash
# Generate 1,000 synthetic candidates in seconds:
python scripts/generate_dataset.py --count 1000 --output data/synthetic_candidates.jsonl
```

### Schema Structure
```json
{
  "candidate_id": "CAND_0000123",
  "full_name": "Sarah Chen",
  "years_of_experience": 6.5,
  "current_title": "Senior AI Research Engineer",
  "current_company": "Zomato",
  "location": "Bengaluru, India",
  "skills": [
    {"name": "Python", "proficiency": "Expert", "endorsements": 24},
    {"name": "PyTorch", "proficiency": "Advanced", "endorsements": 18},
    {"name": "FAISS", "proficiency": "Advanced", "endorsements": 12},
    {"name": "FastAPI", "proficiency": "Intermediate", "endorsements": 9}
  ],
  "career_history": [
    {
      "company": "Zomato",
      "title": "Senior AI Engineer",
      "start_date": "2022-01",
      "is_current": true,
      "description": "Architected hybrid search pipelines processing 50M queries daily."
    }
  ],
  "education": [
    {
      "institution": "Indian Institute of Technology",
      "degree": "BTech in Computer Science",
      "end_year": 2018
    }
  ]
}
```
