# Fake News Detection System

## 📋 Overview

The **Fake News Detection System** is an intelligent, AI-powered application designed to analyze news articles and determine their credibility. It leverages advanced natural language processing (NLP) and machine learning models to verify claims against reliable news sources, providing users with a comprehensive credibility assessment.

The system combines multiple technologies including web scraping for news verification, LLM-based analysis, and a user-friendly web interface to deliver actionable insights about news authenticity.

---

## ✨ Key Features

- **🎯 Credibility Analysis**: Verifies news articles against reliable sources
- **🔍 Keyword Extraction**: Automatically identifies key entities and topics
- **📊 Confidence Scoring**: Provides credibility scores (0-10) with confidence percentages
- **📰 Source Verification**: Cross-references with major news outlets
- **💡 Detailed Reports**: Generates comprehensive analysis reports with evidence
- **🖥️ Web Interface**: User-friendly frontend for easy news submission
- **⚡ RESTful API**: Backend API for programmatic access
- **🔐 Multi-LLM Support**: Compatible with Google Gemini and OpenRouter APIs
- **🎨 Real-time Results**: Instant verdict classification (REAL/FAKE/MISLEADING)

---

## 📁 Project Structure

```
newsprj/
├── app.py                      # Flask backend server
├── check_news.py               # Core news analysis logic
├── gemini_analyzer.py          # Google Gemini LLM integration
├── openrouter_analyzer.py      # OpenRouter LLM integration
├── truth_checker.py            # Truth verification engine
├── predictor/                  # ML model files
├── index.html                  # Frontend web interface
├── news_app.py                 # Auxiliary app module
├── test_models.py              # Testing utilities
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── today_news.txt              # Input news file
├── truth_analysis_report.txt   # Generated analysis output
├── USER_GUIDE.md               # User documentation
└── README.md                   # This file
```

---

## 🛠️ Prerequisites

Before running the application, ensure you have:

