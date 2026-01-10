# %%
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 09:17:28 2025

@author: gina-
"""
"""
Created on Sun Dec 14 09:17:28 2025
@author: gina-
"""

import streamlit as st
import json
import pandas as pd
import gspread

from google.oauth2.service_account import Credentials
from fundraising import fundraising_tab

# 2️⃣ GOOGLE SHEET CONNECTION (RIGHT AFTER IMPORTS)

@st.cache_resource
def get_gsheet():
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        creds_dict,
        scopes=scopes
    )

    gc = gspread.authorize(credentials)

    return gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("tasks")

sheet = get_gsheet()

# 3️⃣ HELPER FUNCTIONS (IMMEDIATELY AFTER)

def load_tasks(sheet, section):
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    return df[df["section"] == section]


def update_task(sheet, section, task_id, done, completed_date):
    records = sheet.get_all_records()
    df = pd.DataFrame(records)

    row = df[
        (df["section"] == section) & (df["task_id"] == task_id)
    ].index[0] + 2

    sheet.update_cell(row, 4, done)
    sheet.update_cell(row, 5, completed_date or "")

def update_task(sheet, section, task_id, done=None, completed_date=None,
                notes=None, event_date=None, ptos_involved=None,
                assembly_date=None, assembly_driver=None, anthem_singer=None,
                volunteer_coordinator=None, social_channels=None,
                ticket_sales_url=None, ticket_dashboard_url=None):

    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    row_idx = df[(df["section"]==section) & (df["task_id"]==task_id)].index[0] + 2

    if done is not None:
        sheet.update_cell(row_idx, 4, done)
    if completed_date is not None:
        sheet.update_cell(row_idx, 5, completed_date or "")
    if notes is not None:
        sheet.update_cell(row_idx, 6, notes or "")
    if event_date is not None:
        sheet.update_cell(row_idx, 7, event_date or "")
    if ptos_involved is not None:
        sheet.update_cell(row_idx, 8, ptos_involved or "")
    if assembly_date is not None:
        sheet.update_cell(row_idx, 9, assembly_date or "")
    if assembly_driver is not None:
        sheet.update_cell(row_idx, 10, assembly_driver or "")
    if anthem_singer is not None:
        sheet.update_cell(row_idx, 11, anthem_singer or "")
    if volunteer_coordinator is not None:
        sheet.update_cell(row_idx, 12, volunteer_coordinator or "")
    if social_channels is not None:
        sheet.update_cell(row_idx, 13, ", ".join(social_channels) if isinstance(social_channels, list) else social_channels)
    if ticket_sales_url is not None:
        sheet.update_cell(row_idx, 14, ticket_sales_url)
    if ticket_dashboard_url is not None:
        sheet.update_cell(row_idx, 15, ticket_dashboard_url)


#######################################################################

st.title("Harlem Wizards Event Organizer")


# -------------------------
# Helper function for tasks
# -------------------------
def task_list_section(section_name, tasks, special_inputs=None):
    """
    Display a section with tasks, checkboxes, and completion dates.
    special_inputs: dict of {task_name: function_to_handle_special_input}
    """
    st.write(f"### {section_name} Tasks")
    for i, task in enumerate(tasks):
        done_key = f"{section_name}_task{i}_done"
        date_key = f"{section_name}_task{i}_date"

        if done_key not in st.session_state:
            st.session_state[done_key] = False
        if date_key not in st.session_state:
            st.session_state[date_key] = None

        st.session_state[done_key] = st.checkbox(task, value=st.session_state[done_key], key=f"{section_name}_checkbox_{i}")
        
        # Special input if needed
        if special_inputs and task in special_inputs:
            special_inputs[task](i)

        if st.session_state[done_key]:
            st.session_state[date_key] = st.date_input(f"Enter completion date for '{task}'", value=st.session_state[date_key], key=f"{section_name}_date_{i}")
            if st.session_state[date_key]:
                formatted_date = st.session_state[date_key].strftime("%d_%b-%Y")
                st.success(f"✅ Task completed on: {formatted_date}")

# -------------------------
# Initial Planning Section
# -------------------------

if "initial_open" not in st.session_state:
    st.session_state.initial_open = False

if st.button("Initial Planning with Wizards - Target Dates ➡️ July & Aug"):
    st.session_state.initial_open = not st.session_state.initial_open

if st.session_state.initial_open:
    st.markdown("## 📝 Initial Planning with Wizards")
    

    # -------------------------
    # Load Sheet
    # -------------------------
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)

    pre_event_df = df_tasks[df_tasks["section"] == "Pre_Event"]

    # -------------------------
    # Tasks
    # -------------------------
    pre_event_tasks = [
        "Reach out to Event Support Rep to schedule Kickoff call 🏀",
        "Secure contracts with Harlem Wizards - 🏀 July - September",
        "Approve contract and submit deposit ($1500)",
        "When to expect digital marketing and where it's mailed to",
        "Rep will send out updated prices on seating",
        "Secure police detail for event"  # <-- new task
    ]

    for i, task_text in enumerate(pre_event_tasks):

        done_key = f"Pre_Event_task{i}_done"
        date_key = f"Pre_Event_task{i}_date"
        notes_key = f"Pre_Event_task{i}_notes"
        notes_loaded_key = f"{notes_key}_loaded"
    
        row = pre_event_df[pre_event_df["task_text"] == task_text]
    
        # ---------- INIT DONE ----------
        if done_key not in st.session_state:
            st.session_state[done_key] = (
                str(row["done"].iloc[0]).upper() == "TRUE"
                if not row.empty and "done" in row else False
            )
    
        # ---------- INIT DATE ----------
        if date_key not in st.session_state:
            if not row.empty and "completed_date" in row:
                completed_date_value = row["completed_date"].iloc[0]
                st.session_state[date_key] = pd.to_datetime(completed_date_value).date() if completed_date_value else None
            else:
                st.session_state[date_key] = None
    
        # ---------- INIT NOTES ----------
        if notes_key not in st.session_state:
            st.session_state[notes_key] = ""  # always initialize to prevent KeyError
    
        if not st.session_state.get(notes_loaded_key, False):
            st.session_state[notes_key] = row["Notes"].iloc[0] if not row.empty and "Notes" in row else ""
            st.session_state[notes_loaded_key] = True
    
        # ---------- CHECKBOX ----------
        st.session_state[done_key] = st.checkbox(
            task_text,
            value=st.session_state[done_key],
            key=f"{done_key}_checkbox"
        )
    
        # ---------- TASK NOTES ----------
        with st.expander(f"Add notes for '{task_text}':"):
            st.text_area(
                "Notes:",
                value=st.session_state[notes_key],
                key=notes_key,
                height=120
            )
    
        # ---------- COMPLETION DATE ----------
        if st.session_state[done_key]:
            st.session_state[date_key] = st.date_input(
                f"Completion date for '{task_text}'",
                value=st.session_state[date_key],
                key=f"{date_key}_input"
            )
    
        # ---------- SAVE TO SHEET ----------
        if not row.empty:
            row_idx = row.index[0] + 2
        else:
            row_idx = len(df_tasks) + 2
            sheet.append_row(["Pre_Event", i+1, task_text, False, "", ""])
    
        # ---------- SAVE TO SHEET (ONLY WHEN DONE OR NOTES CHANGED) ----------
        if st.session_state[done_key] or st.session_state.get(notes_key):
        
            if not row.empty:
                row_idx = row.index[0] + 2
            else:
                row_idx = len(df_tasks) + 2
                sheet.append_row(["Pre_Event", i+1, task_text, False, "", ""])
        
            update_task(
                sheet,
                section="Pre_Event",
                task_id=i+1,
                done=st.session_state[done_key],
                completed_date=(
                    st.session_state[date_key].strftime("%Y-%m-%d")
                    if st.session_state[date_key]
                    else ""
                ),
                notes=st.session_state[notes_key]
            )   

            if st.button("💾 Save Task", key=f"save_pre_event_{i}"):
                update_task(
                    sheet,
                    section="Pre_Event",
                    task_id=i+1,
                    done=st.session_state[done_key],
                    completed_date=(
                        st.session_state[date_key].strftime("%Y-%m-%d")
                        if st.session_state[date_key]
                        else ""
                    ),
                    notes=st.session_state[notes_key]
                )
                st.success("Saved")



# -------------------------
# Nipmuc Facilities Section
# -------------------------

if "nipmuc_facilities_open" not in st.session_state:
    st.session_state.nipmuc_facilities_open = False

if st.button("Nipmuc Facilities - Secure Venue and Resources - Target Dates ➡️ July & Sept"):
    st.session_state.nipmuc_facilities_open = not st.session_state.nipmuc_facilities_open

if st.session_state.nipmuc_facilities_open:
    st.markdown("🏫 Nipmuc Facilities - Venue and Resources")
    
    # -------------------------
    # Load Sheet
    # -------------------------
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)
    
    facilities_df = df_tasks[df_tasks["section"] == "Facilities"]

    # Task description
    st.info(
        "📞 Reach out to Kim Lowther (Facilities Manager in Central Office) to secure the following:\n"
        "- Event date\n"
        "- Scoreboard/time clock\n"
        "- Lobby, restrooms, locker rooms for players and teachers\n"
        "- 12 tables, unlimted access to chairs, green tablecloths\n"
        "- Custodial staff\n"
        "- Flatbed or hand truck\n"
        "- Backup PA system\n"
        "- Confirm 3-pronged electric outlet for microphone setup"
    )
    
    facilities_tasks = [
        "Confirm venue availability",
        "Ensure necessary resources (see above) are available"
    ]

    for i, task_text in enumerate(facilities_tasks):
        done_key = f"facilities_task{i}_done"
        date_key = f"facilities_task{i}_date"
        notes_key = f"facilities_task{i}_notes"
        notes_loaded_key = f"{notes_key}_loaded"

        row = facilities_df[facilities_df["task_text"] == task_text]

        # ---------- INIT DONE ----------
        if done_key not in st.session_state:
            st.session_state[done_key] = (
                str(row["done"].iloc[0]).upper() == "TRUE"
                if not row.empty
                else False
            )

        # ---------- INIT DATE ----------
        if date_key not in st.session_state:
            if not row.empty:
                completed_date_value = row["completed_date"].iloc[0] if "completed_date" in row else None
                if completed_date_value:
                    st.session_state[date_key] = pd.to_datetime(completed_date_value).date()
                else:
                    st.session_state[date_key] = None
            else:
                st.session_state[date_key] = None

        # ---------- INIT NOTES (LOAD ONCE FROM SHEET) ----------
        if not st.session_state.get(notes_loaded_key, False):
            st.session_state[notes_key] = (
                row["Notes"].iloc[0] if not row.empty and "Notes" in row.columns else ""
            )
            st.session_state[notes_loaded_key] = True

        # ---------- CHECKBOX ----------
        st.session_state[done_key] = st.checkbox(
            task_text,
            value=st.session_state[done_key],
            key=f"{done_key}_checkbox"
        )

        # ---------- FACILITIES NOTES ----------
        if task_text == "Confirm venue availability":
            with st.expander("Details for Facilities Call"):
                st.info("💾  See To-Do list for Kim Lowther above")

                # Text area for notes with existing notes loaded
                st.text_area(
                    "Add notes for the Facilities call/email:",
                    key=notes_key,
                    height=120,
                    value=st.session_state.get(notes_key, "")  # Load existing notes
                )

                if st.button("💾 Save Facilities Call Notes", key=f"save_{notes_key}"):
                    filtered_indices = df_tasks[
                        (df_tasks["section"] == "Facilities") &
                        (df_tasks["task_text"] == task_text)
                    ].index

                    if filtered_indices.size > 0:
                        row_idx = filtered_indices[0] + 2  # Adjust offset if necessary
                        sheet.update(
                            range_name=f"F{row_idx}",
                            values=[[st.session_state[notes_key]]]
                        )
                        st.success("Notes saved")
                    else:
                        st.error(f"No matching task found for: {task_text}")

# -------------------------
# Event Planning Section
# -------------------------

if "event_open" not in st.session_state:
    st.session_state.event_open = False

if st.button("Event Planning & PTO Partners - Target Dates ➡️ Sept & Oct"):
    st.session_state.event_open = not st.session_state.event_open

if st.session_state.event_open:
    EVENT_DATE_TASK = "Identify partners for event (PTO)"
    st.markdown("## 📅 Event Planning & PTO Partners")

    # -------------------------
    # Load Sheet
    # -------------------------
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)
    events_df = df_tasks[df_tasks["section"] == "Events"]

    # -------------------------
    # Event date input (main event)
    # -------------------------
    if "event_date" not in st.session_state:
        event_row = events_df[events_df["task_text"] == EVENT_DATE_TASK]
        if not event_row.empty and "Event Date" in event_row.columns:
            completed_event_date = event_row["Event Date"].iloc[0]
            st.session_state["event_date"] = pd.to_datetime(completed_event_date).date() if pd.notna(completed_event_date) else None
        else:
            st.session_state["event_date"] = None

    st.session_state.event_date = st.date_input(
        "Enter the date of the event",
        value=st.session_state["event_date"],
        key="event_date_input"
    )

    if pd.notna(st.session_state.event_date):
        st.info(f"📅 Event Date: {st.session_state.event_date.strftime('%d_%b-%Y')}")

    # -------------------------
    # Tasks
    # -------------------------
    event_tasks = [
        "Identify partners for event (PTO)",
        "Check in with Wizards Rep for marketing materials & to review updated prices and details",
        "Email schools to alert/schedule assemblies ✉️",
        "Schedule 20-minute assemblies (Memorial, Clough, Miscoe)",
        "Coordinate National Anthem singer(s)🎤"
    ]

    for i, task_text in enumerate(event_tasks):
        done_key = f"event_task{i}_done"
        date_key = f"event_task{i}_date"
        notes_key = f"event_task{i}_notes"
        notes_loaded_key = f"{notes_key}_loaded"

        row = events_df[events_df["task_text"] == task_text]

        # ---------- INIT DONE ----------
        if done_key not in st.session_state:
            st.session_state[done_key] = (
                str(row["done"].iloc[0]).upper() == "TRUE" if not row.empty and "done" in row.columns else False
            )

        # ---------- INIT DATE ----------
        if date_key not in st.session_state:
            if not row.empty and "completed_date" in row.columns:
                completed_date_value = row["completed_date"].iloc[0]
                st.session_state[date_key] = pd.to_datetime(completed_date_value).date() if pd.notna(completed_date_value) else None
            else:
                st.session_state[date_key] = None

        # ---------- INIT NOTES ----------
        if notes_key not in st.session_state:
            st.session_state[notes_key] = ""

        if not st.session_state.get(notes_loaded_key, False):
            st.session_state[notes_key] = row["Notes"].iloc[0] if not row.empty and "Notes" in row.columns else ""
            st.session_state[notes_loaded_key] = True

        # ---------- CHECKBOX ----------
        st.session_state[done_key] = st.checkbox(
            task_text,
            value=st.session_state[done_key],
            key=f"{done_key}_checkbox"
        )

        # ---------- NOTES ----------
        with st.expander(f"Add notes for '{task_text}':"):
            st.text_area(
                "Notes:",
                value=st.session_state.get(notes_key, ""),
                key=notes_key,
                height=120
            )

            
        # ---------- COMPLETION DATE ----------
        if st.session_state[done_key]:  # Show date input if the task is marked as done
            date_val = st.session_state.get(date_key)
            if pd.isna(date_val):  # handles NaT
                date_val = None
        
            st.session_state[date_key] = st.date_input(
                f"Completion date for '{task_text}'",
                value=date_val,
                key=f"{date_key}_input"
            )


        # ---------- SAVE TO SHEET ----------
        if not row.empty:
            row_idx = row.index[0] + 2
        else:
            row_idx = len(df_tasks) + 2
            sheet.append_row(["Events", i + 1, task_text, False, "", ""])

        # Safely update values, checking for None dates
        sheet.update(
            range_name=f"D{row_idx}:F{row_idx}",
            values=[[
                st.session_state[done_key],
                st.session_state[date_key].strftime("%Y-%m-%d") if pd.notna(st.session_state[date_key]) else "",
                st.session_state[notes_key]
            ]]
        )

    # -------------------------
    # SAVE EVENT DATE TO SHEET
    # -------------------------
    event_row = events_df[events_df["task_text"] == EVENT_DATE_TASK]
    event_task_done_key = "event_task0_done"
    if not event_row.empty and st.session_state.get(event_task_done_key) and pd.notna(st.session_state.get("event_date")):
        row_idx = event_row.index[0] + 2
        sheet.update(
            range_name=f"H{row_idx}",  # Column for Event Date
            values=[[st.session_state["event_date"].strftime("%Y-%m-%d")]]
        )
        st.success("📅 Event date saved to the sheet.")


# -------------------------
# Website Section
# -------------------------
if "website_open" not in st.session_state:
    st.session_state.website_open = False

if st.button("Website - Target Dates ➡️ Oct - Jan"):
    st.session_state.website_open = not st.session_state.website_open

if st.session_state.website_open:
    st.markdown("## 🌐 Website Tasks")

    website_tasks = [
        "Update Artwork for the website",
        "Update the Wizards main page with ticketing",
        "Update the Wizards corporate sponsorship page & menu page with logos & current pdfs"
    ]

    # Info/checklist for guidance
    task_info = {
        "Update Artwork for the website": [
            "Create Canva flyers ~Christmas, New Years, Generic to use on website",
            "Obtain high resolution flyers from Wizards",
            "Embed custom Wizards Upton Video",
            "Embed Wizards souvenir page",
            "Update MU Dream Team Canva roster"
        ],
        "Update the Wizards main page with ticketing": [
            "Ensure ticketing links are up to date",
            "Check that seating info and pricing is correct",
            "Confirm ticketing dashboard is functioning"
        ],
        "Update the Wizards corporate sponsorship page & menu page with logos & current pdfs": [
            "Update logos for all corporate sponsors",
            "Replace old PDFs with current versions",
            "Confirm links are working"
        ]
    }

    # Load sheet
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)
    website_df = df_tasks[df_tasks["section"] == "Website"]

    for i, task_text in enumerate(website_tasks):
        done_key = f"website_task{i}_done"
        date_key = f"website_task{i}_date"
        notes_key = f"website_task{i}_notes"
        notes_loaded_key = f"{notes_key}_loaded"

        # Filter row from sheet
        row = website_df[website_df["task_text"] == task_text]

        # ---------- INIT DONE ----------
        if done_key not in st.session_state:
            st.session_state[done_key] = (
                str(row["done"].iloc[0]).upper() == "TRUE" if not row.empty else False
            )

        # ---------- INIT DATE ----------
        if date_key not in st.session_state:
            if not row.empty:
                completed_date_value = row["completed_date"].iloc[0] if "completed_date" in row else None
                st.session_state[date_key] = pd.to_datetime(completed_date_value).date() if completed_date_value else None
            else:
                st.session_state[date_key] = None

        # ---------- INIT NOTES ----------
        if not st.session_state.get(notes_loaded_key, False):
            st.session_state[notes_key] = (
                row["Notes"].iloc[0] if not row.empty and "Notes" in row.columns else ""
            )
            st.session_state[notes_loaded_key] = True

        # ---------- CHECKBOX ----------
        st.session_state[done_key] = st.checkbox(
            task_text,
            value=st.session_state[done_key],
            key=f"{done_key}_checkbox"
        )

        # ---------- INFO BOX ----------
        if task_text in task_info:
            st.info("\n".join([f"- {item}" for item in task_info[task_text]]))

        # ---------- NOTES ----------
        with st.expander(f"Add notes for '{task_text}'"):
            st.text_area(
                "Notes:",
                key=notes_key,
                height=120,
                value=st.session_state.get(notes_key, "")
            )
            if st.button(f"💾 Save Notes for '{task_text}'", key=f"save_{notes_key}"):
                if not row.empty:
                    row_idx = website_df[website_df["task_text"] == task_text].index[0] + 2
                    sheet.update(
                        range_name=f"F{row_idx}",  # Notes column
                        values=[[st.session_state[notes_key]]]
                    )
                    st.success("Notes saved to the sheet.")

        # ---------- COMPLETION DATE ----------
        if st.session_state[done_key]:
            st.session_state[date_key] = st.date_input(
                f"Completion date for '{task_text}'",
                value=st.session_state[date_key],
                key=f"{date_key}_input"
            )

        # ---------- SAVE DONE + DATE ----------
        if not row.empty:
            row_idx = website_df[website_df["task_text"] == task_text].index[0] + 2
            sheet.update(
                range_name=f"D{row_idx}:E{row_idx}",
                values=[[st.session_state[done_key],
                         st.session_state[date_key].strftime("%Y-%m-%d") if st.session_state[date_key] else ""]]
            )
# -------------------------
# Mendon-Upton Dream Team Section
# -------------------------
# -------------------------
# Mendon-Upton Dream Team Section
# -------------------------
if "dream_team_open" not in st.session_state:
    st.session_state.dream_team_open = False

if st.button("Mendon-Upton Dream Team - Target Dates ➡️ Oct-Jan"):
    st.session_state.dream_team_open = not st.session_state.dream_team_open

if st.session_state.dream_team_open:
    st.header("🏆 Mendon-Upton Dream Team")

    # Tasks for Dream Team
    dream_team_tasks = [
        "T-shirts: Locate Vendor (e.g., Tommy the T-shirt guy @508-596-9925)", 
        "Secure artwork for T-shirts (front and back) that currently exists in drive", 
        "Obtain any new artwork from corporate sponsors",
        "Get teacher bios and pictures and post to website"
    ]

    # Special inputs for certain tasks
    def dream_team_special_inputs(i):
        task_text = dream_team_tasks[i]
        
        # Unique key for each task
        notes_key = f"DreamTeam_task{i}_notes"
        
        if task_text == "T-shirts: Locate Vendor (e.g., Tommy the T-shirt guy @508-596-9925)":
            with st.expander("Details for T-shirts"):
                st.info("📞 Contact Tommy the T-shirt guy to secure artwork and finalize designs.")
                
                st.text_area(
                    "Add notes for T-shirts:",
                    value=st.session_state.get(notes_key, ""),
                    key=notes_key,
                    height=120
                )
                if st.session_state.get(notes_key):
                    st.success(f"📝 Notes Saved: {st.session_state[notes_key]}")
    
        if task_text == "Get teacher bios and pictures and post to website":
            with st.expander("Details for Teacher Bios and Website Blurb"):
                teacher_bios_key = f"DreamTeam_task{i}_teacher_bios_notes"
                st.text_area(
                    "Add notes for teacher bios and website blurb:",
                    value=st.session_state.get(teacher_bios_key, ""),
                    key=teacher_bios_key,
                    height=120
                )
                if st.session_state.get(teacher_bios_key):
                    st.success(f"📝 Notes Saved: {st.session_state[teacher_bios_key]}")



    # Load sheet records and prepare DataFrame
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)
    dream_df = df_tasks[df_tasks["section"] == "DreamTeam"]

    for i, task_text in enumerate(dream_team_tasks):
        done_key = f"DreamTeam_task{i}_done"
        date_key = f"DreamTeam_task{i}_date"
        notes_key = f"DreamTeam_task{i}_notes"
        notes_loaded_key = f"{notes_key}_loaded"

        row = dream_df[dream_df["task_text"] == task_text]

        # ---------- INIT DONE ----------
        if done_key not in st.session_state:
            st.session_state[done_key] = (
                str(row["done"].iloc[0]).upper() == "TRUE" if not row.empty else False
            )

        # ---------- INIT DATE ----------
        if date_key not in st.session_state:
            if not row.empty:
                completed_date_value = row["completed_date"].iloc[0] if "completed_date" in row else None
                st.session_state[date_key] = pd.to_datetime(completed_date_value).date() if completed_date_value else None
            else:
                st.session_state[date_key] = None

        # ---------- INIT NOTES ----------
        if not st.session_state.get(notes_loaded_key, False):
            st.session_state[notes_key] = (
                row["Notes"].iloc[0] if not row.empty and "Notes" in row.columns else ""
            )
            st.session_state[notes_loaded_key] = True

        # ---------- CHECKBOX ----------
        st.session_state[done_key] = st.checkbox(
            task_text,
            value=st.session_state[done_key],
            key=f"{done_key}_checkbox"
        )

        # ---------- SPECIAL NOTES INPUT ----------
        if dream_team_special_inputs:
            dream_team_special_inputs(i)

        # ---------- COMPLETION DATE ----------
        if st.session_state[done_key]:
            st.session_state[date_key] = st.date_input(
                f"Completion date for '{task_text}'",
                value=st.session_state[date_key],
                key=f"{date_key}_input"
            )
            if st.session_state[date_key]:
                st.success(f"✅ Task completed on: {st.session_state[date_key].strftime('%d_%b-%Y')}")

        # ---------- SAVE TO SHEET ----------
        if not row.empty:
            row_idx = dream_df[dream_df["task_text"] == task_text].index[0] + 2  # Adjust for header row

            # Save 'done' status and completion date
            sheet.update(
                range_name=f"D{row_idx}:E{row_idx}",
                values=[[st.session_state[done_key],
                         st.session_state[date_key].strftime("%Y-%m-%d") if st.session_state[date_key] else ""]]
            )

            # Save notes
            if notes_key in st.session_state:
                sheet.update(
                    range_name=f"F{row_idx}",
                    values=[[st.session_state[notes_key]]]
                )

# -------------------------
# Volunteer Coordination Section

# -------------------------
if "vol_coord_open" not in st.session_state:
    st.session_state.vol_coord_open = False

if st.button("Volunteer Coordination - Target Dates ➡️ Sept-Jan"):
    st.session_state.vol_coord_open = not st.session_state.vol_coord_open

if st.session_state.vol_coord_open:
    st.markdown("## 🙋 Volunteer Coordination")

    # Load sheet data for Volunteers section
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)
    volunteer_df = df_tasks[df_tasks["section"] == "Volunteer"]

    # Volunteer Coordinator Input
    vol_coord_key = "volunteer_coordinator"
    if vol_coord_key not in st.session_state:
        vol_row = volunteer_df[volunteer_df["task_text"] == "Volunteer Coordinator"]
        st.session_state[vol_coord_key] = vol_row["Notes"].iloc[0] if not vol_row.empty and "Notes" in vol_row else ""

    st.session_state[vol_coord_key] = st.text_input(
        "Who is the volunteer coordinator?",
        value=st.session_state[vol_coord_key]
    )

    if st.session_state[vol_coord_key]:
        st.info(f"👤 Volunteer Coordinator: {st.session_state[vol_coord_key]}")
        # Save to sheet
        vol_coord_row = volunteer_df[volunteer_df["task_text"] == "Volunteer Coordinator"]
        if not vol_coord_row.empty:
            row_idx = vol_coord_row.index[0] + 2
        else:
            row_idx = len(df_tasks) + 2
            sheet.append_row(["Volunteer", row_idx-1, "Volunteer Coordinator", False, "", st.session_state[vol_coord_key]])
        sheet.update(f"F{row_idx}", [[st.session_state[vol_coord_key]]])

    # Volunteer Tasks
    vol_tasks = [
        "Recruit volunteers from all schools (e.g., Chris Evans @ NHS, Brian @ DECA)",
        "Coordinate day-of-event volunteer shifts",
        "Ensure volunteers have instructions and materials",
        "Assign volunteers to tasks"
    ]
    
    
    def volunteer_special_inputs(i):
        task_text = vol_tasks[i]
        notes_key = f"Volunteer_task{i}_notes"
        done_key = f"Volunteer_task{i}_done"
        date_key = f"Volunteer_task{i}_date"

        if task_text == "Coordinate day-of-event volunteer shifts":
            st.markdown(
                """
                <div style="margin-left: 20px; margin-bottom: 10px; color: #73faff; font-size: 1.1em;">
                <strong>Venue Volunteer Set Up:</strong><br>
                • Set up 4:30 PM – pull bleachers, set up chairs, help with hand truck & unloading van,\n direct Wizards to locker room (~4 volunteers)<br>
                • Greeters & ticket takers (Lobby) 5:30–6:45 PM (~5 volunteers)<br>
                • Concessions 5:00 PM: 2–3; 5–6 volunteers during halftime<br>
                • Seating attendants 5:00 PM: 2–3 volunteers (gym & meet-and-greet)<br>
                • Souvenir table 5:30 PM: 6 adults, 2 kids (8 total)<br>
                • General clean up during & after event (4 volunteers)<br>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Load previous data
        row = volunteer_df[volunteer_df["task_text"] == task_text]
        if not st.session_state.get(notes_key) and not row.empty:
            st.session_state[notes_key] = row["Notes"].iloc[0] if "Notes" in row.columns else ""
        if not st.session_state.get(done_key) and not row.empty:
            st.session_state[done_key] = str(row["done"].iloc[0]).upper() == "TRUE"
        if not st.session_state.get(date_key) and not row.empty:
            completed_date_value = row["completed_date"].iloc[0] if "completed_date" in row.columns else None
            st.session_state[date_key] = pd.to_datetime(completed_date_value).date() if completed_date_value else None

        # Only show Volunteer Organizations selector for the first task
        if i == 0:
            vol_orgs_key = f"Volunteer_task{i}_orgs"
            if vol_orgs_key not in st.session_state:
                st.session_state[vol_orgs_key] = []

            st.session_state[vol_orgs_key] = st.multiselect(
                "Select student organizations helping recruit volunteers:",
                ["NHS", "Jr NHS", "DECA", "Student Council", "Other"],
                default=st.session_state[vol_orgs_key]
            )

            if st.session_state[vol_orgs_key]:
                st.info(f"📌 Organizations: {', '.join(st.session_state[vol_orgs_key])}")

        # Notes input
        st.text_area(
            f"Add notes for '{task_text}':",
            value=st.session_state.get(notes_key, ""),
            key=notes_key,
            height=120
        )

        # ✅ ADD THIS
        st.session_state[done_key] = st.checkbox(
            f"Mark '{task_text}' as done",
            value=st.session_state.get(done_key, False),
            key=f"{done_key}_widget"
        )

        if st.session_state.get(done_key):
            st.session_state[date_key] = st.date_input(
                f"Completion date for '{task_text}'",
                value=st.session_state.get(date_key),
                key=f"{date_key}_input"
            )


        # Save to Google Sheet only when task is done
        if st.session_state.get(done_key):
            if not row.empty:
                row_idx = row.index[0] + 2
            else:
                row_idx = len(df_tasks) + 2
                sheet.append_row(["Volunteer", i+1, task_text, False, "", "", ""])  # Ensure Volunteer_Orgs column exists

            sheet.update(f"D{row_idx}", [[st.session_state[done_key]]])
            sheet.update(f"F{row_idx}", [[st.session_state.get(notes_key, "")]])
            
            if st.session_state.get(date_key):
                sheet.update(f"E{row_idx}", [[st.session_state[date_key].strftime("%Y-%m-%d")]])
            # Only save Volunteer Orgs for first task
            if i == 0 and st.session_state.get(vol_orgs_key):
                sheet.update(f"H{row_idx}", [[", ".join(st.session_state[vol_orgs_key])]])

    # Render tasks
    task_list_section(
        "Volunteer",
        vol_tasks,
        special_inputs={task: volunteer_special_inputs for task in vol_tasks}
    )



