import streamlit as st
import pandas as pd
from scraper import scrape_google_maps
from enrichment import enrich_leads

# Streamlit page config
st.set_page_config(page_title="LeadGen Tool", page_icon="🔍", layout="wide")

# Header section
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🔍 Lead Generation Tool</h1>
    <h3 style='text-align: center;'>Find, enrich, and export high-impact leads for your business 🚀</h3>
    <hr style='border: 1px solid #eee;'>
    """,
    unsafe_allow_html=True
)

# Sidebar configuration
st.sidebar.header("🔧 Configuration")
business_type = st.sidebar.text_input("Business Type", "Marketing Agency")
location = st.sidebar.text_input("Location (City, Country)", "New York, USA")
num_results = st.sidebar.slider("Number of Results", 10, 100, 20, step=10)

# Enrichment option in sidebar
enrich_now = st.sidebar.checkbox("⚡ Run Enrichment (Emails / Socials)?")

# Main button to run
if st.button("✨ Generate Leads"):
    with st.spinner("Scraping Google Maps..."):
        leads_df = scrape_google_maps(business_type, location, num_results)
        st.success(f"✅ Scraped {len(leads_df)} leads!")

        # If user opted for enrichment
        if enrich_now:
            with st.spinner("Enriching leads..."):
                leads_df = enrich_leads(leads_df)
                st.success("✅ Enrichment completed!")

    # Show results
    st.markdown("### 📄 Lead Results")
    st.dataframe(leads_df)

    # CSV export button
    csv = leads_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="leads.csv",
        mime="text/csv"
    )
