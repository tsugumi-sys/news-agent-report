import json
import streamlit as st
from abc import ABC, abstractmethod


class ChartContainer(ABC):
    """Abstract class for chart containers."""

    def __init__(self, **data):
        self.data = data

    @abstractmethod
    def render(self):
        """Render method must be implemented by subclasses."""
        pass


class CompanyNamesChart(ChartContainer):
    def render(self):
        st.title("Company Names Chart")
        st.write(self.data)
        # Add custom Streamlit rendering logic here


class CountriesPositiveNegativeChart(ChartContainer):
    def render(self):
        st.title("Countries Positive/Negative Chart")
        st.write(self.data)
        # Add custom Streamlit rendering logic here


class IndustriesPositiveNegativeChart(ChartContainer):
    def render(self):
        st.title("Industries Positive/Negative Chart")
        st.write(self.data)
        # Add custom Streamlit rendering logic here


class CompaniesPositiveNegativeChart(ChartContainer):
    def render(self):
        st.title("Companies Positive/Negative Chart")
        st.write(self.data)
        # Add custom Streamlit rendering logic here


class ChartFactory:
    """Factory class for creating chart containers based on data keys."""

    @staticmethod
    def create_chart(key, data):
        chart_classes = {
            "company_names": CompanyNamesChart,
            "countries_positive_negative": CountriesPositiveNegativeChart,
            "industries_positive_negative": IndustriesPositiveNegativeChart,
            "companies_positive_negative": CompaniesPositiveNegativeChart,
        }
        if key in chart_classes:
            return chart_classes[key](**data)
        raise ValueError(f"Unknown chart key: {key}")


# Example usage
if __name__ == "__main__":
    # Load data
    with open("report_data/2025-03-06/analyzed.json", "r", encoding="utf-8") as f:
        analyzed_data = json.load(f)

    # Initialize Streamlit app
    st.title("Charts Dashboard")

    # Create and render charts
    for key, data in analyzed_data.items():
        chart = ChartFactory.create_chart(key, {key: data})
        chart.render()
