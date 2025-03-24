"""
Mock implementation of SambaNova client for testing purposes.
This allows testing the hybrid model system without the actual SambaNova package.
"""

class SN40LClient:
    """Mock SambaNova client that simulates API responses"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        
    def generate(self, model, prompt, params=None):
        """Mock implementation of the generate method
        
        Args:
            model: Model name
            prompt: Text prompt
            params: Parameters for generation
            
        Returns:
            Dictionary with output and usage information
        """
        # Simply create a formatted response that acknowledges it's a mock
        response = {
            "output": f"[SambaNova Mock] Response for prompt: {prompt[:50]}...",
            "usage": {
                "total_tokens": 500,
                "prompt_tokens": 250,
                "completion_tokens": 250
            },
            "model": model
        }
        
        # If this is a refinement request, make the output more specific
        if "refine" in prompt.lower():
            response["output"] = "This is a refined tweet about the topic with better accuracy and engagement. #AI #Tech"
            
        return response
