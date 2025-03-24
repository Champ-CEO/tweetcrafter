from dotenv import load_dotenv

from tweetcrafter.agents import (
    editor_agent,
    researcher_agent,
    scraper_agent,
    writer_agent,
)
from tweetcrafter.config import Config
from tweetcrafter.llama_cloud import TweetCrafterWorkflow

load_dotenv()

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
    "topic": "Summary of the key new features of Phi-3",
    "urls": [
        "https://huggingface.co/microsoft/Phi-3-vision-128k-instruct",
    ],
    "suggestion": "Focus on the performance and how-to use the model.",
}

# Run the workflow
results = workflow.run_workflow(inputs)

print(workflow.usage_metrics)