# -------------------------
# Marketing / Communications Section
# -------------------------
if "marketing_open" not in st.session_state:
    st.session_state.marketing_open = False

if st.button("Marketing / Communications - Target Dates ➡️ Nov-Jan"):
    st.session_state.marketing_open = not st.session_state.marketing_open

if st.session_state.marketing_open:
    st.markdown("## 📣 Marketing / Communications")

    # Load sheet data for Marketing section
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)
    marketing_df = df_tasks[df_tasks["section"] == "Marketing"]

    # Marketing Tasks
    marketing_tasks = [
        "Create and distribute flyers to schools",
        "Post adverts on social media",
        "Attend school events to publicize the event",
        "Coordinate with local media for coverage",
        "Send email communication to parents/students"
    ]

    def marketing_special_inputs(i):
        task_text = marketing_tasks[i]
        notes_key = f"Marketing_task{i}_notes"
        done_key = f"Marketing_task{i}_done"
        date_key = f"Marketing_task{i}_date"

        # Load previous notes / done / date from sheet if exists
        row = marketing_df[marketing_df["task_text"] == task_text]
        if not st.session_state.get(notes_key) and not row.empty:
            st.session_state[notes_key] = row["Notes"].iloc[0] if "Notes" in row.columns else ""
        if not st.session_state.get(done_key) and not row.empty:
            st.session_state[done_key] = str(row["done"].iloc[0]).upper() == "TRUE"
        if not st.session_state.get(date_key) and not row.empty:
            completed_date_value = row["completed_date"].iloc[0] if "completed_date" in row.columns else None
            st.session_state[date_key] = pd.to_datetime(completed_date_value).date() if completed_date_value else None

        # Special input for social media task
        if task_text == "Post adverts on social media":
            social_key = f"Marketing_task{i}_social_channels"
            if social_key not in st.session_state:
                st.session_state[social_key] = []
            st.session_state[social_key] = st.multiselect(
                "Select social media channels to post on:",
                ["Facebook", "Instagram", "Twitter", "LinkedIn", "Other"],
                default=st.session_state[social_key]
            )
            if st.session_state[social_key]:
                st.info(f"📣 Channels: {', '.join(st.session_state[social_key])}")

        # Notes input
        st.text_area(
            f"Add notes for '{task_text}':",
            value=st.session_state.get(notes_key, ""),
            key=notes_key,
            height=120
        )

        # Save to Google Sheet when task is marked done
        if st.session_state.get(done_key):
            if not row.empty:
                row_idx = row.index[0] + 2
            else:
                row_idx = len(df_tasks) + 2
                sheet.append_row(["Marketing", i+1, task_text, False, "", "", ""])  # Extra column for social channels

            sheet.update(f"D{row_idx}", [[st.session_state[done_key]]])
            sheet.update(f"F{row_idx}", [[st.session_state.get(notes_key, "")]])
            if st.session_state.get(date_key):
                sheet.update(f"E{row_idx}", [[st.session_state[date_key].strftime("%Y-%m-%d")]])

            # Save social channels if applicable
            if task_text == "Post adverts on social media" and st.session_state.get(social_key):
                sheet.update(f"H{row_idx}", [[", ".join(st.session_state[social_key])]])

    # Render tasks
    task_list_section(
        "Marketing",
        marketing_tasks,
        special_inputs={task: marketing_special_inputs for task in marketing_tasks}
    )

