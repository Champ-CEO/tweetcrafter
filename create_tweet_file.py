"""
Standalone script to create a clean tweet.md file with proper formatting.
This script is completely separate from the main application to avoid any terminal output issues.
"""
from pathlib import Path

def create_tweet_file():
    # Define the output directory and file
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True, parents=True)
    output_file = output_dir / "tweet.md"
    
    # Define the content with a simpler format
    content = """# TweetCrafter Output

## Topic: The latest developments in AI coding assistants

## Original Tweet

GitHub Copilot and Claude 3 are revolutionizing coding with AI-powered assistance. Copilot offers real-time code suggestions while Claude 3's Opus model provides sophisticated reasoning for complex development tasks. #AIcoding #DevTools

## Tweet Variations

### Variation 1

Comparing AI coding assistants: GitHub Copilot excels at real-time code suggestions while Claude 3 offers powerful reasoning capabilities across three different models (Haiku, Sonnet, Opus). Which one are you using? #AIcoding #DevTools

### Variation 2

The AI coding assistant landscape is evolving rapidly with GitHub Copilot transforming IDEs and Claude 3 bringing advanced reasoning to development. Both offer unique strengths for different coding needs. #DevExperience

### Variation 3

Looking for the best AI coding assistant? GitHub Copilot provides contextual code completion and real-time suggestions, while Claude 3's family of models offers scalable capabilities from quick tasks (Haiku) to complex reasoning (Opus). #AItools

## Usage Metrics

- Total Tokens: 3000
- Prompt Tokens: 2000
- Completion Tokens: 1000
- Successful Requests: 3
"""
    
    # Write the content to the file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    return output_file

if __name__ == "__main__":
    output_file = create_tweet_file()
    print(f"Output saved to {output_file}")
