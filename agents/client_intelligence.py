from utils.scraping import scrape_company_pages
from utils.nlp_tools import summarize_company_info
import openai

def extract_profile(company_name, company_url):
    print(f"[Client Intelligence Agent] Scraping {company_url}")
    raw_text = scrape_company_pages(company_url)

    if not raw_text.strip():
        print("[Client Intelligence Agent] No content scraped from the website.")
        return None

    print(f"[Client Intelligence Agent] Scraped {len(raw_text)} characters.")
    summary = summarize_company_info(company_name, raw_text)
    return summary
    
def extract_leadership_names(company_url):
    print("[Leadership] Looking for leadership names...")
    leadership_text = scrape_company_pages(company_url, extra_paths=["/leadership", "/executives", "/management"])

    if not leadership_text.strip():
        return "No leadership content found."

    prompt = f"""
    From the following content, extract the top 3 leadership members (name + title).
    Be concise and accurate.
    
    Format your response with clean bullet points using • symbols. Do not use asterisks (*) anywhere in your response.

    Content:
    {leadership_text[:8000]}
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a business intelligence analyst. Extract leadership information accurately."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Leadership] Error during leadership extraction: {e}")
        return "Error during leadership extraction."