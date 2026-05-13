from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from check_news import check_news_text

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# Load environment variables
load_dotenv()

@app.route('/check_news', methods=['POST'])
def check_news():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400
        
        article_text = data['text'].strip()
        if not article_text:
            return jsonify({"error": "Empty text provided"}), 400
        
        # Get API keys from environment
        newsapi_key = os.getenv('NEWSAPI_KEY')
        llm_provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
        
        if llm_provider == 'openrouter':
            analyzer_api_key = os.getenv('OPENROUTER_API_KEY')
        else:
            analyzer_api_key = os.getenv('GEMINI_API_KEY')
        
        if not newsapi_key or not analyzer_api_key:
            return jsonify({"error": "API keys not configured"}), 500
        
        # Run analysis
        result = check_news_text(article_text, newsapi_key, analyzer_api_key, llm_provider)
        
        # Transform to frontend format
        frontend_result = transform_to_frontend_format(result)
        
        return jsonify(frontend_result)
    
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

def transform_to_frontend_format(result: dict) -> dict:
    """Transform backend result to frontend expected JSON format."""
    credibility = result.get('credibility', {})
    verdict_map = {"TRUE": "REAL", "FALSE": "FAKE", "MIXED": "MISLEADING"}
    verdict = verdict_map.get(credibility.get('verdict', 'MIXED'), 'MISLEADING')
    
    confidence = credibility.get('confidence', 50)
    credibility_score = int(credibility.get('credibility_score', 5.0) * 10)  # 0-10 to 0-100
    
    # Estimate metrics
    related_count = len(result.get('related_articles', []))
    evidence_for = len(credibility.get('evidence_for', []))
    evidence_against = len(credibility.get('evidence_against', []))
    
    source_quality_score = min(related_count * 10, 100)
    source_quality_label = "High" if source_quality_score > 70 else "Medium" if source_quality_score > 30 else "Low"
    
    factual_accuracy_score = max(0, min(100, (evidence_for - evidence_against) * 20 + 50))
    factual_accuracy_label = "High" if factual_accuracy_score > 70 else "Medium" if factual_accuracy_score > 30 else "Low"
    
    bias_level_score = 50  # Placeholder, could analyze further
    bias_level_label = "Neutral"
    
    emotional_tone_score = 50  # Placeholder
    emotional_tone_label = "Neutral"
    
    # Probability distribution
    if verdict == "REAL":
        prob_fake = 100 - confidence
        prob_real = confidence
        prob_misleading = 0
    elif verdict == "FAKE":
        prob_fake = confidence
        prob_real = 100 - confidence
        prob_misleading = 0
    else:  # MISLEADING
        prob_fake = confidence // 2
        prob_misleading = confidence
        prob_real = 100 - confidence - prob_fake
    
    # Signals
    signals = []
    for ev in credibility.get('evidence_for', []):
        signals.append({"type": "green", "text": ev})
    for ev in credibility.get('evidence_against', []):
        signals.append({"type": "red", "text": ev})
    if not signals:
        signals.append({"type": "yellow", "text": "No specific signals detected"})
    
    return {
        "verdict": verdict,
        "credibility_score": credibility_score,
        "summary": credibility.get('explanation', 'Analysis completed'),
        "source_quality": {"label": source_quality_label, "score": source_quality_score},
        "factual_accuracy": {"label": factual_accuracy_label, "score": factual_accuracy_score},
        "bias_level": {"label": bias_level_label, "score": bias_level_score},
        "emotional_tone": {"label": emotional_tone_label, "score": emotional_tone_score},
        "probability": {
            "fake": prob_fake,
            "misleading": prob_misleading,
            "real": prob_real
        },
        "signals": signals[:4],  # Limit to 4
        "detailed_analysis": credibility.get('explanation', 'Detailed analysis not available'),
        "related_articles": result.get('related_articles', [])
    }

@app.route('/')
def index():
    """Serve the frontend HTML."""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)