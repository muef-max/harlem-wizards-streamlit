# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 09:43:36 2025

@author: gina-
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# -------------------------------
# Load service account credentials
# -------------------------------
try:
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
except KeyError:
    st.error("❌ GOOGLE_CREDENTIALS not found in secrets.toml")
    st.stop()
except json.JSONDecodeError as e:
    st.error(f"❌ JSON decode error: {e}")
    st.stop()

creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)

gc = gspread.authorize(creds)
st.success(f"Service account: {creds.service_account_email}")

# -------------------------------
# Use the new personal spreadsheet ID
# -------------------------------
SPREADSHEET_ID = "19g20uQl-Gdn8ixa_degyyrfSZcLloB5D"

try:
    sh = gc.open_by_key(SPREADSHEET_ID)
    st.success(f"✅ Connected to spreadsheet: {sh.title}")
    st.write("Available worksheets:", [ws.title for ws in sh.worksheets()])
except gspread.exceptions.APIError as e:
    st.error(f"❌ APIError: {e}")
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
