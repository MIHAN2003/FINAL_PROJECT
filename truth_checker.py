import requests
import os
from datetime import datetime
from typing import Dict, List, Tuple
from dotenv import load_dotenv


load_dotenv()


llm_provider = os.getenv('LLM_PROVIDER', 'gemini').lower()

if llm_provider == 'openrouter':
    from openrouter_analyzer import OpenRouterAnalyzer
    AnalyzerClass = OpenRouterAnalyzer
elif llm_provider == 'gemini':
    from gemini_analyzer import GeminiAnalyzer
    AnalyzerClass = GeminiAnalyzer
else:
    raise ValueError(f"Unknown LLM_PROVIDER: {llm_provider}. Use 'gemini' or 'openrouter'")


class TruthChecker:
    """
    Orchestrates the complete pipeline for fact-checking news articles:
    1. Extract keywords from user article
    2. Search for related news using NewsAPI
    3. Analyze credibility using Gemini
    4. Generate truth analysis report
    """
    
    def __init__(self, newsapi_key: str, analyzer_api_key: str = None):
        """
        Initialize Truth Checker with API keys.
        
        Args:
            newsapi_key (str): NewsAPI.org API key
            analyzer_api_key (str): API key for the chosen LLM provider (optional, reads from env)
        """
        self.newsapi_key = newsapi_key
        
        
        if llm_provider == 'openrouter':
            self.analyzer = AnalyzerClass(analyzer_api_key)
        else:  # gemini
            self.analyzer = AnalyzerClass(analyzer_api_key)
            
        self.related_articles = []
    
    def search_related_news(self, keywords: str, max_results: int = 10) -> List[Dict]:
        """
        Search for news articles related to keywords using NewsAPI.
        
        Args:
            keywords (str): Search query (keywords combined with OR)
            max_results (int): Maximum articles to fetch
            
        Returns:
            List[Dict]: List of articles with title, description, url, source
        """
        print(f"📰 [NewsAPI] Searching for related news: {keywords}...\n")
        
        url = f'https://newsapi.org/v2/everything?q={keywords}&language=en&sortBy=relevancy&apiKey={self.newsapi_key}'
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == 'ok' and data['totalResults'] > 0:
                articles = data['articles'][:max_results]
                print(f"✓ Found {len(articles)} related articles\n")
                
                
                with open('related_articles.txt', 'w', encoding='utf-8') as f:
                    f.write(f"RELATED ARTICLES FOR: {keywords}\n")
                    f.write(f"TOTAL FOUND: {data['totalResults']}\n")
                    f.write("="*70 + "\n\n")
                    
                    for idx, article in enumerate(articles, 1):
                        f.write(f"[Article {idx}]\n")
                        f.write(f"Title: {article.get('title', 'N/A')}\n")
                        f.write(f"Source: {article.get('source', {}).get('name', 'Unknown')}\n")
                        f.write(f"URL: {article.get('url', 'N/A')}\n")
                        f.write(f"Description: {article.get('description', 'N/A')}\n")
                        f.write("="*70 + "\n\n")
                
                self.related_articles = articles
                return articles
            else:
                print("⚠ No related articles found\n")
                return []
        
        except Exception as e:
            print(f"❌ Error searching news: {str(e)}\n")
            return []
    
    def generate_truth_report(self, 
                            article_text: str, 
                            keywords_data: Dict, 
                            credibility_data: Dict,
                            ml_prediction: Tuple = None) -> str:
        """
        Generate formatted truth analysis report.
        
        Args:
            article_text (str): Original article
            keywords_data (Dict): Extracted keywords and entities
            credibility_data (Dict): Credibility analysis results
            ml_prediction (Tuple): ML model prediction (optional)
            
        Returns:
            str: Formatted report text
        """
        report = []
        report.append("="*70)
        report.append("TRUTH CHECK REPORT")
        report.append("="*70)
        report.append(f"\n📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n📝 ARTICLE SUMMARY:\n{article_text[:200]}...\n" if len(article_text) > 200 else f"\n📝 ARTICLE:\n{article_text}\n")
        
       
        report.append("\n" + "="*70)
        report.append("EXTRACTED KEYWORDS & ENTITIES")
        report.append("="*70)
        keywords = keywords_data.get('keywords', [])
        entities = keywords_data.get('entities', [])
        report.append(f"\n🔑 Keywords: {', '.join(keywords) if keywords else 'N/A'}")
        report.append(f"👥 Entities: {', '.join(entities) if entities else 'N/A'}")
        report.append(f"💬 Summary: {keywords_data.get('summary', 'N/A')}")
        
      
        main_claims = keywords_data.get('main_claims', [])
        if main_claims:
            report.append(f"\n📌 Main Claims:")
            for idx, claim in enumerate(main_claims, 1):
                report.append(f"   {idx}. {claim}")
        
        
        report.append("\n" + "="*70)
        report.append("TOP CORROBORATING SOURCES")
        report.append("="*70)
        if self.related_articles:
            for idx, article in enumerate(self.related_articles[:3], 1):
                report.append(f"\n{idx}. {article.get('source', {}).get('name', 'Unknown')}")
                report.append(f"   Title: {article.get('title', 'N/A')}")
                report.append(f"   URL: {article.get('url', 'N/A')}")
        else:
            report.append("\n⚠ No related articles found")
        
        
        report.append("\n" + "="*70)
        report.append("CREDIBILITY ANALYSIS")
        report.append("="*70)
        
        verdict = credibility_data.get('verdict', 'UNKNOWN')
        confidence = credibility_data.get('confidence', 0)
        score = credibility_data.get('credibility_score', 0)
        
       
        verdict_emoji = {"TRUE": "✅", "FALSE": "❌", "MIXED": "⚠️"}.get(verdict, "❓")
        
        report.append(f"\n{verdict_emoji} VERDICT: {verdict}")
        report.append(f"📊 Confidence: {confidence}%")
        report.append(f"⭐ Credibility Score: {score}/10")
        
        
        report.append(f"\n📋 Explanation:\n{credibility_data.get('explanation', 'N/A')}")
        
        evidence_for = credibility_data.get('evidence_for', [])
        evidence_against = credibility_data.get('evidence_against', [])
        
        if evidence_for:
            report.append(f"\n✅ Evidence Supporting the Article:")
            for item in evidence_for:
                report.append(f"   • {item}")
        
        if evidence_against:
            report.append(f"\n❌ Evidence Against or Missing Corroboration:")
            for item in evidence_against:
                report.append(f"   • {item}")
        
        report.append("\n" + "="*70)
        report.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*70)
        
        return "\n".join(report)
    
    def check_article(self, article_text: str) -> Dict:
        """
        Run complete fact-checking pipeline on article.
        
        Args:
            article_text (str): The news article to check
            
        Returns:
            Dict: Complete analysis results
        """
        print("\n" + "="*70)
        print("STARTING FACT-CHECK PIPELINE")
        print("="*70 + "\n")
        
       
        print("STEP 1: KEYWORD EXTRACTION")
        print("-"*70)
        keywords_data = self.analyzer.extract_keywords(article_text)
        
        ml_prediction = None
        
        
        print("STEP 2: NEWS SEARCH")
        print("-"*70)
        search_query = self.analyzer.format_search_query(keywords_data.get('keywords', []))
        self.search_related_news(search_query)
        
        
        print("STEP 3: CREDIBILITY ANALYSIS")
        print("-"*70)
        credibility_data = self.analyzer.analyze_credibility(
            article_text, 
            self.related_articles
        )
        
        
        print("STEP 4: GENERATING REPORT")
        print("-"*70)
        report = self.generate_truth_report(
            article_text,
            keywords_data,
            credibility_data,
            ml_prediction
        )
        
        
        with open('truth_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✓ Report saved to truth_analysis_report.txt\n")
        
        return {
            "keywords": keywords_data,
            "related_articles": self.related_articles,
            "credibility": credibility_data,
            "ml_prediction": ml_prediction,
            "report": report
        }
