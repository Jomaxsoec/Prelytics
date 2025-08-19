from agents import client_intelligence
from agents import financial_insight
from agents import operational_signal
from agents import competitor_analysis
from agents import product_analysis


class CoordinatorAgent:
    def __init__(self, name, url):
        print(f"[DEBUG] CoordinatorAgent initialized with {name}, {url}")
        self.name = name
        self.url = url

    def run_workflow(self):
        print(
            f"\n[CoordinatorAgent] Starting intelligence generation for: {self.name}")

        # 1. Client Intelligence
        print(
            f"[CoordinatorAgent] Step 1: Running client intelligence for {self.name}")
        client_data = client_intelligence.extract_profile(self.name, self.url)
        print(
            f"[CoordinatorAgent] Client intelligence result length: {len(str(client_data)) if client_data else 0}")

        # 2. Financial Insight (Tabular + SWOT + CAGR)
        print(
            f"[CoordinatorAgent] Step 2: Running financial analysis for {self.name}")
        financial_data = financial_insight.analyze_financials(self.name)
        print(
            f"[CoordinatorAgent] Financial data result length: {len(str(financial_data)) if financial_data else 0}")

        # 3. Operational Signals
        print(
            f"[CoordinatorAgent] Step 3: Running operational signals for {self.name}")
        ops_data = operational_signal.extract_operational_signals(
            self.name, self.url)
        print(
            f"[CoordinatorAgent] Operational signals result length: {len(str(ops_data)) if ops_data else 0}")

        # 4. Competitor Analysis
        print(
            f"[CoordinatorAgent] Step 4: Running competitor analysis for {self.name}")
        competitor_report = competitor_analysis.extract_competitor_analysis(
            self.name)
        print(
            f"[CoordinatorAgent] Competitor analysis result length: {len(str(competitor_report)) if competitor_report else 0}")

        # 5. Product Analysis
        print(
            f"[CoordinatorAgent] Step 6: Running product analysis for {self.name}")
        product_report = product_analysis.analyze_client(self.name, self.url)
        print(
            f"[CoordinatorAgent] Product analysis result length: {len(str(product_report)) if product_report else 0}")

        # 6. Final Report Sections
        report = []
        report.append("==== CLIENT INTELLIGENCE REPORT ====")
        report.append(client_data or "[No client intelligence available]")

        report.append("\n==== FINANCIAL INSIGHTS ====")
        report.append(financial_data or "[No financial data found]")

        report.append("\n==== OPERATIONAL SIGNALS ====")
        report.append(ops_data or "[No operational signals found]")

        report.append("\n==== COMPETITOR ANALYSIS ====")
        report.append(competitor_report or "[No competitor report found]")

        report.append("\n==== PRODUCT ANALYSIS ====")
        report.append(product_report or "[No product analysis found]")

        # 7. Combine and display report
        final_report = "\n".join(report)

        print("\n" + "=" * 80)
        print("               PRELYTICS BUSINESS INTELLIGENCE REPORT")
        print("=" * 80)
        print(final_report)
        print("=" * 80)
        print("[SUCCESS] Report generation complete")

        return final_report
