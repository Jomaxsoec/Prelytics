# agents/product_analysis.py

from utils.scraping import scrape_company_pages
from utils.nlp_tools import generate_product_analysis

AGILISIUM_OFFERINGS = {
    "cloud modernization": ["AWS", "Azure", "cloud migration", "data lakes"],
    "data engineering": ["ETL", "data pipelines", "databricks", "big data"],
    "AI/ML services": ["machine learning", "model training", "AI insights"],
    "BI & analytics": ["Power BI", "dashboards", "visualization", "reporting"],
    "governance & security": ["compliance", "data quality", "access control"]
}


def match_to_agilisium_offerings(text):
    matched_services = {}
    text_lower = text.lower()
    for service, keywords in AGILISIUM_OFFERINGS.items():
        matches = [kw for kw in keywords if kw.lower() in text_lower]
        if matches:
            matched_services[service] = matches
    return matched_services


def analyze_client(company_name: str, website_url: str) -> str:
    """Analyze client and generate product recommendations"""
    try:
        # Step 1: Scrape website content
        raw_text = scrape_company_pages(website_url)
        if not raw_text:
            return "Failed to extract text from website."

        # Step 2: Generate product analysis using NLP
        product_analysis = generate_product_analysis(company_name, raw_text)

        # Step 3: Match to Agilisium offerings
        matched_offerings = match_to_agilisium_offerings(raw_text)

        # Step 4: Create comprehensive report
        report = f"""
📊 PRODUCT ANALYSIS FOR {company_name.upper()}

{product_analysis}

🎯 AGILISIUM OFFERING MATCHES:
"""

        if matched_offerings:
            for service, keywords in matched_offerings.items():
                report += f"• {service.title()}: {', '.join(keywords)}\n"
        else:
            report += "• No direct matches found, but opportunities may exist based on industry analysis\n"

        return report

    except Exception as e:
        return f"Error during product analysis: {str(e)}"
