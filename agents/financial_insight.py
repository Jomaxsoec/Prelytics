import json
import pandas as pd
import yfinance as yf
from utils.nlp_tools import summarize_financials, generate_swot_analysis, compute_cagr

# Company name to stock symbol mapping
COMPANY_TO_SYMBOL = {
    "AMGN": "AMGN",
    "AMGEN": "AMGN",
    "REGENERON": "REGN",
    "BIOGEN": "BIIB",
    "MODERNA": "MRNA",
    "ELI LILLY": "LLY",
    "LILLY": "LLY",
    "SANOFI": "SNY",
    "ASTRAZENECA": "AZN",
    "TAKEDA": "TAK",
    "NOVO NORDISK": "NVO",
    "ROCHE": "RHHBY",
    "GSK": "GSK",
    "GLAXOSMITHKLINE": "GSK",
    "TEVA": "TEVA",
    "BAYER": "BAYRY",
    "NOVARTIS": "NVS",
    "GENMAB": "GMAB",
    "PFIZER": "PFE",
    "JOHNSON & JOHNSON": "JNJ",
}


def get_stock_symbol(company_name):
    """Convert company name to stock symbol"""
    return COMPANY_TO_SYMBOL.get(company_name.upper())


def analyze_financials(company_name):
    """Main function to analyze financial data for a company"""
    print(
        f"[Financial Insight Agent] Fetching financial snapshot for {company_name}...")

    stock_symbol = get_stock_symbol(company_name)

    if stock_symbol is None:
        return f"[Warning] {company_name} appears to be a private company. No public financial data available."

    try:
        # Get stock data
        stock = yf.Ticker(stock_symbol)
        info = stock.info

        # Debug: Print available keys
        print(f"[Financial Insight Agent] Available keys: {list(info.keys())}")

        # Try different methods to get financial data
        # Method 1: From info
        revenue = info.get("revenue", 0)
        net_income = info.get("netIncome", 0)

        # Method 2: Try financials if info doesn't work
        if revenue == 0 or net_income == 0:
            try:
                financials = stock.financials
                if not financials.empty:
                    # Get latest year's data
                    latest_year = financials.columns[0]
                    revenue = financials.loc['Total Revenue',
                                             latest_year] if 'Total Revenue' in financials.index else 0
                    net_income = financials.loc['Net Income',
                                                latest_year] if 'Net Income' in financials.index else 0
                    print(
                        f"[Financial Insight Agent] Retrieved from financials: Revenue={revenue}, Net Income={net_income}")
            except Exception as e:
                print(
                    f"[Financial Insight Agent] Could not get financials: {e}")

        # Method 3: Try quarterly data
        if revenue == 0 or net_income == 0:
            try:
                quarterly = stock.quarterly_financials
                if not quarterly.empty:
                    latest_quarter = quarterly.columns[0]
                    revenue = quarterly.loc['Total Revenue',
                                            latest_quarter] if 'Total Revenue' in quarterly.index else 0
                    net_income = quarterly.loc['Net Income',
                                               latest_quarter] if 'Net Income' in quarterly.index else 0
                    print(
                        f"[Financial Insight Agent] Retrieved from quarterly: Revenue={revenue}, Net Income={net_income}")
            except Exception as e:
                print(
                    f"[Financial Insight Agent] Could not get quarterly data: {e}")

        # Extract key metrics with better formatting
        metrics = {
            "revenue": revenue,
            "netIncome": net_income,
            "grossMargins": info.get("grossMargins", 0),
            "ebitdaMargins": info.get("ebitdaMargins", 0),
            "operatingMargins": info.get("operatingMargins", 0),
            "profitMargins": info.get("profitMargins", 0),
            "revenueGrowth": info.get("revenueGrowth", 0),
            "returnOnEquity": info.get("returnOnEquity", 0),
            "totalDebt": info.get("totalDebt", 0),
            "totalCash": info.get("totalCash", 0),
            "freeCashflow": info.get("freeCashflow", 0),
            "currentRatio": info.get("currentRatio", 0),
            "quickRatio": info.get("quickRatio", 0),
            "debtToEquity": info.get("debtToEquity", 0)
        }

        # Debug: Print key metrics
        print(
            f"[Financial Insight Agent] Key metrics: Revenue={metrics['revenue']}, Net Income={metrics['netIncome']}")

        # Convert to JSON string for processing
        financial_json = json.dumps(metrics, indent=2)

        print(
            f"[Financial Insight Agent] Found {len(metrics)} financial metrics.")

        # Use existing function to process the data
        return extract_financial_insights(company_name, financial_json)

    except Exception as e:
        print(f"[Financial Insight Agent] Error: {e}")
        return f"[Error] Failed to fetch financial data: {str(e)}"


def extract_financial_insights(company_name, raw_financial_json):
    print(
        f"[Financial Insight Agent] Processing financials for {company_name}...")

    if not raw_financial_json:
        return "No financial data available."

    try:
        # Step 1: Summarize insights using OpenAI
        financial_summary = summarize_financials(
            company_name, raw_financial_json)

        # Step 2: Parse financial JSON (assuming it's structured)
        raw_data = json.loads(raw_financial_json)

        # Format numbers for better display
        def format_currency(value):
            if value == 0:
                return "N/A"
            elif value >= 1e9:
                return f"${value/1e9:.2f}B"
            elif value >= 1e6:
                return f"${value/1e6:.2f}M"
            elif value >= 1e3:
                return f"${value/1e3:.2f}K"
            else:
                return f"${value:.2f}"

        def format_percentage(value):
            if value == 0:
                return "N/A"
            else:
                return f"{value*100:.2f}%"

        def format_ratio(value):
            if value == 0:
                return "N/A"
            else:
                return f"{value:.2f}"

        metrics = {
            "Revenue": format_currency(raw_data.get("revenue", 0)),
            "Net Income": format_currency(raw_data.get("netIncome", 0)),
            "Gross Margin (%)": format_percentage(raw_data.get("grossMargins", 0)),
            "EBITDA Margin (%)": format_percentage(raw_data.get("ebitdaMargins", 0)),
            "Operating Margin (%)": format_percentage(raw_data.get("operatingMargins", 0)),
            "Profit Margin (%)": format_percentage(raw_data.get("profitMargins", 0)),
            "Revenue Growth (%)": format_percentage(raw_data.get("revenueGrowth", 0)),
            "Return on Equity (%)": format_percentage(raw_data.get("returnOnEquity", 0)),
            "Free Cash Flow": format_currency(raw_data.get("freeCashflow", 0)),
            "Total Debt": format_currency(raw_data.get("totalDebt", 0)),
            "Total Cash": format_currency(raw_data.get("totalCash", 0)),
            "Current Ratio": format_ratio(raw_data.get("currentRatio", 0)),
            "Quick Ratio": format_ratio(raw_data.get("quickRatio", 0)),
            "Debt-to-Equity": format_ratio(raw_data.get("debtToEquity", 0)),
        }

        df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])

        # Step 3: Calculate CAGR if revenue history is available
        cagr_result = compute_cagr(company_name, raw_financial_json)

        # Step 4: Run SWOT Analysis
        swot = generate_swot_analysis(company_name, raw_financial_json)

        output = f"{company_name} Financial Briefing:\n\n"
        output += financial_summary
        output += "\n\n==== FINANCIAL METRICS ====\n"
        output += df.to_string(index=False)
        output += f"\n\n{cagr_result}"

        output += "\n\n==== SWOT ANALYSIS ====\n" + swot
        return output

    except Exception as e:
        return f"[Error] Failed to process financial data: {str(e)}"
