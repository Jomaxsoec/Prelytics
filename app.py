from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from coordinator_agent import CoordinatorAgent
import os

app = Flask(__name__)
CORS(app)

# Enable debug mode for auto-reload
app.debug = True
app.config['DEBUG'] = True

# Serve static files


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        company_name = data.get('companyName', '')
        company_url = data.get('companyUrl', '')

        if not company_name or not company_url:
            return jsonify({'error': 'Company name and URL are required'}), 400

        print(
            f"[DEBUG] CoordinatorAgent initialized with {company_name}, {company_url}")

        # Initialize and run the coordinator agent
        coordinator = CoordinatorAgent(company_name, company_url)
        results = coordinator.run_workflow()

        # Parse the results into structured data
        parsed_results = parse_analysis_results(results, company_name)

        return jsonify(parsed_results)

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500


def parse_analysis_results(results, company_name):
    """Parse the analysis results into structured data for the frontend"""

    # Extract financial metrics
    financial_metrics = {}
    if '==== FINANCIAL METRICS ====' in results:
        metrics_section = results.split('==== FINANCIAL METRICS ====')[
            1].split('====')[0]
        lines = metrics_section.strip().split('\n')

        for line in lines:
            if line.strip() and 'Metric' not in line and 'Value' not in line and '----' not in line:
                parts = line.split()
                if len(parts) >= 2:
                    # Find where the value starts
                    value_start = -1
                    for i, part in enumerate(parts):
                        if part.startswith('$') or part.endswith('%') or part.endswith('B') or part.endswith('M'):
                            value_start = i
                            break

                    if value_start != -1:
                        metric = ' '.join(parts[:value_start])
                        value = ' '.join(parts[value_start:])
                        financial_metrics[metric] = value

    # Extract SWOT analysis
    swot_analysis = {}
    if '==== SWOT ANALYSIS ====' in results:
        swot_section = results.split('==== SWOT ANALYSIS ====')[
            1].split('====')[0]
        current_category = None
        swot_analysis = {'Strengths': [], 'Weaknesses': [],
                         'Opportunities': [], 'Threats': []}

        for line in swot_section.split('\n'):
            line = line.strip()
            if line in ['Strengths:', 'Weaknesses:', 'Opportunities:', 'Threats:']:
                current_category = line[:-1]  # Remove colon
            elif (line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.')) and current_category:
                # Remove the bullet point, dash, or number and add to the category
                clean_line = line
                if line.startswith('-') or line.startswith('•'):
                    clean_line = line[1:].strip()
                elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                    # Remove the number and dot
                    clean_line = line[2:].strip()

                if clean_line:
                    swot_analysis[current_category].append(clean_line)

    # Extract operational signals
    operational_signals = []
    if '==== OPERATIONAL SIGNALS ====' in results:
        ops_section = results.split('==== OPERATIONAL SIGNALS ====')[
            1].split('====')[0]
        for line in ops_section.split('\n'):
            if line.strip().startswith('•') or line.strip().startswith('-'):
                operational_signals.append(line.strip())

    # Extract competitor analysis
    competitor_analysis = []
    print(f"[DEBUG] Looking for competitor analysis in results...")
    if '==== COMPETITOR ANALYSIS ====' in results:
        comp_section = results.split('==== COMPETITOR ANALYSIS ====')[
            1].split('====')[0]
        print(
            f"[DEBUG] Found competitor analysis section: {len(comp_section)} characters")
        # Include all lines from competitor analysis, not just bullet points
        for line in comp_section.split('\n'):
            if line.strip():  # Include all non-empty lines
                competitor_analysis.append(line.strip())
        print(
            f"[DEBUG] Extracted {len(competitor_analysis)} competitor analysis lines")
    elif 'COMPETITOR ANALYSIS' in results:
        # Fallback: look for any section containing competitor analysis
        sections = results.split('====')
        for section in sections:
            if 'COMPETITOR' in section.upper():
                for line in section.split('\n'):
                    if line.strip():
                        competitor_analysis.append(line.strip())
        print(
            f"[DEBUG] Found competitor analysis via fallback: {len(competitor_analysis)} lines")
    else:
        print(f"[DEBUG] No competitor analysis section found in results")
        print(
            f"[DEBUG] Available sections: {[s.strip() for s in results.split('====') if s.strip()]}")

    # Extract client intelligence
    client_intelligence = ''
    if '==== CLIENT INTELLIGENCE REPORT ====' in results:
        client_section = results.split('==== CLIENT INTELLIGENCE REPORT ====')[
            1].split('====')[0]
        client_intelligence = client_section.strip()

    # Extract product analysis
    product_analysis = ''
    if '==== PRODUCT ANALYSIS ====' in results:
        product_section = results.split('==== PRODUCT ANALYSIS ====')[
            1].split('====')[0]
        product_analysis = product_section.strip()

    # Extract key decision makers
    key_decision_makers = ''
    if '==== KEY DECISION MAKERS ====' in results:
        leadership_section = results.split('==== KEY DECISION MAKERS ====')[
            1].split('====')[0]
        key_decision_makers = leadership_section.strip()

    return {
        'financial_metrics': financial_metrics,
        'swot_analysis': swot_analysis,
        'operational_signals': operational_signals,
        'competitor_analysis': competitor_analysis,
        'client_intelligence': client_intelligence,
        'product_analysis': product_analysis,
        'key_decision_makers': key_decision_makers,
        'raw_results': results
    }


if __name__ == '__main__':
    # Run with auto-reload enabled
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
