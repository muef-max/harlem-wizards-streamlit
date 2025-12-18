# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 09:32:56 2025

@author: gina-
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json

# -------------------------------
# Load Google credentials ONCE
# -------------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=SCOPES
)

gc = gspread.authorize(creds)

st.write("Service account email:", creds.service_account_email)



# # Try opening the sheet
# SPREADSHEET_NAME = "MUEF Corporate Sponsors Target List 2025"
# try:
#     sh = gc.open(SPREADSHEET_NAME)
#     print("✅ Sheet opened successfully!")
# except Exception as e:
#     print("❌ Failed to open sheet:", e)


st.write("Testing secrets...")

try:
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    st.success("✅ GOOGLE_CREDENTIALS loaded successfully!")
except KeyError:
    st.error("❌ GOOGLE_CREDENTIALS not found in secrets.toml")
except json.JSONDecodeError as e:
    st.error(f"❌ JSON decode error: {e}")


def fundraising_tab():
    st.header("Fundraising / Corporate Sponsorships")

    st.info(
        "Select an existing company from the dropdown to edit it, "
        "or leave it blank to add a new sponsor."
    )
    SPREADSHEET_ID = "1JPS25edzt5Vyi27vVU3-FNmVtmFq1NpI"  # <-- your real ID

    try:
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet("Sponsor_target")
        st.success("✅ Google Sheet connected")
    except Exception as e:
        st.exception(e)
        st.stop()

    # -------------------------------
    # Google Sheets Authentication
    # -------------------------------

    SPREADSHEET_NAME = "MUEF Corporate Sponsors Target List 2025"

    try:
        sh = gc.open(SPREADSHEET_NAME)
        worksheet = sh.worksheet("Sponsor_target")
    except Exception as e:
        st.error("❌ Unable to open Google Sheet. Check name and permissions.")
        st.stop()

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        df = pd.DataFrame(columns=[
            "Company/Organization","Contact Name","Contact Title","MUEF Board Member",
            "Date Contacted","Donation Received","Status","Flyer Posted",
            "Targeted Donation Level","Remarks","Email","Website",
            "Phone","Street Address","City","State","Zip Code"
        ])

    # -------------------------------
    # COMPANY DROPDOWN  ✅ THIS IS THE MISSING PIECE
    # -------------------------------
    st.subheader("🎯 Select Company")

    company_list = sorted(df["Company/Organization"].dropna().unique().tolist())

    selected_company = st.selectbox(
        "Company / Organization",
        [""] + company_list,
        help="Choose an existing sponsor to auto-fill the form"
    )

    if selected_company:
        row = df[df["Company/Organization"] == selected_company].iloc[0]
    else:
        row = pd.Series({col: "" for col in df.columns})

    st.divider()

    # -------------------------------
    # EDIT FORM
    # -------------------------------
    with st.expander("✏️ Add / Edit Sponsor", expanded=True):
        c1 = st.columns(4)
        company = c1[0].text_input("Company/Organization", row["Company/Organization"])
        contact_name = c1[1].text_input("Contact Name", row["Contact Name"])
        contact_title = c1[2].text_input("Contact Title", row["Contact Title"])
        board_member = c1[3].text_input("MUEF Board Member", row["MUEF Board Member"])

        c2 = st.columns(4)
        date_contacted = c2[0].date_input(
            "Date Contacted",
            pd.to_datetime(row["Date Contacted"], errors="coerce")
            if row["Date Contacted"] else None
        )
        donation_received = c2[1].text_input("Donation Received", row["Donation Received"])
        status = c2[2].selectbox(
            "Status",
            ["Pending", "Contacted", "Confirmed", "Declined"],
            index=["Pending","Contacted","Confirmed","Declined"].index(row["Status"])
            if row["Status"] in ["Pending","Contacted","Confirmed","Declined"] else 0
        )
        flyer_posted = c2[3].checkbox("Flyer Posted?", bool(row["Flyer Posted"]))

        c3 = st.columns(4)
        targeted_level = c3[0].text_input("Targeted Donation Level", row["Targeted Donation Level"])
        remarks = c3[1].text_input("Remarks", row["Remarks"])
        email = c3[2].text_input("Email", row["Email"])
        website = c3[3].text_input("Website", row["Website"])

        c4 = st.columns(4)
        phone = c4[0].text_input("Phone", row["Phone"])
        street = c4[1].text_input("Street Address", row["Street Address"])
        city = c4[2].text_input("City", row["City"])
        state = c4[3].text_input("State", row["State"])
        zip_code = st.text_input("Zip Code", row["Zip Code"])

        if st.button("💾 Save Sponsor"):
            new_row = {
                "Company/Organization": company,
                "Contact Name": contact_name,
                "Contact Title": contact_title,
                "MUEF Board Member": board_member,
                "Date Contacted": date_contacted.strftime("%Y-%m-%d") if date_contacted else "",
                "Donation Received": donation_received,
                "Status": status,
                "Flyer Posted": flyer_posted,
                "Targeted Donation Level": targeted_level,
                "Remarks": remarks,
                "Email": email,
                "Website": website,
                "Phone": phone,
                "Street Address": street,
                "City": city,
                "State": state,
                "Zip Code": zip_code
            }

            if selected_company:
                idx = df[df["Company/Organization"] == selected_company].index[0]
                for col in df.columns:
                    df.at[idx, col] = new_row[col]
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            worksheet.update([df.columns.tolist()] + df.values.tolist())
            st.success("✅ Sponsor saved to Google Sheet!")

    # -------------------------------
    # VIEW FULL SHEET
    # -------------------------------
    st.subheader("📊 Current Sponsorships (Live Google Sheet)")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download as CSV",
        csv,
        "sponsorships.csv",
        "text/csv"
    )
