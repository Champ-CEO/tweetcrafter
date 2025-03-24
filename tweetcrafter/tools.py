import requests
from tweetcrafter.config import Config


def save_tweet(text: str):
    """Save a tweet text to a markdown file."""
    file_path = Config.Path.OUTPUT_DIR / "tweet.md"
    with file_path.open("w") as file:
        file.write(text)
    return str(file_path)


def read_tweets() -> str:
    """Read all tweets from a markdown file."""
    with (Config.Path.DATA_DIR / "tweets.md").open("r") as file:
        return file.read()


def search_web(query: str, num_results: int = 5) -> str:
    """Search the web using Firecrawl and return the results.
    
    Args:
        query: The search query
        num_results: Number of results to return (default: 5)
        
    Returns:
        A string with the search results
    """
    api_key = Config.FIRECRAWL_API_KEY
    if not api_key:
        return "Error: FIRECRAWL_API_KEY not found in environment variables."
    
    url = "https://api.firecrawl.dev/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "limit": num_results
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        results = response.json()
        
        formatted_results = []
        for i, result in enumerate(results.get("results", [])):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            snippet = result.get("snippet", "No snippet")
            
            formatted_results.append(f"{i+1}. {title}\n   URL: {url}\n   {snippet}\n")
        
        return "\n".join(formatted_results) if formatted_results else "No results found."
    
    except Exception as e:
        return f"Error searching the web: {str(e)}"
