# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 09:17:28 2025

@author: gina-
"""
import streamlit as st
from fundraising import fundraising_tab  # Make sure this exists in fundraising.py

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
# Pre-Event Planning Section
# -------------------------
if "pre_event_open" not in st.session_state:
    st.session_state.pre_event_open = False

if st.button("Pre-Event Planning"):
    st.session_state.pre_event_open = not st.session_state.pre_event_open

if st.session_state.pre_event_open:
    # Event date input
    if "event_date" not in st.session_state:
        st.session_state.event_date = None
    st.session_state.event_date = st.date_input("Enter the date of the event", value=st.session_state.event_date)
    if st.session_state.event_date:
        st.info(f"📅 Event Date: {st.session_state.event_date.strftime('%d_%b-%Y')}")

    pre_event_tasks = [
        "Secure contracts with Harlem Wizards",
        "Approve contract and submit deposit ($1500)",
        "Identify partners for event (PTO)",
        "Reach out to Event Support Rep to schedule Kickoff call",
        "Meeting with Marissa to review updated prices and details",
        "Email schools to alert/schedule assemblies",
        "Schedule 20-minute assemblies (Memorial, Clough, Miscoe)",
        "Coordinate National Anthem singer(s)"
    ]

    def pre_event_special_inputs(i):
        # PTO input
        if pre_event_tasks[i] == "Identify partners for event (PTO)":
            with st.expander("Enter PTO(s) involved"):
                if "ptos_involved" not in st.session_state:
                    st.session_state.ptos_involved = ""
                st.session_state.ptos_involved = st.text_input("PTO(s) (comma separated):", value=st.session_state.ptos_involved)
                if st.session_state.ptos_involved:
                    st.info(f"🏫 PTOs: {st.session_state.ptos_involved}")

    task_list_section("Pre_Event", pre_event_tasks, special_inputs={task: pre_event_special_inputs for task in pre_event_tasks})

# -------------------------
# Volunteer Coordination Section
# -------------------------
if "vol_coord_open" not in st.session_state:
    st.session_state.vol_coord_open = False

if st.button("Volunteer Coordination"):
    st.session_state.vol_coord_open = not st.session_state.vol_coord_open

if st.session_state.vol_coord_open:
    # Volunteer Coordinator
    if "volunteer_coordinator" not in st.session_state:
        st.session_state.volunteer_coordinator = ""
    st.session_state.volunteer_coordinator = st.text_input("Who is the volunteer coordinator?", value=st.session_state.volunteer_coordinator)
    if st.session_state.volunteer_coordinator:
        st.info(f"👤 Volunteer Coordinator: {st.session_state.volunteer_coordinator}")

    vol_tasks = [
        "Recruit volunteers from all schools",
        "Coordinate day-of-event volunteer shifts",
        "Ensure volunteers have instructions and materials",
        "Assign volunteers to tasks"
    ]

    def volunteer_special_inputs(i):
        # Organizations for recruiting volunteers
        if vol_tasks[i] == "Recruit volunteers from all schools":
            if "vol_orgs" not in st.session_state:
                st.session_state.vol_orgs = []
            st.session_state.vol_orgs = st.multiselect(
                "Select student organizations helping recruit volunteers:",
                ["NHS", "Jr NHS", "DECA", "Student Council", "Other"],
                default=st.session_state.vol_orgs
            )
            if st.session_state.vol_orgs:
                st.info(f"📌 Organizations: {', '.join(st.session_state.vol_orgs)}")
        # Placeholder for assigning volunteers
        if vol_tasks[i] == "Assign volunteers to tasks":
            st.info("🔗 Volunteer sheet integration will go here.")

    task_list_section("Volunteer", vol_tasks, special_inputs={task: volunteer_special_inputs for task in vol_tasks})

# -------------------------
# Marketing / Communications Section
# -------------------------
if "marketing_open" not in st.session_state:
    st.session_state.marketing_open = False

if st.button("Marketing / Communications"):
    st.session_state.marketing_open = not st.session_state.marketing_open

if st.session_state.marketing_open:
    marketing_tasks = [
        "Create and distribute flyers to schools",
        "Post adverts on social media",
        "Attend school events to publicize the event",
        "Coordinate with local media for coverage",
        "Send email communication to parents/students"
    ]

    def marketing_special_inputs(i):
        if marketing_tasks[i] == "Post adverts on social media":
            if "social_channels" not in st.session_state:
                st.session_state.social_channels = []
            st.session_state.social_channels = st.multiselect(
                "Select social media channels to post on:",
                ["Facebook", "Instagram", "Twitter", "LinkedIn", "Other"],
                default=st.session_state.social_channels
            )
            if st.session_state.social_channels:
                st.info(f"📣 Channels: {', '.join(st.session_state.social_channels)}")

    task_list_section("Marketing", marketing_tasks, special_inputs={task: marketing_special_inputs for task in marketing_tasks})

# -------------------------
# Fundraising Section
# -------------------------
# # --- Fundraising / Corporate Sponsorships Section ---
# if "fundraising_open" not in st.session_state:
#     st.session_state.fundraising_open = False
# if st.button("Fundraising / Corporate Sponsorships", key="fundraising_button"):
#     st.session_state.fundraising_open = not st.session_state.fundraising_open

# if st.session_state.fundraising_open:
#     fundraising_tab()


# -------------------------
# Ticketing / Sales / Finance Section
# -------------------------
if "finance_open" not in st.session_state:
    st.session_state.finance_open = False

if st.button("Ticketing / Sales / Finance"):
    st.session_state.finance_open = not st.session_state.finance_open

if st.session_state.finance_open:
    finance_tasks = [
        "Set ticket prices and quantity",
        "Create online ticket sales page",
        "Track ticket sales",
        "Set up Raffles/Get permit",
        "Reconcile final finances after event"
    ]

    def finance_special_inputs(i):
        if finance_tasks[i] == "Create online ticket sales page":
            if "ticket_sales_url" not in st.session_state:
                st.session_state.ticket_sales_url = ""
            st.session_state.ticket_sales_url = st.text_input(
                "Enter the URL for the online ticket sales page:",
                value=st.session_state.ticket_sales_url
            )
            if st.session_state.ticket_sales_url:
                st.info(f"🌐 Ticket Sales Page: {st.session_state.ticket_sales_url}")
        if finance_tasks[i] == "Track ticket sales":
            if "ticket_dashboard_url" not in st.session_state:
                st.session_state.ticket_dashboard_url = ""
            st.session_state.ticket_dashboard_url = st.text_input(
                "Enter the URL for the Wizards dashboard (Username: muef@mursd.org, PW= FNAF2024):",
                value=st.session_state.ticket_dashboard_url
            )
            if st.session_state.ticket_dashboard_url:
                st.info(f"📊 Ticket Sales Dashboard: {st.session_state.ticket_dashboard_url}")

    task_list_section("Finance", finance_tasks, special_inputs={task: finance_special_inputs for task in finance_tasks})

# -------------------------
# Event Day Logistics Section
# -------------------------
if "eventday_open" not in st.session_state:
    st.session_state.eventday_open = False

if st.button("Event Day Logistics"):
    st.session_state.eventday_open = not st.session_state.eventday_open

if st.session_state.eventday_open:
    eventday_tasks = [
        "Set up the venue",
        "Check AV equipment",
        "Organize registration/check-in tables",
        "Coordinate with volunteers for event flow",
        "Manage food/beverage setup",
        "Manage concessions",
        "Ensure safety and first aid stations are ready",
        "Cleanup after the event"
    ]
    task_list_section("EventDay", eventday_tasks)

# -------------------------
# Post-Event Section
# -------------------------
if "post_event_open" not in st.session_state:
    st.session_state.post_event_open = False

if st.button("Post-Event"):
    st.session_state.post_event_open = not st.session_state.post_event_open

if st.session_state.post_event_open:
    post_event_tasks = [
        "Send thank-you emails to sponsors, partners, and volunteers",
        "Reconcile finances and submit final report"
    ]
    task_list_section("PostEvent", post_event_tasks)
