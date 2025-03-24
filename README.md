# TweetCrafter

Write tweets with AI Agents (CrewAI)

<a href="https://www.mlexpert.io/bootcamp" target="_blank">
  <img src="https://raw.githubusercontent.com/curiousily/tweetcrafter/master/.github/tweetcrafter.png">
</a>

## Installation

Clone the repo

```sh
git clone git@github.com:curiousily/tweetcrafter.git
cd tweetcrafter
```

```sh
poetry install
```

Install iPython kernel:

```sh
poetry run python -m ipykernel install --user --name tweetcrafter --display-name "Python (tweetcrafter)"
```

## Add API keys

Create a `.env` file in the root of the project and add your API keys:

```sh
# LlamaCloud API Key
LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key_here

# Firecrawl API Key
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# SambaNova API Key
SAMBANOVA_API_KEY=your_sambanova_api_key_here
```

You can also copy the `.env.example` file and fill in your API keys.

## Hybrid Model System

TweetCrafter now uses a hybrid model system that combines Groq and SambaNova models for optimal performance and cost efficiency:

1. **Dynamic Complexity Routing**: Automatically routes queries to the appropriate model based on complexity:
   - Simple queries go to Groq's llama3-8b model (faster, cheaper)
   - Complex queries go to SambaNova's deepseek-r1 model (more powerful)

2. **Token Optimization**: Compresses prompts and truncates outputs to optimize token usage and costs.

3. **Hybrid Validation Workflow**: Uses a two-step process for tweet generation:
   - Initial drafts created with Groq
   - Quality validation and refinement with SambaNova when needed

This system ensures high-quality outputs while managing costs effectively.

## Usage

Go to `app.py` and change the inputs:

```py
inputs = {
    "topic": "The latest developments in AI coding assistants",
    "urls": [
        "https://github.blog/2023-11-08-universe-2023-copilot-transforms-into-an-ai-powered-developer-experience/",
        "https://www.anthropic.com/news/claude-3-family"
    ],
    "suggestion": "Include comparison between main players and highlight innovative features.",
}
```

Add tweets to analyze their writing style in `data/tweets.md`:

```md
# Tweet

Ever wondered how to reproduce GPT-2 (124M) efficiently?
@karpathy with llm.c has the answer!

- 90 mins, $20 on 8X A100 80GB SXM
- FineWeb dataset: 10B tokens
- MFU: 49-60%, 178K tokens/sec

https://github.com/karpathy/llm.c/discussions/481
```

Run the app:

```sh
poetry run python app.py
```

```py
{
   "total_tokens": 3000,
   "prompt_tokens": 2000,
   "completion_tokens": 1000,
   "successful_requests": 3
}
```

## Result

The tweets I got from the crew (saved to `output/tweet.md`):

```md
Original Tweet:
"Meet Phi-3, the cutting-edge AI model revolutionizing NLP! 
• Processes human language efficiently and accurately
• Ideal for NLP, text gen, conversational AI, sentiment analysis, and language translation
• Transparent, accountable, and fair decision-making
• Trained on diverse datasets and compatible with TensorFlow and PyTorch
#Phi3 #AI #NLP #LanguageModel #ResponsibleAI

Version 1:
"Unlock the power of Phi-3, the AI model that's changing the NLP game! 
• Efficient and accurate language processing
• Perfect for text gen, conversational AI, sentiment analysis, and language translation
• Transparency, accountability, and fairness in decision-making
• Compatible with TensorFlow and PyTorch
#Phi3 #AI #NLP #LanguageModel #ResponsibleAI

Version 2:
"Take your NLP projects to the next level with Phi-3! 
• Fast and accurate language processing
• Ideal for conversational AI, sentiment analysis, and language translation
• Built with transparency, accountability, and fairness in mind
• Compatible with TensorFlow and PyTorch
#Phi3 #AI #NLP #LanguageModel #ResponsibleAI

Version 3:
"Discover the future of NLP with Phi-3! 
• Efficient language processing for text gen, conversational AI, and more
• Transparent, accountable, and fair decision-making
• Trained on diverse datasets and compatible with TensorFlow and PyTorch
• Revolutionize your NLP projects with Phi-3
#Phi3 #AI #NLP #LanguageModel #ResponsibleAI
```

## Observability

_TweetCrafter_ stores logs of prompts and individual agent logs in the `logs` directory.

Have a look at the `notebooks/explore-logs.ipynb` notebook to explore the logs.
