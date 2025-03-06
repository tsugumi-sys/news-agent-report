from collections import defaultdict
import streamlit as st
import json
from news_template import news_container

# Load JSON data

dates = ["2025-03-06"]
report_data = defaultdict(dict)
for date in dates:
    with open("report_data/2025-03-06/raw.json", "r", encoding="utf-8") as f:
        report_raw_data = json.load(f)
    report_data[date]["raw"] = report_raw_data

report_pages = {}
for date, data in report_data.items():
    report_pages[date] = lambda: news_container(data["raw"])

st.title("News Impact Analysis")

navigations = []

for title, page_func in report_pages.items():
    navigations.append(st.Page(page_func, title=title, icon=":material/favorite:"))

pg = st.navigation(navigations)
pg.run()
