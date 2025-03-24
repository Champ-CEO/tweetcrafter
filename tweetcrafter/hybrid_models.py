import re
from typing import Dict, Any

import groq
# Import mock SambaNova client instead of the real one
from tweetcrafter.mock_sambanova import SN40LClient

from tweetcrafter.config import Config


class TokenOptimizer:
    """Optimizes token usage by compressing prompts and truncating outputs"""
    
    def __init__(self):
        self.groq_client = groq.Client(api_key=Config.GROQ_API_KEY)
    
    def compress_prompt(self, text: str) -> str:
        """Compress a prompt to reduce token usage"""
        response = self.groq_client.chat.completions.create(
            model="llama3-8b",
            messages=[{"role": "user", "content": f"Compress: {text}"}],
            max_tokens=150
        )
        return response.choices[0].message.content

    def truncate_output(self, text: str) -> str:
        """Truncate output to Twitter's character limit"""
        return text[:280]  # Enforce tweet length limit


class HybridModelRouter:
    """Routes queries to different models based on complexity"""
    
    def __init__(self):
        self.groq_client = groq.Client(api_key=Config.GROQ_API_KEY)
        self.sn_client = SN40LClient(api_key=Config.SAMBANOVA_API_KEY)
        self.token_optimizer = TokenOptimizer()
        
    def analyze_complexity(self, prompt: str) -> float:
        """Analyze the complexity of a prompt to determine routing
        
        Returns a score between 0 and 1, where higher values indicate more complexity
        """
        complexity_score = 0.0
        
        # Check for technical terms
        technical_terms = [
            r'\b(machine learning|deep learning|transformer|neural network|attention mechanism)\b',
            r'\b(fine-tuning|training|parameter|embedding|token)\b',
            r'\b(algorithm|architecture|inference|optimization|quantization)\b'
        ]
        
        for pattern in technical_terms:
            if re.search(pattern, prompt, re.IGNORECASE):
                complexity_score += 0.1
        
        # Check for code snippets
        if re.search(r'```|def |class |import |from .* import', prompt):
            complexity_score += 0.2
            
        # Check for mathematical notation
        if re.search(r'\$.*\$|\\\(.*\\\)|\\\[.*\\\]', prompt):
            complexity_score += 0.15
            
        # Check length (longer prompts are generally more complex)
        word_count = len(prompt.split())
        complexity_score += min(0.3, word_count / 500)  # Cap at 0.3 for very long prompts
        
        return min(1.0, complexity_score)  # Ensure score doesn't exceed 1.0
    
    def needs_quality_check(self, text: str) -> bool:
        """Determine if a generated text needs quality validation
        
        Returns True if the text should be validated by a more powerful model
        """
        # Check for potential issues that indicate a need for quality check
        issues = [
            # Check for hallucination indicators
            "I'm not sure",
            "I believe",
            "might be",
            # Check for generic/vague responses
            "it depends",
            "generally speaking",
            # Check for incomplete thoughts
            "...",
            "etc.",
        ]
        
        for issue in issues:
            if issue.lower() in text.lower():
                return True
                
        # Also check if the response is too short
        if len(text.split()) < 20:
            return True
            
        return False
    
    def route_query(self, prompt: str) -> Dict[str, Any]:
        """Route a query to the appropriate model based on complexity
        
        For simpler queries, use Groq's Llama3-8b model
        For more complex queries, use SambaNova's DeepSeek model
        """
        complexity_score = self.analyze_complexity(prompt)
        
        if complexity_score < 0.4:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-tool-use",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return {
                "content": response.choices[0].message.content,
                "model": "groq-llama3-8b",
                "tokens": response.usage.total_tokens
            }
        else:
            response = self.sn_client.generate(
                model="deepseek-r1-671b",
                prompt=prompt,
                params={"precision": "bf16"}
            )
            return {
                "content": response['output'],
                "model": "sambanova-deepseek-r1",
                "tokens": response.get('usage', {}).get('total_tokens', 0)
            }
    
    def generate_tweet(self, prompt: str) -> str:
        """Generate a tweet using a hybrid approach for higher quality
        
        First uses Groq for initial draft, then optionally refines with SambaNova
        """
        # First draft via Groq
        draft_response = self.groq_client.chat.completions.create(
            model="llama3-70b-tool-use",
            messages=[{"role": "user", "content": prompt}]
        )
        draft = draft_response.choices[0].message.content
        
        # Accuracy boost via SambaNova if needed
        if self.needs_quality_check(draft):
            refined_response = self.sn_client.generate(
                model="deepseek-r1-671b",
                prompt=f"Refine this tweet to be accurate, engaging, and concise: {draft}"
            )
            return self.token_optimizer.truncate_output(refined_response['output'])
        
        return self.token_optimizer.truncate_output(draft)


def create_hybrid_model() -> HybridModelRouter:
    """Create and return a configured hybrid model router instance"""
    return HybridModelRouter()
