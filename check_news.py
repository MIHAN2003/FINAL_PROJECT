#!/usr/bin/env python3
"""
CLI Entry Point for Fake News Detection System
Reads article from today_news.txt and runs the complete fact-checking pipeline
"""

import os
from dotenv import load_dotenv
from truth_checker import TruthChecker


def check_news_text(article_text: str, newsapi_key: str, analyzer_api_key: str, provider: str = 'gemini') -> dict:
    """
    Run the complete fact-checking pipeline on the given text.
    
    Args:
        article_text (str): The news article text to analyze
        newsapi_key (str): NewsAPI key
        analyzer_api_key (str): LLM API key (Gemini or OpenRouter)
        provider (str): 'gemini' or 'openrouter'
    
    Returns:
        dict: Analysis results
    """
    # Set provider in environment
    os.environ['LLM_PROVIDER'] = provider
    
    # Initialize Truth Checker
    checker = TruthChecker(newsapi_key, analyzer_api_key)
    
    # Run the pipeline
    result = checker.check_article(article_text)
    
    return result


def print_concise_output(result: dict):
    """Print concise truth check results to console."""
    print("\n" + "="*70)
    print("QUICK VERDICT")
    print("="*70 + "\n")
    
    # Keywords
    keywords = result['keywords'].get('keywords', [])
    print(f"🔑 Keywords: {', '.join(keywords[:5]) if keywords else 'N/A'}")
    
    # Sources
    articles = result['related_articles']
    if articles:
        sources = [art.get('source', {}).get('name', 'Unknown') for art in articles[:3]]
        print(f"📰 Top Sources: {', '.join(sources)}")
    else:
        print("📰 Top Sources: No related articles found")
    
    # Verdict
    cred = result['credibility']
    verdict = cred.get('verdict', 'UNKNOWN')
    confidence = cred.get('confidence', 0)
    
    verdict_emoji = {"TRUE": "✅", "FALSE": "❌", "MIXED": "⚠️"}.get(verdict, "❓")
    print(f"\n{verdict_emoji} VERDICT: {verdict}")
    print(f"📊 Confidence: {confidence}%")
    print(f"⭐ Credibility Score: {cred.get('credibility_score', 0)}/10")
    
    print("\n" + "="*70)
    print("📄 Full report saved to: truth_analysis_report.txt")
    print("="*70 + "\n")


def main():
    """Main CLI entry point."""
    print("\n" + "="*70)
    print("🔍 FAKE NEWS DETECTION - TRUTH CHECKER")
    print("="*70 + "\n")
    
    # Load environment variables
    load_dotenv()
    
    # Get LLM provider
    llm_provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
    
    # Get API keys
    newsapi_key = os.getenv('NEWSAPI_KEY')
    if not newsapi_key:
        newsapi_key = input("Enter your NewsAPI key (https://newsapi.org): ").strip()
    
    # Get the appropriate API key based on provider
    if llm_provider == 'openrouter':
        analyzer_api_key = os.getenv('OPENROUTER_API_KEY')
        if not analyzer_api_key or analyzer_api_key == 'your_openrouter_api_key_here':
            analyzer_api_key = input("Enter your OpenRouter API key (https://openrouter.ai): ").strip()
        provider_name = "OpenRouter"
    else:  # gemini
        analyzer_api_key = os.getenv('GEMINI_API_KEY')
        if not analyzer_api_key:
            analyzer_api_key = input("Enter your Google Gemini API key: ").strip()
        provider_name = "Gemini"
    
    if not newsapi_key or not analyzer_api_key:
        print(f"❌ Error: NewsAPI key and {provider_name} API key are required")
        sys.exit(1)
    
    # Check if input file exists
    if not os.path.exists('today_news.txt'):
        print("❌ Error: today_news.txt not found")
        print("Please create today_news.txt with your news article")
        sys.exit(1)
    
    # Read article from file
    try:
        with open('today_news.txt', 'r', encoding='utf-8') as f:
            article_text = f.read().strip()
        
        if not article_text:
            print("❌ Error: today_news.txt is empty")
            sys.exit(1)
        
        print(f"📖 Loaded article from today_news.txt ({len(article_text)} characters)\n")
    
    except Exception as e:
        print(f"❌ Error reading today_news.txt: {e}")
        sys.exit(1)
    
    # Initialize Truth Checker
    try:
        result = check_news_text(article_text, newsapi_key, analyzer_api_key, llm_provider)
        print_concise_output(result)
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
