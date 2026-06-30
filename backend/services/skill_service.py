import re


class SkillService:

    def __init__(self):

        self.skills = {

            # Programming
            "python", "java", "c", "c++", "c#", "javascript",
            "typescript", "go", "rust", "scala", "kotlin",

            # AI / ML
            "machine learning", "deep learning", "artificial intelligence",
            "neural networks", "computer vision", "nlp",
            "transformers", "bert", "gpt", "llm", "rag",
            "prompt engineering", "fine tuning", "lora",
            "qlora", "peft", "huggingface",
            "langchain", "langgraph",

            # Vector DB
            "faiss", "pinecone", "milvus",
            "weaviate", "qdrant", "chromadb",

            # ML Frameworks
            "tensorflow", "keras", "pytorch",
            "scikit-learn", "xgboost", "lightgbm",

            # Backend
            "fastapi", "flask", "django",
            "spring", "node.js", "express",

            # Frontend
            "react", "angular", "vue",
            "html", "css", "tailwind",

            # Databases
            "sql", "mysql", "postgresql",
            "mongodb", "redis", "sqlite",

            # Big Data
            "spark", "hadoop", "airflow",
            "kafka", "beam", "snowflake",
            "databricks",

            # Cloud
            "aws", "azure", "gcp",
            "docker", "kubernetes",

            # Search
            "bm25", "elasticsearch",
            "opensearch",

            # APIs
            "rest", "rest api", "graphql",

            # DevOps
            "git", "github",
            "linux", "ci/cd",
            "terraform",

            # Misc
            "opencv",
            "ocr",
            "speech recognition",
            "tts",
            "gan",
            "recommendation systems",

            # LLM Ecosystem
            "ollama",
            "vllm",
            "llamaindex",
            "sentence transformers",
            "embeddings",
            "reranking"
        }

        self.alias = {

            "open ai": "openai",
            "hugging face": "huggingface",
            "lang chain": "langchain",
            "lang graph": "langgraph",
            "vector database": "faiss",
            "vector db": "faiss",
            "retrieval augmented generation": "rag",
            "large language model": "llm",
            "tf": "tensorflow",
            "sklearn": "scikit-learn",
            "postgres": "postgresql",
            "mongo": "mongodb",
            "gen ai": "generative ai",
            "llms": "llm"
        }

    # ==========================================
    # Normalize
    # ==========================================

    def normalize(self, text):

        if not text:
            return ""

        text = text.lower()

        for old, new in self.alias.items():

            text = text.replace(old, new)

        return text

    # ==========================================
    # Skill Extraction
    # ==========================================

    def extract_skills(self, text):

        text = self.normalize(text)

        found = set()

        # Match multi-word skills first
        for skill in self.skills:

            if " " in skill:

                pattern = rf"\b{re.escape(skill)}\b"

                if re.search(pattern, text):

                    found.add(skill)

        # Tokenize once
        words = set(
            re.findall(
                r"[a-zA-Z0-9\-\+\.#]+",
                text
            )
        )

        # Match single-word skills
        for skill in self.skills:

            if " " not in skill:

                if skill in words:

                    found.add(skill)

        return sorted(found)