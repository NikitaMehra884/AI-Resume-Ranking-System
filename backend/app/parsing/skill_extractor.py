import re
from typing import List, Set

class SkillExtractor:
    """Extracts and normalizes technical and domain skills with alias mapping."""
    
    SKILLS = {
        # Programming & Core
        "python", "java", "c", "c++", "c#", "javascript", "typescript", "go", "rust", "scala", "kotlin", "ruby", "php", "swift",
        # AI / ML / NLP / LLMs
        "machine learning", "deep learning", "artificial intelligence", "natural language processing", "nlp",
        "neural networks", "computer vision", "transformers", "bert", "gpt", "llm", "rag",
        "prompt engineering", "fine-tuning", "lora", "qlora", "peft", "huggingface", "langchain", "langgraph",
        "ollama", "vllm", "llamaindex", "sentence-transformers", "embeddings", "reranking",
        # Vector DBs & Search
        "faiss", "pinecone", "milvus", "weaviate", "qdrant", "chromadb", "elasticsearch", "opensearch", "bm25",
        # ML Frameworks & Libs
        "tensorflow", "keras", "pytorch", "scikit-learn", "xgboost", "lightgbm", "pandas", "numpy", "scipy", "opencv",
        # Backend & Architecture
        "fastapi", "flask", "django", "spring", "spring boot", "node.js", "express", "graphql", "rest", "rest api", "microservices",
        # Frontend
        "react", "angular", "vue", "next.js", "html", "css", "tailwind", "redux",
        # Databases & Storage
        "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "cassandra", "dynamodb",
        # Data Engineering & Cloud
        "spark", "pyspark", "hadoop", "airflow", "kafka", "snowflake", "databricks", "dbt",
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "git", "github", "linux"
    }

    ALIASES = {
        "open ai": "openai",
        "hugging face": "huggingface",
        "lang chain": "langchain",
        "lang graph": "langgraph",
        "vector database": "faiss",
        "vector db": "faiss",
        "retrieval augmented generation": "rag",
        "large language model": "llm",
        "large language models": "llm",
        "tf": "tensorflow",
        "sklearn": "scikit-learn",
        "postgres": "postgresql",
        "mongo": "mongodb",
        "gen ai": "generative ai",
        "generative ai": "llm",
        "llms": "llm",
        "fine tuning": "fine-tuning",
        "fine-tuning llms": "fine-tuning",
        "prompt engineering": "prompt engineering",
        "py-torch": "pytorch",
        "node": "node.js",
        "nodejs": "node.js"
    }

    def __init__(self):
        self.multi_word_skills = sorted([s for s in self.SKILLS if " " in s or "-" in s], key=len, reverse=True)
        self.single_word_skills = sorted([s for s in self.SKILLS if " " not in s and "-" not in s])

    def normalize(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        for old, new in self.ALIASES.items():
            text = re.sub(rf"\b{re.escape(old)}\b", new, text)
        return text

    def extract_skills(self, text: str) -> List[str]:
        if not text:
            return []
        normalized = self.normalize(text)
        found: Set[str] = set()

        # Multi-word match first
        for skill in self.multi_word_skills:
            pattern = rf"\b{re.escape(skill)}\b"
            if re.search(pattern, normalized):
                found.add(skill)

        # Single-word match on word tokens (strip trailing punctuation like periods or commas)
        raw_words = re.findall(r"[a-zA-Z0-9\-\+\.#]+", normalized)
        words = {w.strip(".,:;!?") for w in raw_words}
        for skill in self.single_word_skills:
            if skill in words:
                found.add(skill)

        return sorted(found)
