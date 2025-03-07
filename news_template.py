import streamlit as st


class NewsReportPage:
    """Class representing a single news report page."""

    def __init__(self, date, report_data):
        self.date = date
        self.report_data = report_data

    def render(self) -> st.Page:
        """Render the news report page."""
        return create_news_report_page(self.date, self.report_data)


def create_news_report_page(date, report_data) -> st.Page:
    """Creates a Streamlit Page instance for the news report."""

    def news_page():
        st.title(f"Report at {date}")
        # render news data
        for item in report_data["news"]:
            container = st.container()
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
                        impact_label = (
                            "🟢 Positive" if impact_value > 0 else "🔴 Negative"
                        )
                        container.markdown(
                            f"**{impact['target']} にとって {impact_label} ({impact_value})**"
                        )
                        container.write(f"**理由:** {impact['reason']}")
                        container.markdown("---")

            container.markdown("### ⚖️ Supply & Demand")
            container.write(f"**供給:** {supply_demand['supply_resource']}")
            container.write(f"**需要:** {supply_demand['demand_resource']}")
            container.write(supply_demand["balance_description"])
            container.markdown("---")

    return st.Page(news_page, title=f"News Report at {date}")
