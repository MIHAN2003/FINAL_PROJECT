import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('NEWSAPI_KEY', '7fe0e0b48ee349cc9b8c815073a5d5a9')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY','AIzaSyAEHX4Nts86McWSxg3nrdpo1sdYC-AkT_c' )

# Try to import Gemini analyzer (optional enhancement)
try:
    from gemini_analyzer import GeminiAnalyzer
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠ Gemini integration not available. Install google-generativeai for enhanced analysis.")

print("="*70)
print("NEWS SEARCH")
print("="*70 + "\n")

# 1. Ask the user what they want to search for
topic = input("Enter a topic you want to search for (e.g., Tesla, NASA, Crypto): ")

# 3. Use the 'everything' endpoint to fetch articles
url = f'https://newsapi.org/v2/everything?q={topic}&language=en&apiKey={API_KEY}'

print(f"\nSearching for news about: {topic}...\n")

try:
    response = requests.get(url)
    data = response.json()
except Exception as e:
    print(f"❌ Error making API request: {str(e)}")
    exit(1)

if data['status'] == 'ok' and data['totalResults'] > 0:
    print(f"--- SEARCH RESULTS FOR: {topic.upper()} ---")
    print(f"Total results available: {data['totalResults']}\n")
    
    # Open the file in 'w' mode to overwrite old news with the new search
    with open("search_results.txt", "w", encoding="utf-8") as file:
        file.write(f"SEARCH TOPIC: {topic}\n")
        file.write(f"TOTAL RESULTS: {data['totalResults']}\n")
        file.write("="*70 + "\n\n")
        
        # Process the first 10 articles
        for idx, article in enumerate(data['articles'][:10], 1):
            title = article.get('title', 'N/A')
            description = article.get('description', 'N/A')
            url = article.get('url', 'N/A')
            source_name = article.get('source', {}).get('name', 'Unknown')
            published_at = article.get('publishedAt', 'N/A')
            author = article.get('author', 'Unknown')
            content = article.get('content', '')
            url_to_image = article.get('urlToImage', 'N/A')
            
            # Display article metadata
            print(f"\n[{idx}] 🔎 ARTICLE")
            print(f"TITLE: {title}")
            print(f"SOURCE: {source_name} | AUTHOR: {author}")
            print(f"PUBLISHED: {published_at}")
            print(f"DESCRIPTION: {description[:100]}..." if len(str(description)) > 100 else f"DESCRIPTION: {description}")
            print(f"LINK: {url}")
            print("-"*70)
            
            # Save to file
            file.write(f"[ARTICLE {idx}]\n")
            file.write(f"PREDICTION: {news_type}\n")
            file.write(f"CONFIDENCE: {confidence_pct:.1f}%\n")
            file.write(f"TITLE: {title}\n")
            file.write(f"SOURCE: {source_name}\n")
            file.write(f"AUTHOR: {author}\n")
            file.write(f"PUBLISHED: {published_at}\n")
            file.write(f"DESCRIPTION: {description}\n")
            file.write(f"LINK: {url}\n")
            file.write(f"IMAGE: {url_to_image}\n")
            file.write("="*70 + "\n\n")
    
    print(f"\n✓ Success! Top 10 results with predictions saved to search_results.txt")
    
elif data['totalResults'] == 0:
    print("❌ No articles found for that topic. Try something else!")
else:
    print("❌ Error fetching news. Check your API key or connection.")


# ============================================================================
# GEMINI-ENHANCED ANALYSIS FUNCTIONS
# ============================================================================

def analyze_article_with_gemini(article_text, gemini_analyzer):
    """
    Enhanced analysis using Gemini for semantic understanding.
    
    Args:
        article_text (str): Article text to analyze
        gemini_analyzer (GeminiAnalyzer): Initialized Gemini analyzer
        
    Returns:
        dict: Analysis results with keywords and credibility insights
    """
    if not GEMINI_AVAILABLE or not gemini_analyzer:
        return None
    
    try:
        keywords_data = gemini_analyzer.extract_keywords(article_text)
        return keywords_data
    except Exception as e:
        print(f"⚠ Gemini analysis error: {e}")
        return None


def search_and_verify_with_gemini(topic, gemini_analyzer):
    """
    Search for articles and use Gemini to verify credibility.
    
    Args:
        topic (str): Topic to search for
        gemini_analyzer (GeminiAnalyzer): Initialized Gemini analyzer
        
    Returns:
        tuple: (articles, credibility_scores)
    """
    if not GEMINI_AVAILABLE or not gemini_analyzer:
        return None, None
    
    # Search for articles
    url = f'https://newsapi.org/v2/everything?q={topic}&language=en&apiKey={API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'ok' and data['totalResults'] > 0:
            articles = data['articles'][:10]
            
            # Store for credibility analysis
            return articles, data['totalResults']
    except Exception as e:
        print(f"⚠ Search error: {e}")
    
    return None, None