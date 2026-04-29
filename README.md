# 🚀 AI-Powered Multi-Platform Content Generator

This is a Streamlit-based AI application that generates high-quality content for multiple platforms like Instagram, LinkedIn, Twitter, and Blogs.
It also evaluates and improves the generated content using AI.

---

## Features

* Generate platform-specific content instantly
* Supports Instagram, LinkedIn, Twitter & Blog
* Tone selection (Professional, Casual, Motivational, Funny)
* AI-based content evaluation (engagement & readability)
* One-click content improvement (enhanced version)
* Download all generated content
* Dark mode support
* History tracking

---

## Tech Stack

* Python
* Streamlit
* OpenAI API

---

## How It Works

1. Enter a topic and target audience
2. Select tone (Professional, Casual, etc.)
3. Click **Generate**
4. AI creates content for:

   * Instagram
   * LinkedIn
   * Twitter
   * Blog
5. View AI-based evaluation
6. Improve content using the **Improve button**
7. Download all content if needed

---

## How to Run

1. Install dependencies:

pip install -r requirements.txt

2. Add your API key:

Create `.streamlit/secrets.toml` and add:

OPENAI_API_KEY = "your_api_key_here"

3. Run the app:

streamlit run app.py

---

## Project Structure

AI-Content-Generator/

├── app.py
├── requirements.txt
├── README.md

---

## Use Cases

* Social media content creation
* Blogging assistance
* Marketing content generation
* Student & creator productivity

---

## Future Improvements

* Image generation for posts
* SEO optimization suggestions
* Content scheduling feature
* Analytics dashboard
  
