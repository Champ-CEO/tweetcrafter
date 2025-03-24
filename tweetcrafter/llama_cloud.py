from typing import Dict, List, Optional, Any
import requests
from tweetcrafter.config import Config
from tweetcrafter.callbacks import step_callback


class LlamaCloudAgent:
    """LlamaCloud Agent class to replace CrewAI Agent"""
    
    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        allowed_tools: List[Any] = None,
        log_file: Optional[str] = None
    ):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.allowed_tools = allowed_tools or []
        self.log_file = log_file
        self.api_key = Config.LLAMA_CLOUD_API_KEY
        self.base_url = "https://cloud.llamaindex.ai/api/completions"
        
    def execute(self, task_description: str, context: str = "", **kwargs) -> str:
        """Execute a task using LlamaCloud API"""
        
        # Construct the prompt with the agent's role, goal, and the task
        prompt = f"""
You are a {self.role}.
Goal: {self.goal}
Background: {self.backstory}

Task: {task_description}

{context if context else ""}

Please complete this task to the best of your abilities.
"""
        
        # Call LlamaCloud API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "prompt": prompt,
            "model": "llama3-70b-chat",
            "max_tokens": 2000,
            "temperature": 0.7,
            "stop": ["<END>"],
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            output = result.get("choices", [{}])[0].get("text", "").strip()
            
            # Log the interaction if a log file is specified
            if self.log_file:
                log_data = {
                    "agent": self.name,
                    "prompt": prompt,
                    "response": output
                }
                step_callback(log_data, self.name, self.log_file)
                
            return output
        
        except Exception as e:
            return f"Error executing task: {str(e)}"
    
    def use_tool(self, tool_name: str, **kwargs) -> str:
        """Use a specific tool by name"""
        for tool in self.allowed_tools:
            if getattr(tool, "__name__", "") == tool_name:
                return tool(**kwargs)
        
        return f"Tool {tool_name} not found or not allowed for this agent."


class TweetCrafterWorkflow:
    """Class to replace CrewAI Crew for managing the workflow"""
    
    def __init__(self, agents: List[LlamaCloudAgent]):
        self.agents = agents
        self.results = {}
        self.usage_metrics = {"total_tokens": 0, "completion_tokens": 0, "prompt_tokens": 0, "successful_requests": 0}
    
    def run_scraper(self, urls: List[str]) -> str:
        """Run the scraper agent to get content from URLs"""
        scraper = next((agent for agent in self.agents if agent.name == "scraper"), None)
        if not scraper:
            return "Scraper agent not found"
        
        url_list = "\n".join([f"- {url}" for url in urls])
        task = f"Scrape the content from the following URLs:\n{url_list}"
        
        return scraper.execute(task)
    
    def run_researcher(self, topic: str, scraped_content: str) -> str:
        """Run the researcher agent to analyze content"""
        researcher = next((agent for agent in self.agents if agent.name == "researcher"), None)
        if not researcher:
            return "Researcher agent not found"
        
        task = f"Research and analyze information about the topic: {topic}"
        context = f"Use the following scraped content as your primary source:\n{scraped_content}"
        
        return researcher.execute(task, context=context)
    
    def run_writer(self, research_report: str) -> str:
        """Run the writer agent to create a tweet"""
        writer = next((agent for agent in self.agents if agent.name == "writer"), None)
        if not writer:
            return "Writer agent not found"
        
        task = "Write an engaging tweet based on the research report"
        context = f"Research Report:\n{research_report}"
        
        return writer.execute(task, context=context)
    
    def run_editor(self, original_tweet: str, research_report: str, suggestion: str) -> str:
        """Run the editor agent to create tweet variations"""
        editor = next((agent for agent in self.agents if agent.name == "editor"), None)
        if not editor:
            return "Editor agent not found"
        
        task = "Create 3 different versions of the tweet"
        context = f"""
Original Tweet:
{original_tweet}

Research Report:
{research_report}

Suggestion:
{suggestion}
"""
        
        return editor.execute(task, context=context)
    
    def run_workflow(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Run the entire workflow sequentially"""
        topic = inputs.get("topic", "")
        urls = inputs.get("urls", [])
        suggestion = inputs.get("suggestion", "")
        
        # Step 1: Scrape content
        scraped_content = self.run_scraper(urls)
        self.results["scraped_content"] = scraped_content
        
        # Step 2: Research and analyze
        research_report = self.run_researcher(topic, scraped_content)
        self.results["research_report"] = research_report
        
        # Step 3: Write the tweet
        original_tweet = self.run_writer(research_report)
        self.results["original_tweet"] = original_tweet
        
        # Step 4: Edit and create variations
        final_tweets = self.run_editor(original_tweet, research_report, suggestion)
        self.results["final_tweets"] = final_tweets
        
        return self.results
