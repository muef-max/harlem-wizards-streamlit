# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 09:32:56 2025

@author: gina-
"""
import streamlit as st
import pandas as pd
from datetime import datetime


print(st.__version__)
print(hasattr(st, "experimental_data_editor"))

import sys
print(sys.executable)


def fundraising_tab():
    st.header("Fundraising / Corporate Sponsorships")

    st.info(
        "Select an existing company to view its info, add a new company manually, "
        "or edit the full table below."
    )


    # -------------------------------
    # Full company data (all companies)
    # -------------------------------
    company_data = [
        {"Company/Organization":"Altitude Trampoline Park","Contact Name":"","Contact Title":"","MUEF Board Member":"Steve","Date Contacted":"12/10/2025","Donation Received":"","Status":"emailed","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Allen Engineering","Contact Name":"","Contact Title":"","MUEF Board Member":"Gina","Date Contacted":"12/13/2025","Donation Received":"","Status":"","Flyer Posted":"Sent note on website","Targeted Donation Level":"","Remarks":"","Email":"","Website":"https://allen-ea.com/contact/","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Asphalt Engineering","Contact Name":"Nathan","Contact Title":"President","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Aurora Exterior Painting","Contact Name":"Marc Ferlo","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"mferlo55@yahoo.com","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"BJs","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"(774) 512-6186","Street Address":"25 Research Dr.","City":"Westborough","State":"MA","Zip Code":"01581"},
        {"Company/Organization":"Cabinet Makers Hopkinton","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Century 21","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Charles River Bank","Contact Name":"Ann Sherry","Contact Title":"Senior VP/ Customer Care & Relationship Development","MUEF Board Member":"Gina and Victoria","Date Contacted":"12/5/2025","Donation Received":"","Status":"emailed","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"asherry@charlesriverbank.com","Website":"","Phone":"508-533-8661","Street Address":"70 Main St","City":"Medway","State":"MA","Zip Code":"02053"},
        {"Company/Organization":"Coffee Bean","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"Upton","State":"MA","Zip Code":"01568"},
        {"Company/Organization":"Colonial Chem Dry","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"508-529-4115","Street Address":"152 Milford St","City":"Upton","State":"MA","Zip Code":"01568"},
        {"Company/Organization":"Colonial Liquore","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"Upton","State":"MA","Zip Code":"01568"},
        {"Company/Organization":"Community Center Upton","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Core Fitness","Contact Name":"Sarah Bibeau","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"sarahcorefitness@gmail.com","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Country Sooper","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Courtyard by Marriott","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"CVS Pharmacy","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"(508) 839-2240","Street Address":"100 Worcester St","City":"Grafton","State":"MA","Zip Code":"01536"},
        {"Company/Organization":"Crown Trophy","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"https://www.crowntrophy.com/","Phone":"","Street Address":"","City":"Northborough","State":"MA","Zip Code":""},
        {"Company/Organization":"Davidson Nealley Construction","Contact Name":"Jack Nealley","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"508-529-3909","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Dean Bank","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"Vknox@Deanbank.com","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Dell EMC","Contact Name":"Linda Gazoorian, Steven Aubut","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"EMC.gives.back@emc.com","Website":"","Phone":"866-438-3622","Street Address":"176 South Street","City":"Hopkinton","State":"MA","Zip Code":"01748"},
        {"Company/Organization":"Doubletree Milford Hotel","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"12/8","Donation Received":"","Status":"emailed - steve","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Dunkin Donuts Mendon","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"(508) 482-1990","Street Address":"4 Uxbridge Rd","City":"Mendon","State":"MA","Zip Code":"01756"},
        {"Company/Organization":"Dunkin Donuts Upton","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"(508) 529-9806","Street Address":"10 Hartford Ave North","City":"Upton","State":"MA","Zip Code":"01568"},
        {"Company/Organization":"Dicks","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Family Farms","Contact Name":"","Contact Title":"","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"Upton","State":"MA","Zip Code":"01568"},
        {"Company/Organization":"Family Karate Northbridge","Contact Name":"Michelle","Contact Title":"","MUEF Board Member":"","Date Contacted":"12/11/2025","Donation Received":"yes","Status":"","Flyer Posted":"tried to contact by phone","Targeted Donation Level":"9/12/2023","Remarks":"","Email":"","Website":"","Phone":"508-234-0900","Street Address":"96 Church St","City":"Whitinsville","State":"MA","Zip Code":""},
        {"Company/Organization":"Fitts Insurance Agency","Contact Name":"Chris Fitts","Contact Title":"President","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"508-620-6200","Street Address":"2 Willow Street, Suite 102","City":"Southborough","State":"MA","Zip Code":"01745"},
        {"Company/Organization":"Grafton Upton Railroad","Contact Name":"Delli Priscoli","Contact Title":"Owner & CEO","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"info@graftonuptonrr.com","Website":"","Phone":"508-839-1701","Street Address":"929 Boston Post Road East","City":"Marlborough","State":"MA","Zip Code":"01752"},
        {"Company/Organization":"Great Stories","Contact Name":"Chris Mills","Contact Title":"Owner","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Greenhouse Woodfired Pub","Contact Name":"John McCarthy","Contact Title":"Owner","MUEF Board Member":"","Date Contacted":"","Donation Received":"","Status":"","Flyer Posted":"","Targeted Donation Level":"","Remarks":"","Email":"","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        {"Company/Organization":"Hilton","Contact Name":"Robert Loewen","Contact Title":"","MUEF Board Member":"Gina","Date Contacted":"12/13/2026","Donation Received":"","Status":"","Flyer Posted":"emailed","Targeted Donation Level":"","Remarks":"","Email":"Robert.Loewen@hilton.com","Website":"","Phone":"","Street Address":"","City":"","State":"","Zip Code":""},
        # ... continue for remaining companies exactly in this pattern
    ]

    df = pd.DataFrame(company_data)
    
    # -------------------------------
    # Dropdown to select company or add new
    # -------------------------------
    company_list = sorted(df["Company/Organization"].dropna().unique().tolist())
    selected_company = st.selectbox(
        "Company / Organization",
        ["Add New Company"] + company_list
    )

    # -------------------------------
    # If user selects an existing company
    # -------------------------------
    if selected_company != "Add New Company":
        filtered = df[df["Company/Organization"] == selected_company]
        if not filtered.empty:
            row = filtered.iloc[0]
            st.subheader(f"ℹ️ Details for {selected_company}")
            for col in df.columns:
                st.write(f"**{col}:** {row[col]}")
        else:
            st.warning(f"No data found for {selected_company}.")

    # -------------------------------
    # If user selects "Add New Company"
    # -------------------------------
    else:
        st.subheader("✏️ Add New Company")
        with st.form("add_new_company"):
            new_company = st.text_input("Company/Organization")
            contact_name = st.text_input("Contact Name")
            contact_title = st.text_input("Contact Title")
            board_member = st.text_input("MUEF Board Member")
            date_contacted = st.date_input("Date Contacted", datetime.today())
            donation_received = st.text_input("Donation Received")
            status = st.selectbox("Status", ["Pending", "Contacted", "Confirmed", "Declined"])
            flyer_posted = st.checkbox("Flyer Posted?")
            targeted_level = st.text_input("Targeted Donation Level")
            remarks = st.text_input("Remarks")
            email = st.text_input("Email")
            website = st.text_input("Website")
            phone = st.text_input("Phone")
            street = st.text_input("Street Address")
            city = st.text_input("City")
            state = st.text_input("State")
            zip_code = st.text_input("Zip Code")

            submitted = st.form_submit_button("💾 Add Company")
            if submitted:
                new_row = {
                    "Company/Organization": new_company,
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
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✅ Added {new_company}!")

    # -------------------------------
    # Editable table of all companies
    # -------------------------------
    st.subheader("📊 All Companies (Editable)")
    edited_df = st.experimental_data_editor(df, num_rows="dynamic")
    df = edited_df

    # -------------------------------
    # Download CSV
    # -------------------------------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download as CSV",
        csv,
        "sponsorships.csv",
        "text/csv"
    )
#
