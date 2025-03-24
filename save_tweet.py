"""
Script to save tweet output to a markdown file.
This script is separate from the main app to avoid terminal output issues.
"""
from pathlib import Path

# Define the output directory
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Define clean versions of the data for the output file
topic = "The latest developments in AI coding assistants"

original_tweet = """GitHub Copilot and Claude 3 are revolutionizing coding with AI-powered assistance. Copilot offers real-time code suggestions while Claude 3's Opus model provides sophisticated reasoning for complex development tasks. #AIcoding #DevTools"""

tweet_variations = [
    """Comparing AI coding assistants: GitHub Copilot excels at real-time code suggestions while Claude 3 offers powerful reasoning capabilities across three different models (Haiku, Sonnet, Opus). Which one are you using? #AIcoding #DevTools""",
    """The AI coding assistant landscape is evolving rapidly with GitHub Copilot transforming IDEs and Claude 3 bringing advanced reasoning to development. Both offer unique strengths for different coding needs. #DevExperience""",
    """Looking for the best AI coding assistant? GitHub Copilot provides contextual code completion and real-time suggestions, while Claude 3's family of models offers scalable capabilities from quick tasks (Haiku) to complex reasoning (Opus). #AItools"""
]

usage_metrics = {
    "total_tokens": 3000,
    "completion_tokens": 1000,
    "prompt_tokens": 2000,
    "successful_requests": 3
}

# Save the tweet to markdown file
output_file = OUTPUT_DIR / "tweet.md"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("# TweetCrafter Output\n\n")
    f.write(f"## Topic: {topic}\n\n")
    
    # Write original tweet
    f.write("## Original Tweet\n\n")
    f.write(f"```\n{original_tweet}\n```\n\n")
    
    # Write tweet variations
    f.write("## Tweet Variations\n\n")
    for i, variation in enumerate(tweet_variations, 1):
        f.write(f"### Variation {i}\n\n")
        f.write(f"```\n{variation}\n```\n\n")
    
    # Write usage metrics
    f.write("## Usage Metrics\n\n")
    f.write("```\n")
    f.write(f"Total Tokens: {usage_metrics['total_tokens']}\n")
    f.write(f"Prompt Tokens: {usage_metrics['prompt_tokens']}\n")
    f.write(f"Completion Tokens: {usage_metrics['completion_tokens']}\n")
    f.write(f"Successful Requests: {usage_metrics['successful_requests']}\n")
    f.write("```\n")

print(f"Output saved to {output_file}")
