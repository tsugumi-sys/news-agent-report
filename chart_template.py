from collections import defaultdict
import streamlit as st
from abc import ABC, abstractmethod
import pandas as pd
from enum import StrEnum, auto


class ChartContainer(ABC):
    """Abstract class for chart containers."""

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def render(self):
        """Render method must be implemented by subclasses."""
        pass

    @abstractmethod
    def analyze(self) -> pd.DataFrame:
        pass


class NewsCategoryCount(ChartContainer):
    def render(self):
        df = self.analyze()
        container = st.container(border=True)
        container.subheader("ニュースの種類")
        # TODO: create pandas dataframe of name and count, then render with dataframe.
        df.sort_values(by="count", ascending=False, inplace=True)
        container.bar_chart(df, x="category", y=["count"], color=["#FF4D00"])
        container.dataframe(df, hide_index=True)

    def analyze(self) -> pd.DataFrame:
        category_counts = defaultdict(int)
        for news in self.data:
            category = news["knowledges"]["news_basic_information"].get(
                "category", "N/A"
            )
            category_counts[category] += 1
        data = {"category": category_counts.keys(), "count": category_counts.values()}
        return pd.DataFrame(data)


class ShortTermMarketImpact(ChartContainer):
    def render(self):
        data = self.analyze()
        container = st.container(border=True)
        container.subheader("📊 短期的な株価の変動予想")
        container.text(
            "ニュースによって上昇・下落の予想が揺れる。割合をみて判断するのが良さそうだ。"
        )
        data.sort_values(by="increase", ascending=False, inplace=True)
        container.bar_chart(
            data,
            x="ticker",
            y=["increase", "decrease"],
            stack=True,
            color=["#FF0000", "#0000FF"],
        )
        container.dataframe(data, hide_index=True)

    def analyze(self) -> pd.DataFrame:
        impacts = defaultdict(lambda: defaultdict(int))
        for news in self.data:
            shortterm_impacts = news["knowledges"]["market_and_industry_impact"].get(
                "short_term_impacts", []
            )
            for d in shortterm_impacts:
                impacts[d["ticker"]][d["impact"]] += 1
        data = {
            "ticker": impacts.keys(),
            "increase": [d["increase"] for d in impacts.values()],
            "decrease": [d["decrease"] for d in impacts.values()],
        }
        return pd.DataFrame(data)


class LongTermMarketImpact(ChartContainer):
    def render(self):
        data = self.analyze()
        container = st.container(border=True)
        container.subheader("📊 中長期の業界変動予想")
        container.text(
            "ニュースによって上昇・下落の予想が揺れる。割合をみて判断するのが良さそうだ。"
        )
        data.sort_values(by="expansion", ascending=False, inplace=True)
        container.bar_chart(
            data,
            x="sector",
            y=["expansion", "contraction"],
            stack=True,
            color=["#FF0000", "#0000FF"],
        )
        container.dataframe(data, hide_index=True)

    def analyze(self) -> pd.DataFrame:
        impacts = defaultdict(lambda: defaultdict(int))
        for news in self.data:
            shortterm_impacts = news["knowledges"]["market_and_industry_impact"].get(
                "long_term_directions", []
            )
            for d in shortterm_impacts:
                if d["timeframe"] in ["years", "months", "weeks", "days"]:
                    impacts[d["sector"]][d["expected_growth"]] += 1
        data = {
            "sector": impacts.keys(),
            "expansion": [d["expansion"] for d in impacts.values()],
            "contraction": [d["contraction"] for d in impacts.values()],
        }
        return pd.DataFrame(data)


class IndustriesPositiveNegativeChart(ChartContainer):
    def render(self):
        container = st.container(border=True)
        container.subheader("🏭 業界ごとの影響度")
        data = {
            "industry": self.data.keys(),
            "positive": [item["positive"] for item in self.data.values()],
            "negative": [item["negative"] for item in self.data.values()],
            "neutral": [item["neutral"] for item in self.data.values()],
        }
        df = pd.DataFrame(data)
        df.sort_values(by="positive", ascending=False, inplace=True)
        container.bar_chart(
            data,
            x="industry",
            y=["positive", "negative"],
            stack=True,
            color=["#FF0000", "#0000FF"],
        )
        container.dataframe(df, hide_index=True)


class CompaniesPositiveNegativeChart(ChartContainer):
    def render(self):
        container = st.container(border=True)
        container.subheader("🏢 企業の影響度")

        data = {
            "company": self.data.keys(),
            "positive": [item["positive"] for item in self.data.values()],
            "negative": [item["negative"] for item in self.data.values()],
            "neutral": [item["neutral"] for item in self.data.values()],
        }
        df = pd.DataFrame(data)
        df.sort_values(by="positive", ascending=False, inplace=True)
        container.bar_chart(
            data,
            x="company",
            y=["positive", "negative"],
            stack=True,
            color=["#FF0000", "#0000FF"],
        )
        container.dataframe(df, hide_index=True)


class AnalysisName(StrEnum):
    countries_positive_negative = auto()
    industries_positive_negative = auto()
    companies_positive_negative = auto()
    news_category_count = auto()
    short_term_market_impacts = auto()
    long_term_market_impacts = auto()


class ChartFactory:
    """Factory class for creating chart containers based on data keys."""

    @staticmethod
    def create_chart(key, data):
        chart_classes = {
            AnalysisName.industries_positive_negative: IndustriesPositiveNegativeChart,
            AnalysisName.companies_positive_negative: CompaniesPositiveNegativeChart,
            AnalysisName.news_category_count: NewsCategoryCount,
            AnalysisName.short_term_market_impacts: ShortTermMarketImpact,
            AnalysisName.long_term_market_impacts: LongTermMarketImpact,
        }
        if key in chart_classes:
            return chart_classes[key](data)
        raise ValueError(f"Unknown chart key: {key}")