# -------------------------
# Fundraising Section
# -------------------------
# # --- Fundraising / Corporate Sponsorships Section ---
if "fundraising_open" not in st.session_state:
    st.session_state.fundraising_open = False
if st.button("Fundraising / Corporate Sponsorships", key="fundraising_button"):
    st.session_state.fundraising_open = not st.session_state.fundraising_open

if st.session_state.fundraising_open:
    fundraising_tab()


# -------------------------
# Ticketing / Sales / Finance Section
# -------------------------
if "finance_open" not in st.session_state:
    st.session_state.finance_open = False

if st.button("Ticketing / Sales / Finance - Target Dates ➡️ November"):
    st.session_state.finance_open = not st.session_state.finance_open

if st.session_state.finance_open:
    st.markdown("## 💵 Ticketing / Sales / Finance")

    # Load sheet data for Finance section
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)
    finance_df = df_tasks[df_tasks["section"] == "Finance"]

    finance_tasks = [
        "Set ticket prices and quantity",
        "Create online ticket sales page",
        "Track ticket sales",
        "Set up Raffles/Get permit",
        "Reconcile final finances after event"
    ]

    def finance_special_inputs(i):
        task_text = finance_tasks[i]
        notes_key = f"Finance_task{i}_notes"
        done_key = f"Finance_task{i}_done"
        date_key = f"Finance_task{i}_date"

        # Load previous data from sheet
        row = finance_df[finance_df["task_text"] == task_text]
        if not st.session_state.get(notes_key) and not row.empty:
            st.session_state[notes_key] = row["Notes"].iloc[0] if "Notes" in row.columns else ""
        if not st.session_state.get(done_key) and not row.empty:
            st.session_state[done_key] = str(row["done"].iloc[0]).upper() == "TRUE"
        if not st.session_state.get(date_key) and not row.empty:
            completed_date_value = row["completed_date"].iloc[0] if "completed_date" in row.columns else None
            st.session_state[date_key] = pd.to_datetime(completed_date_value).date() if completed_date_value else None

        # Special inputs
        if task_text == "Create online ticket sales page":
            url_key = f"Finance_task{i}_url"
            if url_key not in st.session_state:
                st.session_state[url_key] = ""
            st.session_state[url_key] = st.text_input(
                "Enter the URL for the online ticket sales page:",
                value=st.session_state[url_key]
            )
            if st.session_state[url_key]:
                st.info(f"🌐 Ticket Sales Page: {st.session_state[url_key]}")

        if task_text == "Track ticket sales":
            dashboard_key = f"Finance_task{i}_dashboard"
            if dashboard_key not in st.session_state:
                st.session_state[dashboard_key] = ""
            st.session_state[dashboard_key] = st.text_input(
                "Enter the URL for the Wizards dashboard (Username: muef@mursd.org, PW= FNAF2024):",
                value=st.session_state[dashboard_key]
            )
            if st.session_state[dashboard_key]:
                st.info(f"📊 Ticket Sales Dashboard: {st.session_state[dashboard_key]}")

        # Notes input
        st.text_area(
            f"Add notes for '{task_text}':",
            value=st.session_state.get(notes_key, ""),
            key=notes_key,
            height=120
        )

        # Done checkbox
        st.session_state[done_key] = st.checkbox(
            f"Mark '{task_text}' as done",
            value=st.session_state.get(done_key, False),
            key=f"{done_key}_widget"
        )

        # Save to Google Sheet when task is done
        if st.session_state[done_key]:
            if not row.empty:
                row_idx = row.index[0] + 2
            else:
                row_idx = len(df_tasks) + 2
                sheet.append_row(["Finance", i+1, task_text, False, "", ""])

            sheet.update(f"D{row_idx}", [[st.session_state[done_key]]])
            sheet.update(f"F{row_idx}", [[st.session_state.get(notes_key, "")]])
            if st.session_state.get(date_key):
                sheet.update(f"E{row_idx}", [[st.session_state[date_key].strftime("%Y-%m-%d")]])

            # Save special URLs if applicable
            if task_text == "Create online ticket sales page" and st.session_state.get(url_key):
                sheet.update(f"H{row_idx}", [[st.session_state[url_key]]])
            if task_text == "Track ticket sales" and st.session_state.get(dashboard_key):
                sheet.update(f"H{row_idx}", [[st.session_state[dashboard_key]]])

    # Render Finance tasks
    task_list_section(
        "Finance",
        finance_tasks,
        special_inputs={task: finance_special_inputs for task in finance_tasks}
    )

