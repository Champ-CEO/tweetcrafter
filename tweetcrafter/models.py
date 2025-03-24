from tweetcrafter.config import Config, Model
from tweetcrafter.hybrid_models import create_hybrid_model
import groq
from sambanova import SN40LClient


def create_model(model: Model):
    """Create and return a model instance based on the configured model type"""
    
    if model == Model.GROQ_LLAMA3:
        return create_hybrid_model()
    elif model == Model.SAMBANOVA_DEEPSEEK:
        return SN40LClient(api_key=Config.SAMBANOVA_API_KEY)
    elif model == Model.LLAMA_3:
        # Direct Groq client setup as fallback
        return groq.Client(api_key=Config.GROQ_API_KEY)
    elif model == Model.GPT_4o:
        # This is kept for backwards compatibility but not actively used in the hybrid approach
        from openai import OpenAI
        return OpenAI()
