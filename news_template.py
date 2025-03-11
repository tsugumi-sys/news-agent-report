import streamlit as st
from chart_template import ChartFactory


class NewsReportPage:
    """Class representing a single news report page."""

    def __init__(self, date, report_data):
        self.date = date
        self.report_data = report_data

    def render(self) -> st.Page:
        """Render the news report page."""
        return create_news_report_page(self.date, self.report_data)


def impact_label(impact: str) -> str:
    if impact == "increase":
        return "📈 Increase"
    if impact == "decrease":
        return "📉 Decrease"
    return "- Neutral"


def create_news_report_page(date, report_data) -> st.Page:
    """Creates a Streamlit Page instance for the news report.

    Args:
        report_data: { 'news': {}, 'analysis': {}}
    """

    def news_page():
        """Creates a Streamlit page instance for the news report."""

        st.header(f"News Report - {date}")

        for news_data in report_data["news"]:
            news_info = news_data["knowledges"].get("news_basic_information", {})
            related_industries = news_data["knowledges"].get("related_industries", {})
            mentioned_companies = news_data["knowledges"].get("mentioned_companies", {})
            market_impact = news_data["knowledges"].get(
                "market_and_industry_impact", {}
            )
            competitive_impact = news_data["knowledges"].get(
                "competitive_landscape_impact", {}
            )
            supply_demand = news_data["knowledges"].get(
                "supply_demand_balance_change", {}
            )

            container = st.container(border=True)
            with container:
                st.subheader(news_info.get("title", "Untitled"))
                st.write(f"🕒 Published: {news_info.get('published_date', 'Unknown')}")
                st.write(f"📂 Category: {news_info.get('category', 'N/A')}")
                st.write(f"🔗 [Read More]({report_data.get('url', '#')})")

                if "industries" in related_industries:
                    st.subheader("📌 Related Industries")
                    st.write(", ".join(related_industries["industries"]))

                if "items" in mentioned_companies:
                    st.subheader("🏢 Mentioned Companies")
                    for company in mentioned_companies["items"]:
                        st.write(
                            f"- {company['name']} ({company['ticker']}, {company['exchange']})"
                        )

                if market_impact:
                    st.subheader("📉 Market & Industry Impact")
                    for impact in market_impact.get("short_term_impacts", []):
                        st.write(
                            f"- {impact['company']} ({impact['ticker']}): {impact_label(impact['impact'])}"
                        )
                        st.write(f"  *Reason*: {impact['reason']}")
                    for direction in market_impact.get("long_term_directions", []):
                        st.write(
                            f"- {direction['sector']} expected {impact_label(direction['expected_growth'])} over {direction['timeframe']}"
                        )

                if competitive_impact:
                    st.subheader("⚔️ Competitive Landscape")
                    for change in competitive_impact.get("market_share_changes", []):
                        st.write(
                            f"- {change['company']}: Market share {impact_label(change['change'])}"
                        )
                    for advantage in competitive_impact.get(
                        "technological_advantages", []
                    ):
                        st.write(f"- {advantage['company']}: {advantage['advantage']}")

                if supply_demand:
                    st.subheader("⚖️ Supply & Demand Balance")
                    for demand in supply_demand.get("demand_changes", []):
                        st.write(
                            f"- Demand for {demand['sector']}: {impact_label(demand['change'])}"
                        )
                    for supply in supply_demand.get("supply_changes", []):
                        st.write(
                            f"- Supply in {supply['sector']}: {impact_label(supply['change'])}"
                        )
                    for inventory in supply_demand.get("inventory_statuses", []):
                        st.write(
                            f"- {inventory['sector']}: {impact_label(inventory['status'])} (Price Impact: {impact_label(inventory['price_impact'])})"
                        )

    news_page.__name__ = f"news_page_{date.replace("-", "")}"
    return st.Page(news_page, title=f"News Report at {date}")
