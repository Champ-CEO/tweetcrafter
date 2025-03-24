import os
from enum import Enum
from pathlib import Path


class Model(Enum):
    GPT_4o = "gpt-4o"
    LLAMA_3 = "Llama3"
    GROQ_LLAMA3 = "groq-llama3"
    SAMBANOVA_DEEPSEEK = "sambanova-deepseek"


class Config:
    class Path:
        APP_HOME = Path(os.getenv("APP_HOME", Path(__file__).parent.parent))
        DATA_DIR = APP_HOME / "data"
        OUTPUT_DIR = APP_HOME / "output"
        LOGS_DIR = APP_HOME / "logs"
        AGENT_LOGS_DIR = LOGS_DIR / "agents"

    MODEL = Model.GROQ_LLAMA3
    LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY", "")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY", "")
