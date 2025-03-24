from dotenv import load_dotenv
import os

from tweetcrafter.agents import (
    editor_agent,
    researcher_agent,
    scraper_agent,
    writer_agent,
)
from tweetcrafter.config import Config
from tweetcrafter.llama_cloud import TweetCrafterWorkflow

# Load environment variables from .env file
load_dotenv()

# Verify API keys are loaded
required_keys = ["LLAMA_CLOUD_API_KEY", "FIRECRAWL_API_KEY", "GROQ_API_KEY", "SAMBANOVA_API_KEY"]
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
else:
    print("All required API keys loaded successfully")

Config.Path.AGENT_LOGS_DIR.mkdir(exist_ok=True, parents=True)
Config.Path.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Create agents
scraper = scraper_agent()
researcher = researcher_agent()
writer = writer_agent()
editor = editor_agent()

# Initialize workflow
workflow = TweetCrafterWorkflow(agents=[scraper, researcher, writer, editor])

inputs = {
    "topic": "The latest developments in AI coding assistants",
    "urls": [
        "https://github.blog/2023-11-08-universe-2023-copilot-transforms-into-an-ai-powered-developer-experience/",
        "https://www.anthropic.com/news/claude-3-family"
    ],
    "suggestion": "Include comparison between main players and highlight innovative features.",
}

print("Starting TweetCrafter Workflow using Hybrid Model System (Groq + SambaNova)")
print(f"Topic: {inputs['topic']}")
print(f"URLs: {', '.join(inputs['urls'])}")
print(f"Suggestion: {inputs['suggestion']}")
print("="*80)

# Run the workflow
results = workflow.run_workflow(inputs)

# Display results
print("\nRESULTS:")
print("="*80)
print("\nORIGINAL TWEET:")
print(results.get("original_tweet", "No tweet generated"))
print("\nFINAL TWEETS:")
print(results.get("final_tweets", "No variations generated"))
print("="*80)

print("\nUsage Metrics:")
print(workflow.usage_metrics)
