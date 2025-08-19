import openai
import os

# Set your OpenAI API Key
# Or hardcode for local testing
openai.api_key = os.getenv(
    "OPENAI_API_KEY", "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")


def summarize_company_info(company_name, raw_text):
    if not raw_text.strip():
        print("[NLP] No text received for summarization.")
        return "No content available to summarize."

    trimmed_text = raw_text[:6000]
    print(
        f"[NLP] Received {len(trimmed_text)} characters of text for {company_name}")
    print(f"[NLP] Preview:\n{trimmed_text[:250]}...\n")

    prompt = f"""
        Your job is to explain clearly and helpfully what {company_name} does based on this raw website content.

        Don't use fluff or corporate buzzwords. Be specific, grounded, and easy to follow — like a smart person explaining to another.

        Respond in this exact format, using these exact labels and bullets, and start each bullet on a new line:

        • What the company does: [your answer]
        • Who their typical customers are: [your answer]
        • What technologies or platforms they rely on: [your answer]
        • Strategic priorities or focus areas: [your answer]

        Do not add or remove any labels. Do not repeat the label in your answer. Start each bullet on a new line.

        Raw website content:
        {trimmed_text}
            """

    print("[NLP] Sending data to OpenAI GPT-3.5 for summarization...")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        result = response.choices[0].message.content.strip()
        print(
            f"[NLP] Successfully received response ({len(result)} characters).")
        return result

    except Exception as e:
        print(f"[NLP] Error during summarization: {e}")
        return (
            "We couldn't summarize the company info at this time. "
            f"Error: {str(e)}"
        )

def summarize_financials(company_name, raw_json):
    prompt = f"""
You are a financial analyst reviewing data for {company_name}.

1. Revenue/profit trends
2. Growth/stability indicators
3. Debt or cash flow observations
4. Red flags or risks

Keep it crisp. Use • bullet points.

Data:
{raw_json[:3500]}
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[NLP] Error during financial analysis: {e}")
        return f"Error during AI processing: {str(e)}"


def generate_swot_analysis(company_name, raw_json):
    prompt = f"""
Act as a business strategist. Perform a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
for {company_name} using the following financial data give me 3 points for each:

{raw_json[:3500]}

Format:
Strengths:
- ...
Weaknesses:
- ...
Opportunities:
- ...
Threats:
- ...
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[NLP] Error during SWOT analysis: {e}")
        return f"Error during AI processing: {str(e)}"


def compute_cagr(company_name, financial_data):
    """Compute CAGR using OpenAI"""
    prompt = f"""
    Calculate the Compound Annual Growth Rate (CAGR) for {company_name} based on this financial data:
    
    {financial_data}
    
    If sufficient data is available, provide the CAGR calculation. If not, indicate "Not Available".
    """

    print("[NLP] Computing CAGR...")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[NLP] Error during CAGR calculation: {e}")
        return f"Error during AI processing: {str(e)}"


def summarize_operations(company_name, signals: dict):
    prompt = f"""
Help me understand how {company_name} operates based on this data.

Look at:
• What roles they're hiring
• Their tech stack
• Insights from blog or press

Now break it down:
• What kind of talent are they looking for?
• What's their technical direction?
• What initiatives are they working on?
• Where might they need help or be falling short?

Keep it real and readable. Be smart but clear. No corporate tone. bullet points should be in next line. And give enough space after each bullet point.

Signals:
- Job Roles: {signals.get("job_keywords", [])}
- Tech Stack: {signals.get("tech_stack", {})}
- Content Insights: {signals.get("content_insights", "")}
    """
    print("[NLP] Sending operational signals for summarization...")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[NLP] Error during operations analysis: {e}")
        return f"Error during AI processing: {str(e)}"


# def summarize_competition(client_name, text_block):
#     prompt = f"""
# You're a competitive analyst. Based on this info, identify key IT or consulting firms working with {client_name}.

# For each one, break down:
# • Who they are
# • What they offer to {client_name}
# • Strengths
# • Weaknesses
# • How to position against them

# Make it sharp. Use bold font for "who they are". Use • bullets. Be clear, not fluffy. Skip buzzwords. give space between each bullet point.

# Text block:
# {text_block}
#     """
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         print(f"[NLP] Error during competition analysis: {e}")
#         return f"Error during AI processing: {str(e)}"


