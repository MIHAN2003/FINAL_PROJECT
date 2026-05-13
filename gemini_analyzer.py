import google.genai as genai
import json
import os
from typing import Dict, List, Tuple


class GeminiAnalyzer:
    """
    Analyzes news articles using Google Gemini API for:
    - Keyword and entity extraction
    - Credibility analysis against related articles
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini analyzer with API key.
        
        Args:
            api_key (str): Google Gemini API key. If None, reads from GEMINI_API_KEY env var.
        """
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError(
                "❌ Gemini API key not found. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = genai.Client(api_key=api_key)
        print("✓ Gemini API initialized successfully\n")
    
    def extract_keywords(self, article_text: str) -> Dict:
        """
        Extract keywords, entities, and main claims from article text.
        
        Args:
            article_text (str): The news article text to analyze
            
        Returns:
            Dict: Contains 'keywords', 'entities', 'main_claims' as lists
        """
        print("🔍 [Gemini] Extracting keywords and entities...")
        
        prompt = f"""Analyze this news article and extract key information. Return ONLY valid JSON.

ARTICLE:
{article_text}

Return this exact JSON structure (no additional text):
{{
    "keywords": [list of 5-10 most important keywords/topics],
    "entities": [list of important people, organizations, places mentioned],
    "main_claims": [list of 3-5 main assertions or claims in the article],
    "summary": "1-2 sentence summary of the article"
}}

IMPORTANT: Return ONLY the JSON object, nothing else."""

        try:
            response = self.client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
            response_text = response.text.strip()
            
            # Parse JSON response
            result = json.loads(response_text)
            
            print(f"✓ Extracted {len(result.get('keywords', []))} keywords")
            print(f"✓ Identified {len(result.get('entities', []))} entities")
            print(f"✓ Found {len(result.get('main_claims', []))} main claims\n")
            
            return result
        
        except json.JSONDecodeError as e:
            print(f"⚠ Warning: Failed to parse Gemini JSON response: {e}")
            if 'response_text' in locals():
                print(f"Response was: {response_text}\n")
            # Return default structure on parse error
            return {
                "keywords": [],
                "entities": [],
                "main_claims": [],
                "summary": "Failed to extract"
            }
        except Exception as e:
            print(f"❌ Error extracting keywords: {str(e)}\n")
            return {
                "keywords": [],
                "entities": [],
                "main_claims": [],
                "summary": "Error during extraction"
            }
    
    def analyze_credibility(
        self, 
        user_article: str, 
        related_articles: List[Dict],
        ml_prediction: Tuple[int, float] = None
    ) -> Dict:
        """
        Analyze credibility of user article against related articles.
        
        Args:
            user_article (str): The user-provided article text
            related_articles (List[Dict]): List of related articles with 'title', 'description', 'url'
            ml_prediction (Tuple): Optional (prediction, confidence) from ML model
            
        Returns:
            Dict: Contains 'verdict', 'confidence', 'evidence', 'explanation'
        """
        print("🔬 [Gemini] Analyzing credibility against related sources...")
        
        # Format related articles for context
        sources_text = ""
        for idx, article in enumerate(related_articles[:10], 1):
            title = article.get('title', 'N/A')
            description = article.get('description', 'N/A')
            source = article.get('source', {}).get('name', 'Unknown')
            sources_text += f"\n[Source {idx}] {source}\nTitle: {title}\nContent: {description}\n"
        
        # Add ML prediction if available
        ml_note = ""
        if ml_prediction:
            pred, conf = ml_prediction
            ml_pred_text = "FAKE" if pred == 0 else "REAL"
            ml_note = f"\nNote: ML model prediction: {ml_pred_text} (confidence: {conf*100:.1f}%)"
        
        prompt = f"""You are a fact-checking expert. Analyze the user's article against these related sources.

USER ARTICLE:
{user_article}

RELATED SOURCES FROM NEWS API:{sources_text}

{ml_note}

Analyze:
1. Are the facts in the user's article consistent with the related sources?
2. Do any sources contradict the main claims?
3. Is the article credible, partially credible, or fake?
4. What evidence supports or contradicts each main claim?

Return ONLY this JSON (no other text):
{{
    "verdict": "TRUE" or "FALSE" or "MIXED",
    "confidence": 0-100 (integer confidence percentage),
    "credibility_score": 0-10 (decimal score),
    "evidence_for": [list of supporting facts from sources],
    "evidence_against": [list of contradicting facts or missing corroboration],
    "explanation": "2-3 sentence explanation of the verdict"
}}

IMPORTANT: Return ONLY the JSON object, nothing else."""

        try:
            response = self.client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
            response_text = response.text.strip()
            
            # Parse JSON response
            result = json.loads(response_text)
            
            # Ensure all required fields exist
            result.setdefault('verdict', 'MIXED')
            result.setdefault('confidence', 50)
            result.setdefault('credibility_score', 5.0)
            result.setdefault('evidence_for', [])
            result.setdefault('evidence_against', [])
            result.setdefault('explanation', 'Analysis completed')
            
            print(f"✓ Verdict: {result['verdict']} (Confidence: {result['confidence']}%)")
            print(f"✓ Credibility Score: {result['credibility_score']}/10\n")
            
            return result
        
        except json.JSONDecodeError as e:
            print(f"⚠ Warning: Failed to parse credibility response: {e}")
            if 'response_text' in locals():
                print(f"Response was: {response_text}\n")
            # Return default structure on parse error
            return {
                "verdict": "MIXED",
                "confidence": 50,
                "credibility_score": 5.0,
                "evidence_for": [],
                "evidence_against": ["Unable to parse analysis response"],
                "explanation": "Analysis error - manual review recommended"
            }
        except Exception as e:
            print(f"❌ Error analyzing credibility: {str(e)}\n")
            return {
                "verdict": "MIXED",
                "confidence": 50,
                "credibility_score": 5.0,
                "evidence_for": [],
                "evidence_against": [str(e)],
                "explanation": f"Error during credibility analysis: {str(e)}"
            }
    
    def format_search_query(self, keywords: List[str], max_keywords: int = 5) -> str:
        """
        Format keywords into an optimized search query for NewsAPI.
        
        Args:
            keywords (List[str]): List of keywords
            max_keywords (int): Maximum keywords to use
            
        Returns:
            str: Formatted search query
        """
        # Take most relevant keywords and join with OR
        selected = keywords[:max_keywords]
        query = " OR ".join(selected)
        return query
