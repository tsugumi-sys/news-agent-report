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


def impact_label(impact: int) -> str:
    if impact > 0:
        return "🟢 Positive"
    if impact < 0:
        return "🔴 Negative"
    return "- Neutral"


def create_news_report_page(date, report_data) -> st.Page:
    """Creates a Streamlit Page instance for the news report.

    Args:
        report_data: { 'news': {}, 'analysis': {}}
    """

    def news_page():
        st.header(f"Report at {date}")

        analysis_data = report_data["analysis"]
        for key, data in analysis_data.items():
            chart = ChartFactory.create_chart(key, data)
            chart.render()

        st.subheader("News List")
        news_data = report_data["news"]
        for item in news_data:
            container = st.container(border=True)
            news_info = item["knowledges"]["news_basic_information"]
            supply_demand = item["knowledges"]["supply_and_demand_balance"]
            countries_impact = item["knowledges"]["countries_positive_negative"][
                "items"
            ]
            industries_impact = item["knowledges"]["industries_positive_negative"][
                "items"
            ]
            companies_impact = item["knowledges"]["companies_positive_negative"][
                "items"
            ]

            container.subheader(news_info["title"])
            container.markdown(f"🔗 [Read More]({item['url']})")
            if news_info["importance"]:
                container.markdown(f"重要度: {news_info["importance"]}")
                container.markdown(
                    "(投資判断においてどれくらい重要な情報を含んでいるかしめす。Max 5, Min 0.)"
                )
            container.write(f"🕒 Published: {news_info['published_date']}")

            impact_sections = [
                ("🌍 Countries", countries_impact),
                ("🏭 Industries", industries_impact),
                ("🏢 Companies", companies_impact),
            ]

            for title, impacts in impact_sections:
                if impacts:
                    container.markdown(f"### {title}に対するインパクト")
                    for impact in impacts:
                        impact_value = impact["impact"]
                        container.markdown(
                            f"**{impact['target']} にとって {impact_label(impact_value)} ({impact_value})**"
                        )
                        container.write(f"**理由:** {impact['reason']}")
                        container.markdown("---")

            container.markdown("### ⚖️ Supply & Demand")
            container.write(f"**供給:** {supply_demand['supply_resource']}")
            container.write(f"**需要:** {supply_demand['demand_resource']}")
            container.write(supply_demand["balance_description"])
            container.markdown("---")

    news_page.__name__ = f"news_page_{date.replace("-", "")}"
    return st.Page(news_page, title=f"News Report at {date}")
