# 4-Stage Hybrid Retrieval & Multi-Signal Ranking Algorithm

## 1. Overview of the 4 Stages

The core intelligence of the platform resides in the **4-Stage Hybrid Ranking Engine**, designed to eliminate common failure modes of early ATS prototypes (such as ranking Customer Support above AI Engineers due to unconstrained BM25 keyword matching).

```
[Job Mandate]
      │
      ▼
Stage 1: Hard Eligibility Filters (Role Alignment, Minimum Seniority, Location)
      │
      ▼
Stage 2: Hybrid Retrieval (FAISS Dense Vector Search ∪ BM25Okapi Lexical Search)
      │
      ▼
Stage 3: Normalized Multi-Signal Scoring (8 Independent Signals, strictly in [0, 100])
      │
      ▼
Stage 4: Top-K Shortlist & Grounded Explainability
```

---

## 2. Mathematical Formalism

### 2.1 Stage 1: Hard Eligibility Filtering
Candidates are filtered against non-negotiable job requirements before ranking:
* **Role Alignment**: If the job title represents a software or machine learning role (`Engineer`, `Developer`, `Scientist`, `Architect`), candidates whose latest title contains non-engineering terms (`Customer Support`, `Sales Executive`, `HR Recruiter`) are eliminated.
* **Seniority Boundary**: If $y_{\text{candidate}} < y_{\text{job\_min}} - 2.0$, candidate is disqualified from senior/lead roles.
* **Location & Work Mode**: Candidates outside target location are filtered unless `work_mode == "remote"` or candidate has `willing_to_relocate == true`.

### 2.2 Stage 2: Hybrid Dense-Sparse Candidate Retrieval
Let $Q$ be the parsed job description.
1. **Dense Semantic Retrieval**:
   $$\mathbf{e}_Q = \text{SentenceTransformer}(Q)$$
   The top $N=1,500$ candidates are retrieved from the FAISS inner-product index:
   $$\mathcal{C}_{\text{dense}} = \text{Top-N}_{\mathbf{e}_i \in \text{FAISS}} \left( \mathbf{e}_Q \cdot \mathbf{e}_i \right)$$
   Dense vector score is normalized:
   $$S_{\text{dense}} = \max(0, \min(100, (\mathbf{e}_Q \cdot \mathbf{e}_i) \times 100))$$

2. **Sparse Lexical Retrieval**:
   Using tokenized candidate documents $\mathcal{D}$:
   $$\text{BM25}(Q, D_i) = \sum_{q \in Q} \text{IDF}(q) \cdot \frac{f(q, D_i) \cdot (k_1 + 1)}{f(q, D_i) + k_1 \cdot \left(1 - b + b \cdot \frac{|D_i|}{\text{avgdl}}\right)}$$
   BM25 scores are normalized across retrieved candidates:
   $$S_{\text{bm25}} = \frac{\text{BM25}(Q, D_i)}{\max_{j} \text{BM25}(Q, D_j)} \times 100$$
   The retrieved candidate pool is the union $\mathcal{C} = \mathcal{C}_{\text{dense}} \cup \mathcal{C}_{\text{sparse}}$.

### 2.3 Stage 3: Multi-Signal Normalized Scoring
The final score $S_{\text{final}} \in [0, 100]$ is a weighted linear combination of 8 independent, normalized sub-scores:

$$S_{\text{final}} = \sum_{k=1}^{8} w_k \cdot S_k, \quad \sum_{k=1}^{8} w_k = 1.0$$

| Signal | Metric Symbol | Default Weight $w_k$ | Description |
| :--- | :---: | :---: | :--- |
| **Dense Semantic** | $S_{\text{dense}}$ | 0.25 | SentenceTransformer cosine similarity. |
| **Sparse Lexical** | $S_{\text{bm25}}$ | 0.10 | BM25Okapi exact keyword matching. |
| **Required Skills** | $S_{\text{req}}$ | 0.25 | $\frac{|\text{Skills}_{\text{candidate}} \cap \text{Skills}_{\text{job, req}}|}{|\text{Skills}_{\text{job, req}}|} \times 100$ |
| **Preferred Skills** | $S_{\text{pref}}$ | 0.10 | $\frac{|\text{Skills}_{\text{candidate}} \cap \text{Skills}_{\text{job, pref}}|}{|\text{Skills}_{\text{job, pref}}|} \times 100$ |
| **Experience Fit** | $S_{\text{exp}}$ | 0.15 | Proximity to target experience window $[y_{\min}, y_{\max}]$. |
| **Education Tier** | $S_{\text{edu}}$ | 0.05 | Degree level and institution prestige tier. |
| **Career Trajectory**| $S_{\text{career}}$| 0.05 | Recency of role, tenure stability, promotion progression. |
| **Availability** | $S_{\text{avail}}$ | 0.05 | Notice period $\le 30$ days, relocation willingness. |

### 2.4 Stage 4: Top-K Shortlist & Grounded Explainability
Candidates are sorted descending by $S_{\text{final}}$. The top $K$ candidates are returned:
$$\text{Shortlist} = \text{Top-}K_{c \in \mathcal{C}}(S_{\text{final}}(c))$$

For each shortlisted candidate, an **Explainable Grounded Evidence Report** is generated:
* **Grounded Strengths**: Specific overlapping skills that contributed positively to $S_{\text{req}}$ and $S_{\text{pref}}$.
* **Skill Gaps**: Exact mandatory skills missing from the candidate's verified profile.
* **Experience Justification**: Comparison of candidate's verified tenure against job mandate.
* **Why Ranked**: Natural language summary linking scores to factual resume evidence.