# -------------------------
# Event Day Logistics Section
# -------------------------
if "eventday_open" not in st.session_state:
    st.session_state.eventday_open = False

if st.button("Event Day Logistics - Game Day ➡️ Last Saturday in January"):
    st.session_state.eventday_open = not st.session_state.eventday_open

if st.session_state.eventday_open:
    st.markdown("## 🎪 Event Day Logistics")

    # Event Day Tasks
    eventday_tasks = [
        "Set up Souvenir Space",
        "Check AV equipment",
        "Organize registration/check-in tables",
        "Coordinate with volunteers for event flow",
        "Manage food/beverage setup (Pizza, Gatorade, Snacks for players and volunteers)",
        "Manage concessions",
        "Ensure safety and first aid stations are ready",
        "Cleanup after the event"
    ]

    # Load sheet data
    records = sheet.get_all_records()
    df_tasks = pd.DataFrame(records)
    eventday_df = df_tasks[df_tasks["section"] == "EventDay"]

    def eventday_special_inputs(i):
        task_text = eventday_tasks[i]
        notes_key = f"EventDay_task{i}_notes"
        done_key = f"EventDay_task{i}_done"
        date_key = f"EventDay_task{i}_date"

                # ✅ ADD THIS BLOCK
        if task_text == "Set up Souvenir Space":
            st.markdown(
                """
                <div style="margin-left: 20px; margin-bottom: 10px; color: #73faff; font-size: 1.2em;">
                <strong>Souvenir Sales Setup:</strong><br>
                • 8 tables (6–7 feet each) with Green tablecloths if possible<br>
                • 16 chairs<br>
                • Location near entrance in an area capable of handling a large crowd
                </div>
                """,
                unsafe_allow_html=True
            )
        
               # ✅ ADD THIS BLOCK
        if task_text == "Organize registration/check-in tables":
           st.markdown(
               """
               <div style="margin-left: 20px; margin-bottom: 10px; color: #73faff; font-size: 1.2em;">
               <strong>Registration & Check-in tables:</strong><br>
               • 4 tables (6 feet each) with Green tablecloths if possible<br>
               • 6 chairs<br>
               • Location: Lobby- 1 on either side of entrance, 1 in center, 1 in front lobby for same day purchase
               </div>
               """,
               unsafe_allow_html=True
           )
        
        # Load previous data from sheet
        row = eventday_df[eventday_df["task_text"] == task_text]
        
        if not st.session_state.get(notes_key) and not row.empty:
            st.session_state[notes_key] = row["Notes"].iloc[0] if "Notes" in row.columns else ""
        if not st.session_state.get(done_key) and not row.empty:
            st.session_state[done_key] = str(row["done"].iloc[0]).upper() == "TRUE"
        if not st.session_state.get(date_key) and not row.empty:
            completed_date_value = row["completed_date"].iloc[0] if "completed_date" in row.columns else None
            st.session_state[date_key] = pd.to_datetime(completed_date_value).date() if completed_date_value else None

        # # Notes input
        # st.text_area(
        #     f"Add notes for '{task_text}':",
        #     value=st.session_state.get(notes_key, ""),
        #     key=notes_key,
        #     height=120
        # )

        # Done checkbox
        # st.session_state[done_key] = st.checkbox(
        #     f"Mark '{task_text}' as done",
        #     value=st.session_state.get(done_key, False),
        #     key=f"{done_key}_widget"
        # )

        # Save to Google Sheet when done
        if st.session_state[done_key]:
            if not row.empty:
                row_idx = row.index[0] + 2
            else:
                row_idx = len(df_tasks) + 2
                sheet.append_row(["EventDay", i+1, task_text, False, "", ""])

            sheet.update(f"D{row_idx}", [[st.session_state[done_key]]])
            sheet.update(f"F{row_idx}", [[st.session_state.get(notes_key, "")]])
            if st.session_state.get(date_key):
                sheet.update(f"E{row_idx}", [[st.session_state[date_key].strftime("%Y-%m-%d")]])

    # Render Event Day tasks
    task_list_section(
        "EventDay",
        eventday_tasks,
        special_inputs={task: eventday_special_inputs for task in eventday_tasks}
    )

    # Additional general notes for Event Day Logistics
    if "eventday_notes" not in st.session_state:
        st.session_state.eventday_notes = ""

    eventday_notes = st.text_area(
        "Add additional notes or tasks for Event Day Logistics:",
        value=st.session_state.eventday_notes,
        key="eventday_notes_textarea",
        height=120
    )

    # Save general notes to sheet (create a single row if none exists)
    if eventday_notes:
        st.session_state.eventday_notes = eventday_notes
        st.success(f"📝 Notes Saved: {eventday_notes}")

        # Save or update a "general notes" row in the sheet
        general_row = eventday_df[eventday_df["task_text"] == "General Event Day Notes"]
        if not general_row.empty:
            row_idx = general_row.index[0] + 2
            sheet.update(f"F{row_idx}", [[eventday_notes]])
        else:
            row_idx = len(df_tasks) + 2
            sheet.append_row(["EventDay", row_idx-1, "General Event Day Notes", False, "", eventday_notes])

    # Close button for Event Day Logistics section
    if st.button("Close Event Day Logistics Section", key="close_eventday"):
        st.session_state.eventday_open = False