- **Python 3.8+** installed
- **pip** package manager
- **Git** (optional, for version control)
- Valid API keys for:
  - [NewsAPI](https://newsapi.org) - For news verification
  - [Google Gemini API](https://makersuite.google.com/app/apikey) OR [OpenRouter API](https://openrouter.ai) - For LLM analysis

---

## 📦 Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd newsprj
```

### 2. Create a Virtual Environment

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Create Environment Variables File

Create a `.env` file in the project root:

```bash
# Windows PowerShell
New-Item -Path .\.env -ItemType File

# macOS/Linux
touch .env
```

### 2. Add Your API Keys

Edit `.env` and add the following:

```env
# News API Configuration
NEWSAPI_KEY=your_newsapi_key_here

# LLM Provider Selection (gemini or openrouter)
LLM_PROVIDER=gemini

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# OpenRouter API (alternative)
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Verify Configuration

The application will automatically validate API keys on startup.

---

## 🚀 Quick Start

### Method 1: Command Line Usage

#### Step 1: Add Your News Article

Edit `today_news.txt` and paste your full article text (not just URLs):

```
Tesla Announces Revolutionary 500-Mile Battery Technology

Tesla announced today that it has developed a new battery technology 
that can store 500 miles of driving range on a single charge...
```

#### Step 2: Run the Analyzer

```bash
python check_news.py
```

#### Step 3: View Results

Results will display in the console and be saved to `truth_analysis_report.txt`

### Method 2: Web Interface

#### Step 1: Start the Flask Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

#### Step 2: Open the Frontend

- Open `index.html` in your web browser, or
- Navigate to `http://localhost:5000` if configured

#### Step 3: Submit Your News

Paste your article text in the interface and click "Check News"

---

## 📊 API Documentation

### Endpoint: `/check_news`

**Method:** `POST`

**Request Format:**
```json
{
  "text": "Your full news article text here..."
}
```

**Response Format:**
```json
{
  "verdict": "REAL",
  "confidence": 89,
  "credibility_score": 8.9,
  "keywords": ["Tesla", "Battery", "EV"],
  "top_sources": ["BBC", "Reuters", "TechCrunch"],
  "evidence_supporting": ["Multiple independent sources confirm..."],
  "evidence_against": [],
  "analysis": "Detailed analysis text..."
}
```

**Example cURL Request:**
```bash
curl -X POST http://localhost:5000/check_news \
  -H "Content-Type: application/json" \
  -d '{"text": "Your news article here..."}'
```

**Status Codes:**
- `200 OK` - Analysis successful
- `400 Bad Request` - Missing or invalid text field
- `500 Internal Server Error` - API key or analysis error

---

## 📋 Output Format

### Console Output Example

```
🔑 Keywords: Tesla, Battery Technology, 500 miles, EV
📰 Top Sources: BBC, Reuters, TechCrunch
✅ VERDICT: REAL
📊 Confidence: 89%
⭐ Credibility Score: 8.9/10
```

### Report File Example (`truth_analysis_report.txt`)

```
TRUTH CHECK REPORT
======================================================================

📝 ARTICLE: Tesla Announces Revolutionary 500-Mile Battery...
🔍 ANALYSIS DATE: 2026-05-13

EXTRACTED KEYWORDS & ENTITIES
- Keywords: Tesla, Battery, 500 miles, EV charging
- Entities: Tesla Inc., Electric Vehicle Industry

TOP CORROBORATING SOURCES
1. BBC News - "Tesla's New Battery Tech Cuts Charging Time"
2. Reuters - "Electric Vehicle Battery Breakthrough"
3. TechCrunch - "Tesla's Battery Innovation Details"

CREDIBILITY ANALYSIS
✅ VERDICT: REAL
📊 Confidence: 89%
⭐ Credibility Score: 8.9/10

EVIDENCE SUPPORTING:
- Multiple independent sources confirm announcement
- Technical specs align across reports
- Stock price movement corroborates news

EVIDENCE AGAINST:
- None found in analyzed sources
```

---

## 🔄 Verdict Classifications

| Verdict | Description |
|---------|-------------|
| **REAL** ✅ | Article is supported by credible sources; high confidence in authenticity |
| **FAKE** ❌ | Article contradicts reliable sources; appears to contain misinformation |
| **MISLEADING** ⚠️ | Article contains partial truths mixed with unverified claims |

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Flask 3.0.0 |
| **LLM Analysis** | Google Gemini / OpenRouter |
| **News Verification** | NewsAPI |
| **ML/NLP** | scikit-learn, joblib |
| **Data Processing** | pandas |
| **HTTP Client** | requests |
| **Frontend** | HTML5, CSS3, JavaScript |
| **CORS Support** | flask-cors |
| **Environment** | python-dotenv |

---

## 🐛 Troubleshooting

### Issue: "API keys not configured"
**Solution:** Verify your `.env` file exists with valid API keys and is in the project root directory.

### Issue: "Connection refused" on localhost
**Solution:** Ensure the Flask server is running with `python app.py` and check that port 5000 is not in use.

### Issue: "Empty text provided"
**Solution:** Ensure you've added actual article content to the submission, not just URLs or headlines.

### Issue: "Analysis failed"
**Solution:** Check API key validity and ensure you have internet connectivity for news verification.

---

## 📚 Additional Resources

- [USER_GUIDE.md](USER_GUIDE.md) - Detailed user guide with examples
- [NewsAPI Documentation](https://newsapi.org/docs) - News data provider
- [Google Gemini API](https://ai.google.dev/tutorials/python_quickstart) - LLM documentation
- [Flask Documentation](https://flask.palletsprojects.com/) - Backend framework

---

## 📝 License

This project is provided as-is for educational and research purposes.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Submit a pull request

---

## 📞 Support

For issues, questions, or suggestions, please:

- Check the [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions
- Review the troubleshooting section above
- Examine error messages in console output

---

## 🎯 Future Enhancements

- [ ] Support for multiple articles batch processing
- [ ] Image and video analysis capabilities
- [ ] User authentication and history tracking
- [ ] Enhanced credibility visualization dashboard
- [ ] Mobile app development
- [ ] Real-time news feed integration
- [ ] Multilingual support

---

**Last Updated:** May 2026  
**Version:** 1.0.0  
**Status:** Production Ready
