import streamlit as st
from news_template import create_news_report_page
from data_loader import DataLoader


class NewsReportPage:
    """Class representing a single news report page."""

    def __init__(self, date, report_data):
        self.date = date
        self.report_data = report_data

    def render(self) -> st.Page:
        """Render the news report page."""
        return create_news_report_page(self.date, self.report_data)


class SummaryPage:
    """Class representing the summary of all news reports."""

    def __init__(self, report_pages: list[st.Page]):
        self.report_pages = report_pages

    def render(self) -> st.Page:
        """Render the summary page listing all report pages."""

        def page():
            st.header("All Reports")
            for report_key in sorted(self.report_pages.keys()):
                st.page_link(self.report_pages[report_key])

        return st.Page(page, title="Summary", default=True)


# Initialize DataLoader and PageManager
report_data_dir = "./report_data"
data_loader = DataLoader(report_data_dir)
report_data = data_loader.load_data()

report_pages = {}
for date, data in report_data.items():
    news_page = NewsReportPage(date, data)
    report_pages[date] = news_page.render()

summary_page = SummaryPage(report_pages)
navigations = [summary_page.render()]
for page in report_pages.values():
    navigations.append(page)

pg = st.navigation(navigations)

pg.run()
