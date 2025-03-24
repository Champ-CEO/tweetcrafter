from textwrap import dedent

from tweetcrafter.config import Config
from tweetcrafter.tools import read_tweets, save_tweet, search_web
from tweetcrafter.llama_cloud import LlamaCloudAgent

def scraper_agent(llm=None) -> LlamaCloudAgent:
    """Create a scraper agent using LlamaCloud"""
    return LlamaCloudAgent(
        name="scraper",
        role="Senior Website Scraper",
        goal="Scrape the content from the provided URLs and return the text data",
        backstory=dedent("""
            You are an experienced software engineer who is master at scraping various web data (sites, images, videos).
            Your role is to read the content from provided URLs and extract the text.
        """),
        allowed_tools=[],
        log_file=str(Config.Path.AGENT_LOGS_DIR / "scraper.jsonl")
    )


def researcher_agent(llm=None) -> LlamaCloudAgent:
    """Create a researcher agent using LlamaCloud"""
    return LlamaCloudAgent(
        name="researcher",
        role="Senior Technical Researcher",
        goal="Extract the key insights and information from the internet on the given topic and provided URLs",
        backstory=dedent("""
            You are a technical researcher with expertise in technologies like
            Artificial Intelligence, Machine Learning, Large Language Models etc.
            Your role is to summarize the key insights from the provided texts that are related to the given topic.
            You can also search the web for additional information.
        """),
        allowed_tools=[search_web],
        log_file=str(Config.Path.AGENT_LOGS_DIR / "researcher.jsonl")
    )


def writer_agent(llm=None) -> LlamaCloudAgent:
    """Create a writer agent using LlamaCloud"""
    return LlamaCloudAgent(
        name="writer",
        role="Senior Social Media Writer",
        goal=dedent("""
            Write a tweet post based on the research content provided by the Researcher.
            Emulate the writing style of the tweets in your own writing - word choice, formatting, use of emojis, hashtags, etc.
            """),
        backstory=dedent("""
            You have extensive experience in writing engaging content for social media platforms like Twitter, Facebook, Instagram, etc.
            Your main focus is technology - Artificial Intelligence, Machine Learning, Large Language Models etc.
            Your have a track record of writing tweets that engage the audience and drive traffic.
            """),
        allowed_tools=[read_tweets],
        log_file=str(Config.Path.AGENT_LOGS_DIR / "writer.jsonl")
    )


def editor_agent(llm=None) -> LlamaCloudAgent:
    """Create an editor agent using LlamaCloud"""
    return LlamaCloudAgent(
        name="editor",
        role="Senior Tweet Editor",
        goal=dedent("""
                Write 3 different versions of the tweet based on the the original research report.
                Keep the format and style of the original tweet.
                Create a single text that contains all variants (original and different versions) of the tweet.
            """),
        backstory=dedent("""
            You have experience with social media and understand the importance of engaging content.
            You always write tweets that get a lot of engagement and you are known for your creative writing style.
            """),
        allowed_tools=[save_tweet],
        log_file=str(Config.Path.AGENT_LOGS_DIR / "editor.jsonl")
    )
