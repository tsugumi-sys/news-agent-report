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
        return "📈"
    if impact == "decrease":
        return "📉"
    return "-"


def create_news_report_page(date, report_data) -> st.Page:
    """Creates a Streamlit Page instance for the news report.

    Args:
        report_data: { 'news': {}, 'analysis': {}}
    """

    def news_page():
        """Creates a Streamlit page instance for the news report."""

        st.header(f"News Report - {date}")

        st.markdown("""
### 分析内容

1. **ニュースの分類:** 需要・供給・競争環境・政策のどれか
2. **影響を受ける企業:** ポジティブ or ネガティブな企業を特定
3. **短期・中長期の影響:** 需給変化、市場動向、技術革新の影響
4. **判断:** 投資・事業戦略の方向性を決める
                    """)

        st.markdown("## News")
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
                st.write(f"🔗 [Read More]({news_data.get('url', '#')})")

                st.markdown("**ニュースの種類**")
                st.text(
                    f"{news_info.get('category', 'N/A')}  (需要・供給・競争環境・政策のどれか)"
                )

                if market_impact:
                    ###
                    # 影響を受ける企業 (短期の株価上昇下落)
                    ###
                    st.markdown("----")
                    st.markdown("### 影響を受ける企業")
                    st.markdown("**短期で影響を受ける企業**")
                    up_companies = []
                    down_companies = []
                    for impact in market_impact.get("short_term_impacts", []):
                        if impact["impact"] == "increase":
                            up_companies.append(impact)
                        else:
                            down_companies.append(impact)
                    if len(up_companies) > 0:
                        st.markdown(
                            f"{impact_label('increase')} 短期的に株価が上昇すると予想される企業:"
                        )
                        for company in up_companies:
                            st.write(
                                f"- {company['company']} (Ticker: {company['ticker']}): {company['reason']}"
                            )

                    if len(down_companies) > 0:
                        st.markdown(
                            f"{impact_label('decrease')} 短期的に株価が下落すると予想される企業:"
                        )
                        for company in down_companies:
                            st.write(
                                f"- {company['company']} (Ticker: {company['ticker']}): {company['reason']}"
                            )

                    ###
                    # 中長期で影響を受ける企業・業界
                    ###
                    st.markdown("**中長期で影響を受ける企業・業界**")
                    for sector in market_impact.get("long_term_directions", []):
                        st.write(
                            f"- {sector["sector"]} (時間軸: {sector["timeframe"]}): {impact_label('increase') if sector["expected_growth"] == "expansion" else impact_label('decrease')}"
                        )

                if competitive_impact:
                    ###
                    # 競争環境の変化
                    ###
                    st.markdown("----")
                    st.markdown("### ⚔️ 競争環境の変化")
                    # 市場シェアの変化
                    st.markdown("**市場シェアの変化**")
                    for change in competitive_impact.get("market_share_changes", []):
                        st.write(
                            f"- {change['company']}のシェア: {impact_label(change['change'])}"
                        )

                    # 技術的優位性の変化
                    st.markdown("**技術的優位性の変化**")
                    for advantage in competitive_impact.get(
                        "technological_advantages", []
                    ):
                        st.write(f"- {advantage['company']}: {advantage['advantage']}")

                    # 技術的優位性の変化
                    st.markdown("**業界の寡占化・新規参入**")
                    industry_structure_changes = competitive_impact.get(
                        "industry_structure_changes"
                    )
                    if industry_structure_changes:
                        if industry_structure_changes["change_type"] == "entry":
                            st.write(
                                f"- 新規参入: {industry_structure_changes ["affected_companies"]}"
                            )
                        elif industry_structure_changes["change_type"] == "oligopoly":
                            st.write(
                                f"- 既存企業の寡占状態変化: {industry_structure_changes ["affected_companies"]}"
                            )
                        elif industry_structure_changes["change_type"] == "contraction":
                            st.write(
                                f"- 縮小: {industry_structure_changes ["affected_companies"]}"
                            )

                        else:
                            raise ValueError(
                                f"unsupported change type: {industry_structure_changes ["change_type"]}"
                            )

                ###
                # 需給バランスの変化
                ###
                if supply_demand:
                    st.markdown("----")
                    st.markdown("### ⚖️ 需給バランスの変化")
                    for demand in supply_demand.get("demand_changes", []):
                        st.write(
                            f"- {demand['sector']}の需要: {impact_label(demand['change'])}"
                        )
                    for supply in supply_demand.get("supply_changes", []):
                        st.write(
                            f"- {supply['sector']}の供給: {impact_label(supply['change'])}"
                        )
                    for inventory in supply_demand.get("inventory_statuses", []):
                        if inventory["status"] == "surplus":
                            st.write(
                                f"- {inventory['sector']}の在庫が余剰になる: (価格への影響: {impact_label(inventory['price_impact'])})"
                            )
                        # TODO: 表記揺れを直す。
                        elif (
                            inventory["status"] == "shortage"
                            or inventory["status"] == "不足"
                        ):
                            st.write(
                                f"- {inventory['sector']}の在庫が不足する: (価格への影響: {impact_label(inventory['price_impact'])})"
                            )
                        else:
                            raise ValueError(
                                f"unsupported inventory status: {inventory["status"]}"
                            )

                ###
                # 関連業界
                ###
                if "industries" in related_industries:
                    st.markdown("----")
                    st.markdown("関連業界")
                    st.write(", ".join(related_industries["industries"]))

                ###
                # ニュースに含まれる企業
                ###
                if "items" in mentioned_companies:
                    st.markdown("ニュースに含まれる企業")
                    for company in mentioned_companies["items"]:
                        st.write(
                            f"- {company['name']} ({company['ticker']}, {company['exchange']})"
                        )

    news_page.__name__ = f"news_page_{date.replace("-", "")}"
    return st.Page(news_page, title=f"News Report at {date}")
