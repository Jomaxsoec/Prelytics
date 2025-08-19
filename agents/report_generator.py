import os
import json

def generate(data, company_name):
    os.makedirs("outputs/client_briefs", exist_ok=True)
    os.makedirs("outputs/competitor_reports", exist_ok=True)

    with open(f"outputs/client_briefs/{company_name}_brief.json", "w") as f:
        json.dump(data['client_profile'], f, indent=2)

    with open(f"outputs/competitor_reports/{company_name}_competitors.json", "w") as f:
        json.dump(data['competitors'], f, indent=2)

    print("[ReportGenerator] Reports generated successfully!")