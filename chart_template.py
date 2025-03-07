import streamlit as st
from abc import ABC, abstractmethod
import pandas as pd
from enum import StrEnum, auto


class ChartContainer(ABC):
    """Abstract class for chart containers."""

    def __init__(self, **data):
        self.data = data

    @abstractmethod
    def render(self):
        """Render method must be implemented by subclasses."""
        pass


class CompanyNamesChart(ChartContainer):
    # data: dict[str, int]
    # e.g)
    # {
    #   company_a: 1,
    #   company_b: 2
    # }
    def render(self):
        container = st.container(border=True)
        container.subheader("🏢 企業の言及回数")
        # TODO: create pandas dataframe of name and count, then render with dataframe.
        data = {"company_name": self.data.keys(), "mention_count": self.data.values()}
        df = pd.DataFrame(data)
        df.sort_values(by="mention_count", ascending=False, inplace=True)
        container.bar_chart(
            data,
            x="company_name",
            y=["mention_count"],
        )
        container.dataframe(df, hide_index=True)


class CountriesPositiveNegativeChart(ChartContainer):
    def render(self):
        container = st.container(border=True)
        container.subheader("📊 国ごとの影響度")


class IndustriesPositiveNegativeChart(ChartContainer):
    def render(self):
        container = st.container(border=True)
        container.subheader("🏭 業界ごとの影響度")


class CompaniesPositiveNegativeChart(ChartContainer):
    def render(self):
        container = st.container(border=True)
        container.subheader("🏢 企業の影響度")


class AnalysisName(StrEnum):
    company_names = auto()
    countries_positive_negative = auto()
    industries_positive_negative = auto()
    companies_positive_negative = auto()


class ChartFactory:
    """Factory class for creating chart containers based on data keys."""

    @staticmethod
    def create_chart(key, data):
        chart_classes = {
            AnalysisName.company_names: CompanyNamesChart,
            AnalysisName.countries_positive_negative: CountriesPositiveNegativeChart,
            AnalysisName.industries_positive_negative: IndustriesPositiveNegativeChart,
            AnalysisName.companies_positive_negative: CompaniesPositiveNegativeChart,
        }
        if key in chart_classes:
            return chart_classes[key](**data)
        raise ValueError(f"Unknown chart key: {key}")
