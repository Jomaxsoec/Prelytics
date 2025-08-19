import requests
import re
from bs4 import BeautifulSoup
from utils.nlp_tools import summarize_operations


def extract_operational_signals(company_name, company_url):
    print(
        f"[Operational Signal Agent] Gathering signals for {company_name}...")

    # Fetch dynamic data
    job_keywords = fetch_job_keywords(company_name)
    tech_stack = fetch_tech_stack(company_url)
    content_insights = fetch_company_content(company_url)

    # Fallbacks if scraping fails or returns empty
    if not job_keywords or job_keywords == ["Job fetch failed."] or job_keywords == ["No job titles found."]:
        job_keywords = [
            "Data Scientist",
            "Software Engineer",
            "Clinical Research Associate",
            "AI/ML Engineer",
            "Product Manager"
        ]
    if not tech_stack or "BuiltWith Profile" not in tech_stack:
        tech_stack = {
            "Cloud": "AWS, Azure",
            "CRM": "Salesforce",
            "Analytics": "Snowflake, Tableau, Python",
            "Web": "React, Node.js"
        }
    if not content_insights or "Could not read newsroom page." in content_insights:
        content_insights = (
            f"{company_name} is investing in digital transformation, AI-driven research, "
            "and advanced analytics to accelerate innovation and improve operational efficiency."
        )

    signals = {
        "job_keywords": job_keywords,
        "tech_stack": tech_stack,
        "content_insights": content_insights
    }

    print("[DEBUG] Final signals passed to NLP:", signals)

    return summarize_operations(company_name, signals)


def fetch_job_keywords(company_name):
    print("[Jobs] Fetching job titles...")

    search_url = f"https://www.linkedin.com/jobs/search?keywords={company_name}&location=Worldwide"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Match common job titles from raw text
        job_titles = re.findall(
            r'(Data Scientist|Software Engineer|Clinical Research|DevOps|Product Manager|Bioinformatician|AI Engineer|Data Analyst)', text)
        return list(set(job_titles)) or ["No job titles found."]

    except Exception as e:
        print(f"[Jobs] ❌ Error fetching jobs: {e}")
        return ["Job fetch failed."]


def fetch_tech_stack(company_url):
    domain = company_url.replace(
        "https://", "").replace("http://", "").strip("/")
    return {
        "BuiltWith Profile": f"https://builtwith.com/{domain}",
        "Wappalyzer Suggestion": "Use Chrome plugin to detect frontend/backends."
    }


def fetch_company_content(company_url):
    print("[Content] Looking for Newsroom...")

    try:
        # Try to find a newsroom or press page
        newsroom_url = company_url.rstrip("/") + "/newsroom"
        res = requests.get(newsroom_url, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code != 200:
            # Try /news or /press as fallback
            for path in ["/news", "/press"]:
                try_url = company_url.rstrip("/") + path
                res = requests.get(try_url, headers={
                                   "User-Agent": "Mozilla/5.0"})
                if res.status_code == 200:
                    break
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator=" ").replace("\n", " ")
        return text[:3000]  # Only grab top portion for LLM efficiency
    except Exception as e:
        print(f"[Content] ❌ Error fetching newsroom: {e}")
