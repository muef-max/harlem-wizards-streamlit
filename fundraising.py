import streamlit as st

def fundraising_tab():
    st.header("Fundraising / Corporate Sponsorships")

    st.info(
        "Fundraising and sponsorship tracking is now managed offline in Google Sheets. "
        "Please use the link below to view or update the data."
    )

    # Button to open Google Sheet
    google_sheet_url = "https://docs.google.com/spreadsheets/d/1hkzFKL4yqSQcS9vV6BVHKHPsfKj3ziVD/edit?gid=799937764#gid=799937764"
    if st.button("📄 Open Fundraising Sheet"):
        st.markdown(f"[Click here to open the Google Sheet]({google_sheet_url})", unsafe_allow_html=True)

    st.warning(
        "⚠️ Please update the fundraising information directly in the Google Sheet. "
        "This app does not manage fundraising data anymore."
    )

