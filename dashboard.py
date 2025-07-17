import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

import streamlit as st
import json
import os

st.set_page_config(page_title="Vendor News Dashboard", layout="wide")
st.title("📰 Vendor News Dashboard")

# Check if data file exists
if not os.path.exists("vendor_news.json"):
    st.error("❌ vendor_news.json not found. Run the fetch script first.")
    st.stop()

# Try to load JSON data
try:
    with open("vendor_news.json") as f:
        data = json.load(f)
except Exception as e:
    st.error(f"Failed to load JSON: {e}")
    st.stop()

# Extract vendor list
vendors = [entry["vendor"] for entry in data]
selected_vendor = st.selectbox("Select a vendor", vendors)

# Show articles
for vendor_data in data:
    if vendor_data["vendor"] == selected_vendor:
        articles = vendor_data.get("articles", [])
        st.subheader(f"📰 {len(articles)} Articles for {selected_vendor}")

        if not articles:
            st.info("No articles found for this vendor.")
        else:
            for article in articles:
                st.markdown(f"### {article.get('title', 'No Title')}")
                st.markdown(f"[🔗 Read Article]({article.get('link', '#')})", unsafe_allow_html=True)
                pub_date = article.get("pubDate", "Unknown date")
                st.caption(f"🕒 Published: {pub_date}")
                st.write("---")
