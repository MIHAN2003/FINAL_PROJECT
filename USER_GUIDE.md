# How to Use the Fake News Detection System

## 📝 Adding Your News to Check

The system reads news from `today_news.txt`. Here's how to use it:

### Step 1: Prepare Your News Article

Add your **news article content** (not just URLs) to `today_news.txt`. The article should be in **plain text format**.

### Example Format for `today_news.txt`:

```
Tesla Announces Revolutionary 500-Mile Battery Technology

Tesla announced today that it has developed a new battery technology that can store 500 miles of driving range on a single charge. The company claims this breakthrough will revolutionize the electric vehicle industry and make EVs more competitive with gasoline-powered cars. 

The new battery uses advanced solid-state technology that the company has been developing for over five years. Tesla plans to begin production of vehicles with this technology in 2027. Industry analysts believe this development could accelerate EV adoption and potentially eliminate range anxiety concerns among consumers.

The company's stock price rose 5% on the news.
```

### Important Notes:
- **Include full article text**, not just headlines and URLs
- **Remove URLs** - the system will search for related articles automatically
- **One article per check** - add one article at a time
- Keep the text **clear and readable**

---

## 🚀 Running the Fact Checker

### Step 1: Add your news to `today_news.txt`
Simply replace the content with your news article text

### Step 2: Run the checker
```bash
python check_news.py
```

### Step 3: View Results

Two files are created:

1. **Console Output** - Displays:
   - Keywords extracted from your article
   - Top related news sources
   - **Verdict**: TRUE ✅ / FALSE ❌ / MIXED ⚠️
   - Confidence percentage
   - Credibility score (0-10)

2. **`truth_analysis_report.txt`** - Detailed report with:
   - Full keyword analysis
   - Top 3 corroborating sources
   - Evidence supporting the article
   - Evidence against or missing
   - Detailed explanation

---

## 📊 Output Example

### Console Output:
```
🔑 Keywords: Tesla, Battery Technology, 500 miles, EV
📰 Top Sources: BBC, Reuters, TechCrunch
✅ VERDICT: TRUE
📊 Confidence: 89%
⭐ Credibility Score: 8.9/10

```

### File Report: `truth_analysis_report.txt`
```
TRUTH CHECK REPORT
======================================================================

📝 ARTICLE: Tesla Announces Revolutionary 500-Mile Battery...
🔍 ANALYSIS DATE: 2026-04-23

EXTRACTED KEYWORDS & ENTITIES
- Keywords: Tesla, Battery, 500 miles, EV charging, solid-state
- Entities: Tesla Inc., Electric Vehicle Industry

TOP CORROBORATING SOURCES
1. BBC News - "Tesla's New Battery Tech Cuts Charging Time"
2. Reuters - "Electric Vehicle Battery Breakthrough"
3. TechCrunch - "Tesla's Battery Innovation Details"

CREDIBILITY ANALYSIS
✅ VERDICT: TRUE
📊 Confidence: 89%
⭐ Credibility Score: 8.9/10

EVIDENCE SUPPORTING:
- Multiple independent sources confirm announcement
- Technical specs align across reports
- Stock price movement corroborates news

EVIDENCE AGAINST:
- None found

Report generated: 2026-04-23 HH:MM:SS
```

---

## ✅ Quick Start

### To Test the System:

1. **Copy this sample article** and paste into `today_news.txt`:
```
SpaceX Successfully Launches Starship to Orbit

SpaceX announced today that its Starship vehicle successfully reached orbit for the third time this month. The company successfully launched from Starbase in Texas and completed multiple test objectives. The vehicle demonstrated improved landing precision and fuel efficiency compared to previous test flights.

This achievement brings SpaceX closer to its goal of enabling humans to live on Mars. NASA has selected Starship as the lunar lander for future Artemis missions. Industry experts believe this success increases the likelihood of human Moon missions within the next two years.

The successful launch has renewed investor confidence in SpaceX's commercial space venture.
```

2. **Run the checker**:
```bash
python check_news.py
```

3. **Check results**:
   - Look at terminal output for quick verdict
   - Open `truth_analysis_report.txt` for full analysis

---

## � Switching Between LLM Providers

The system supports two LLM providers: **Gemini** (Google) and **OpenRouter** (multiple models).

### To Switch Providers:

1. **Edit `.env` file**:
   ```bash
   # For Gemini (default)
   LLM_PROVIDER=gemini
   
   # For OpenRouter
   LLM_PROVIDER=openrouter
   ```

2. **Add the appropriate API key**:
   ```bash
   # For Gemini
   GEMINI_API_KEY=your_gemini_key_here
   
   # For OpenRouter
   OPENROUTER_API_KEY=your_openrouter_key_here
   ```

3. **Get API Keys**:
   - **Gemini**: https://ai.google.dev (free tier available)
   - **OpenRouter**: https://openrouter.ai (supports GPT-4, Claude, etc.)

4. **Available OpenRouter Models**:
   - `gpt-3.5-turbo` (fast, cheap)
   - `gpt-4` (powerful, expensive)
   - `claude-3-sonnet` (good balance)
   - `llama-2-70b` (open source)

### Example `.env` Configurations:

**Using Gemini:**
```bash
NEWSAPI_KEY=your_newsapi_key
GEMINI_API_KEY=your_gemini_key
LLM_PROVIDER=gemini
```

**Using OpenRouter:**
```bash
NEWSAPI_KEY=your_newsapi_key
OPENROUTER_API_KEY=your_openrouter_key
LLM_PROVIDER=openrouter
```

---

## ❓ FAQ

**Q: Why are there no keywords?**
A: Make sure `today_news.txt` contains actual **article content**, not just headlines or URLs.

**Q: Can I check multiple articles?**
A: Yes, but one at a time. After checking one, replace `today_news.txt` with the next article and run again.

**Q: What if the system says "No related articles found"?**
A: This means the search found no news about the topic. Try a different article with more common keywords.

**Q: How accurate is the verdict?**
A: The system uses both AI (Gemini) and ML models. It's a credibility score, not 100% definitive. Always verify critical information independently.

---

## 📌 Important Tips

✅ **DO:**
- Include full article text with multiple sentences
- Use articles from reputable news sources as input
- Check the `truth_analysis_report.txt` for detailed evidence

❌ **DON'T:**
- Submit only headlines or URLs
- Add multiple articles at once
- Treat the verdict as 100% accurate - verify independently
- Share API keys in code (use `.env` file)

---

**Need help?** Check that:
1. `.env` file exists with API keys
2. `today_news.txt` has actual article content
3. All dependencies are installed: `pip install -r requirements.txt`
