import os
import requests
import streamlit as st
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Web Intelligence",
    page_icon="🌐",
    layout="wide"
)

# ---------------- CUSTOM STYLES ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 24px;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
}

.title {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}

.snippet {
    font-size: 16px;
    color: #e0e0e0;
    margin-top: 10px;
}

.source {
    font-size: 14px;
    margin-top: 12px;
}

a {
    color: #4dd0e1;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>🌍 AI Web Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("Search the web. See **full context**. Know **exact sources**.")

# ---------------- SEARCH INPUT ----------------
query = st.text_input("🔍 Enter your search query", placeholder="e.g. What is quantum computing?")

# ---------------- SERPAPI SEARCH ----------------
def web_search(query):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "engine": "google",
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": 10
    }
    response = requests.get(url, params=params, timeout=15)
    data = response.json()
    return data.get("organic_results", [])

# ---------------- DISPLAY RESULTS ----------------
if query:
    with st.spinner("Scraping the internet intelligently 🧠"):
        results = web_search(query)

    if not results:
        st.warning("No results found.")
    else:
        for r in results:
            title = r.get("title", "No title")
            snippet = r.get("snippet", "No snippet available.")
            link = r.get("link", "#")
            source = r.get("source", "Unknown source")

            st.markdown(f"""
            <div class="card">
                <div class="title">{title}</div>
                <div class="snippet">{snippet}</div>
                <div class="source">
                    🔗 <a href="{link}" target="_blank">{link}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