def get_agilisium_competitors_for_client(client_name):
    prompt = f"""
You're working at Agilisium Consulting and your client is {client_name}.

Analyze the competitive landscape for {client_name} and identify top consulting, data analytics, and technology firms that serve similar biotech/life sciences clients.

For each competitor, provide detailed analysis in this exact format:

• [Competitor Name]:
  Services: [List their main services for {client_name} or similar clients]
  Strengths: [3-4 key strengths]
  Weaknesses: [3-4 key weaknesses]
  Agilisium Advantage: [How Agilisium can differentiate]


Provide top 3 detailed competitor analyses that are on same level with AGILISIUM. Use bullet points for each section. Make it comprehensive and actionable.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        result = response.choices[0].message.content.strip()
        print(f"[NLP] Competitor analysis generated: {len(result)} characters")

        # If the result is too short or contains error, provide fallback
        if len(result) < 100 or "Error" in result:
            print("[NLP] Providing fallback competitor analysis")
            return get_fallback_competitor_analysis(client_name)

        return result
    except Exception as e:
        print(f"[NLP] Error during competitor analysis: {e}")
        return get_fallback_competitor_analysis(client_name)


# def get_agilisium_competitor_analysis(client_name):
#     """
#     Uses OpenAI (GPT-3.5) to generate a competitive analysis of Agilisium
#     against other consulting firms for a given client in life sciences.
#     """
#     prompt = f"""
# You're a strategy analyst at Agilisium Consulting.

# Our client is {client_name}, a major player in the life sciences/biotech sector.

# Find 4–5 major consulting or data analytics firms that are likely competitors of Agilisium for {client_name}.

# For each competitor, describe:
# • Name
# • Services offered to {client_name} or similar clients
# • Strengths
# • Weaknesses
# • How Agilisium can differentiate

# Write clearly, use • bullets, and avoid fluff or generic phrases.
# """
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.4
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         print(f"[NLP] Error in Agilisium competitor analysis: {e}")
#         return f"[Error] Unable to generate competitor analysis: {str(e)}"


def generate_product_analysis(company_name, raw_text):
    """Generate product analysis using OpenAI"""
    prompt = f"""
Create a comprehensive product analysis for {company_name} based on this text:

{raw_text[:10000]}

Provide analysis in this exact format with clear headings:

CLIENT STRATEGY MEMO
[Provide strategic insights about the client's business model, market position, and key challenges]

CLIENT OPPORTUNITY BRIEF
[Identify specific opportunities where Agilisium can add value, including pain points and business needs]

AGILISIUM PRODUCT FIT
[Detail how Agilisium's services align with the client's needs, including specific solutions and capabilities]

COMPETITIVE POSITIONING
[Analyze how Agilisium can differentiate from competitors and position itself effectively]


PITCH STRATEGY
[Develop a detailed, step-by-step pitch strategy for engaging with {company_name}. 
- Use only the information from the provided text—do not use generic or boilerplate advice.
- Reference the client's actual business lines, products, or recent news as found in the text.
- Specify the most relevant Agilisium offerings and how they address the client's unique challenges.
- Suggest concrete actions, outreach methods, and key stakeholders to target (by role or department if possible).
- Tailor the messaging and value propositions to the client's stated goals, pain points, and industry context.
- Make the recommendations practical, actionable, and specific to {company_name}.]

    """

    print("[NLP] Generating product analysis...")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[NLP] Error during product analysis: {e}")
        return get_fallback_product_analysis(company_name)


def get_fallback_product_analysis(company_name):
    """Provide fallback product analysis when AI fails"""
    return f"""
CLIENT STRATEGY MEMO
{company_name} operates in the biotech/life sciences sector with a focus on innovation and research. The company likely faces challenges in data management, regulatory compliance, and scaling operations efficiently. Their strategic priorities include accelerating drug development, optimizing clinical trials, and maintaining competitive advantage through technology adoption.

CLIENT OPPORTUNITY BRIEF
Key opportunities for Agilisium engagement include:
• Data analytics and insights for clinical trial optimization
• Regulatory compliance and reporting automation
• Digital transformation of research and development processes
• Patient data management and privacy solutions
• Supply chain optimization and risk management

AGILISIUM PRODUCT FIT
Agilisium's specialized services align perfectly with {company_name}'s needs:
• Advanced analytics and machine learning for drug discovery
• Cloud-based data management and security solutions
• Regulatory compliance automation and reporting
• Clinical trial data integration and analysis
• Custom software development for research workflows

COMPETITIVE POSITIONING
Agilisium differentiates through:
• Deep biotech industry expertise and domain knowledge
• Faster implementation and time-to-value
• Cost-effective solutions compared to large consultancies
• Personalized service and dedicated support
• Specialized technical capabilities in life sciences

PITCH STRATEGY
Recommended approach for engaging {company_name}:
• Focus on specific pain points in clinical trial management
• Demonstrate ROI through case studies and success metrics
• Emphasize regulatory compliance and risk mitigation
• Offer pilot programs to prove value quickly
• Leverage industry expertise and thought leadership
"""
