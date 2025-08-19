from utils.nlp_tools import get_agilisium_competitors_for_client


def extract_competitor_analysis(company_name):
    print(
        f"[Competitor Analysis Agent] Finding competitors of Agilisium for client: {company_name}...")
    return get_agilisium_competitors_for_client(company_name)
