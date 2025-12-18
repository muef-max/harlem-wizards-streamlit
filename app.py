# %%
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
# Initial Planning Section
# -------------------------
if "initial_open" not in st.session_state:
    st.session_state.initial_open = False

if st.button("Initial Planning with Wizards - Target Dates ➡️ July & August"):
    st.session_state.initial_open = not st.session_state.initial_open
if st.session_state.initial_open:
    st.markdown("## 📝 Initial Planning with Wizards")

if st.session_state.initial_open:
    # Event date input
    if "event_date" not in st.session_state:
        st.session_state.event_date = None
    st.session_state.event_date = st.date_input("Enter the date of the event", value=st.session_state.event_date)
    if st.session_state.event_date:
        st.info(f"📅 Event Date: {st.session_state.event_date.strftime('%d_%b-%Y')}")

    # Define the tasks for Initial Planning
    pre_event_tasks = [
        "Reach out to Event Support Rep to schedule Kickoff call 🏀",
        "Secure contracts with Harlem Wizards - 🏀 July - September",
        "Approve contract and submit deposit ($1500)",
        "When to expect digital marketing and where it's mailed to",
        "Rep will send out updated prices on seating",
    ]

    # Define the special inputs for each task
    def initial_open_special_inputs(i):
        if pre_event_tasks[i] == "Reach out to Event Support Rep to schedule Kickoff call 🏀":
            with st.expander("Details for Kickoff Call"):
                # Display contact information
                st.info("📞 Todd Davis (President) or Stefani (Account Mgr) @ 573-567-0202")

                # Notes box
                kickoff_notes = st.text_area(
                    "Add notes for the Kickoff Call:",
                    value=st.session_state.get("kickoff_notes", ""),
                    key="kickoff_notes"
                )

                # Display saved notes
                if kickoff_notes:
                    st.success(f"📝 Notes Saved: {kickoff_notes}")

    # Render the task list for Initial Planning
    task_list_section("Pre_Event", pre_event_tasks, special_inputs={task: initial_open_special_inputs for task in pre_event_tasks})

# -------------------------
# Nipmuc Facilities Section
# -------------------------
if "nipmuc_facilities_open" not in st.session_state:
    st.session_state.nipmuc_facilities_open = False

if st.button("Nipmuc Facilities - Secure Venue and Resources - Target Dates ➡️ July & September"):
    st.session_state.nipmuc_facilities_open = not st.session_state.nipmuc_facilities_open

if st.session_state.nipmuc_facilities_open:
    st.header("🏫 Nipmuc Facilities - Venue and Resources")

    # Task description
    st.info(
        "📞 Reach out to Kim Lowther (Facilities Manager in Central Office) to secure the following:\n"
        "- Event date\n"
        "- Scoreboard/time clock\n"
        "- Lobby, restrooms, locker rooms for players and teachers\n"
        "- 12 tables, 20 chairs, green tablecloths\n"
        "- Custodial staff\n"
        "- Flatbed or hand truck\n"
        "- Backup PA system\n"
        "- Confirm 3-pronged electric outlet for microphone setup"
    )

    # Notes box for Nipmuc Facilities
    if "nipmuc_notes" not in st.session_state:
        st.session_state.nipmuc_notes = ""
    nipmuc_notes = st.text_area(
        "Add notes for Nipmuc Facilities:",
        value=st.session_state.nipmuc_notes,
        key="nipmuc_notes"
    )

    # Display saved notes
    if nipmuc_notes:
        st.session_state.nipmuc_notes = nipmuc_notes
        st.success(f"📝 Notes Saved: {nipmuc_notes}")

    # Close button for Nipmuc Facilities section
    if st.button("Close Nipmuc Facilities Section", key="close_nipmuc"):
        st.session_state.nipmuc_facilities_open = False    
# -------------------------
# Pre-Event Planning Section
# -------------------------
if "pre_event_open" not in st.session_state:
    st.session_state.pre_event_open = False

if st.button("Pre-Event Planning & PTO Partners - Target Dates ➡️ September & October"):
    st.session_state.pre_event_open = not st.session_state.pre_event_open
if st.session_state.pre_event_open:
    st.markdown("## 📅 Pre-Event Planning & PTO Partners")
if st.session_state.pre_event_open:
    # Event date input
    if "event_date" not in st.session_state:
        st.session_state.event_date = None
    st.session_state.event_date = st.date_input("Enter the date of the event", value=st.session_state.event_date)
    if st.session_state.event_date:
        st.info(f"📅 Event Date: {st.session_state.event_date.strftime('%d_%b-%Y')}")

    pre_event_tasks = [
        "Identify partners for event (PTO)",
        "Check in with Wizards Rep for marketing materials & to review updated prices and details",
        "Email schools to alert/schedule assemblies ✉️",
        "Schedule 20-minute assemblies (Memorial, Clough, Miscoe)",
        "Coordinate National Anthem singer(s)🎤"
    ]

    def pre_event_special_inputs(i):
        if pre_event_tasks[i] == "Reach out to Event Support Rep to schedule Kickoff call 🏀":
            with st.expander("Details for Kickoff Call"):
                # Display contact information
                st.info("📞 Todd (Owner) or Stefani @ 573-567-0202")

                # Notes box
                kickoff_notes = st.text_area(
                    "Add notes for the Kickoff Call:",
                    value=st.session_state.get("kickoff_notes", ""),
                    key="kickoff_notes"
                )

                # Display saved notes
                if kickoff_notes:
                    st.success(f"📝 Notes Saved: {kickoff_notes}")
        # PTO input
        if pre_event_tasks[i] == "Identify partners for event (PTO)":
            with st.expander("Enter PTO(s) involved"):
                if "ptos_involved" not in st.session_state:
                    st.session_state.ptos_involved = ""
                st.session_state.ptos_involved = st.text_input("PTO(s) (comma separated):", value=st.session_state.ptos_involved)
                if st.session_state.ptos_involved:
                    st.info(f"🏫 PTOs: {st.session_state.ptos_involved}")

        # Assembly scheduling input
        if pre_event_tasks[i] == "Schedule 20-minute assemblies (Memorial, Clough, Miscoe)":
            with st.expander("Enter assembly details for all schools"):
                # One date for all schools
                assembly_date = st.date_input(
                    "Select assembly date for all schools",
                    value=st.session_state.get("assembly_date", None),
                    key="assembly_date"
                )

                # Separate times for each school
                schools = ["Memorial", "Clough", "Miscoe"]
                for school in schools:
                    school_time_key = f"{school}_assembly_time"

                    # Time input for each school
                    school_time = st.time_input(
                        f"Select assembly time for {school}",
                        value=st.session_state.get(school_time_key, None),
                        key=school_time_key
                    )

                # Single driver input for all schools
                if "assembly_driver" not in st.session_state:
                    st.session_state["assembly_driver"] = ""
                assembly_driver = st.text_input(
                    "Who will drive to all the assemblies?",
                    value=st.session_state["assembly_driver"],
                    key="assembly_driver"
                )

                # Display confirmation for all schools
                if assembly_date and all(st.session_state.get(f"{school}_assembly_time") for school in schools):
                    st.success(
                        f"📅 Assemblies Scheduled on {assembly_date.strftime('%d_%b-%Y')} | Driver: {assembly_driver}"
                    )
                    for school in schools:
                        school_time = st.session_state.get(f"{school}_assembly_time")
                        st.info(f"{school}: {school_time.strftime('%H:%M')}")
        # National Anthem singer input
        if pre_event_tasks[i] == "Coordinate National Anthem singer(s)🎤":
            with st.expander("Enter details for the National Anthem singer(s)"):
                if "anthem_singer" not in st.session_state:
                    st.session_state["anthem_singer"] = ""
                anthem_singer = st.text_input(
                    "Who will sing the National Anthem?",
                    value=st.session_state["anthem_singer"],
                    key="anthem_singer"
                )
                # Display confirmation
                if anthem_singer:
                    st.success(f"🎤 National Anthem Singer: {anthem_singer}")
    task_list_section("Pre_Event", pre_event_tasks, special_inputs={task: pre_event_special_inputs for task in pre_event_tasks})
# -------------------------
# Website Section
# -------------------------
if "website_open" not in st.session_state:
    st.session_state.website_open = False

if st.button("Website - Target Dates ➡️ October through January"):
    st.session_state.website_open = not st.session_state.website_open

if st.session_state.website_open:
    st.header("🌐 Website Updates")

    website_tasks = [
        "Update the Wizards tab with current advertising",
        "Update the Wizards tab with ticketing",
        "Update the Wizards tab with sponsor page"
    ]

    def website_special_inputs(i):
        if website_tasks[i] == "Update the Wizards tab with current advertising":
            with st.expander("Details for Advertising Updates"):
                advertising_notes = st.text_area(
                    "Add notes for advertising updates:",
                    value=st.session_state.get("advertising_notes", ""),
                    key="advertising_notes"
                )
                if advertising_notes:
                    st.success(f"📝 Notes Saved: {advertising_notes}")

        if website_tasks[i] == "Update the Wizards tab with ticketing":
            with st.expander("Details for Ticketing Updates"):
                ticketing_notes = st.text_area(
                    "Add notes for ticketing updates:",
                    value=st.session_state.get("ticketing_notes", ""),
                    key="ticketing_notes"
                )
                if ticketing_notes:
                    st.success(f"📝 Notes Saved: {ticketing_notes}")

        if website_tasks[i] == "Update the Wizards tab with sponsor page":
            with st.expander("Details for Sponsor Page Updates"):
                sponsor_page_notes = st.text_area(
                    "Add notes for sponsor page updates:",
                    value=st.session_state.get("sponsor_page_notes", ""),
                    key="sponsor_page_notes"
                )
                if sponsor_page_notes:
                    st.success(f"📝 Notes Saved: {sponsor_page_notes}")

    task_list_section("Website", website_tasks, special_inputs={task: website_special_inputs for task in website_tasks})
# -------------------------
# Mendon-Upton Dream Team Section
# -------------------------
if "dream_team_open" not in st.session_state:
    st.session_state.dream_team_open = False

if st.button("Mendon-Upton Dream Team - Target Dates ➡️ October through January"):
    st.session_state.dream_team_open = not st.session_state.dream_team_open

if st.session_state.dream_team_open:
    st.header("🏆 Mendon-Upton Dream Team")

    dream_team_tasks = [
        "T-shirts: Locate Vendor (e.g., Tommy the T-shirt guy @508-596-9925)", 
        "Secure artwork for T-shirts (front and back) that currently exsits in drive", 
        "Obtain any new artwork from corporate sponsors",
        "Get teacher bios and pictures and post to website"
    ]

    def dream_team_special_inputs(i):
        if dream_team_tasks[i] == "T-shirts: Get the t-shirt person (Tommy the T-shirt guy), secure artwork for t-shirts, get artwork from corporate sponsors":
            with st.expander("Details for T-shirts"):
                st.info("📞 Contact Tommy the T-shirt guy to secure artwork and finalize designs.")
                tshirt_notes = st.text_area(
                    "Add notes for T-shirts:",
                    value=st.session_state.get("tshirt_notes", ""),
                    key="tshirt_notes"
                )
                if tshirt_notes:
                    st.success(f"📝 Notes Saved: {tshirt_notes}")

        if dream_team_tasks[i] == "Get teacher bios and pictures, modify website blurb":
            with st.expander("Details for Teacher Bios and Website Blurb"):
                teacher_bios_notes = st.text_area(
                    "Add notes for teacher bios and website blurb:",
                    value=st.session_state.get("teacher_bios_notes", ""),
                    key="teacher_bios_notes"
                )
                if teacher_bios_notes:
                    st.success(f"📝 Notes Saved: {teacher_bios_notes}")

    task_list_section("DreamTeam", dream_team_tasks, special_inputs={task: dream_team_special_inputs for task in dream_team_tasks})


# -------------------------
# Volunteer Coordination Section
# -------------------------
if "vol_coord_open" not in st.session_state:
    st.session_state.vol_coord_open = False

if st.button("Volunteer Coordination - Target Dates ➡️ September through January"):
    st.session_state.vol_coord_open = not st.session_state.vol_coord_open
if st.session_state.vol_coord_open:
    st.markdown("## 🙋 Volunteer Coordination")
if st.session_state.vol_coord_open:
    # Volunteer Coordinator
    if "volunteer_coordinator" not in st.session_state:
        st.session_state.volunteer_coordinator = ""
    st.session_state.volunteer_coordinator = st.text_input("Who is the volunteer coordinator?", value=st.session_state.volunteer_coordinator)
    if st.session_state.volunteer_coordinator:
        st.info(f"👤 Volunteer Coordinator: {st.session_state.volunteer_coordinator}")

    vol_tasks = [
        "Recruit volunteers from all schools (e.g., Chris Evans @ NHS, Brian @ DECA)",
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

if st.button("Marketing / Communications  - Target Dates ➡️ November through January"):
    st.session_state.marketing_open = not st.session_state.marketing_open
if st.session_state.marketing_open:
    st.markdown("## 📣 Marketing / Communications")
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

if st.button("Ticketing / Sales / Finance- Target Dates ➡️ November"):
    st.session_state.finance_open = not st.session_state.finance_open

if st.session_state.finance_open:
    st.markdown("## 💵 Ticketing / Sales / Finance")

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

if st.button("Event Day Logistics - Game Day ➡️ Last Saturday in January"):
    st.session_state.eventday_open = not st.session_state.eventday_open

if st.session_state.eventday_open:
    st.markdown("## 🎪 Event Day Logistics")

    # Task description
    st.info(
        "📋 Event Day Tasks:\n"
        "- Set up the venue\n"
        "- Check AV equipment\n"
        "- Organize registration/check-in tables\n"
        "- Coordinate with volunteers for event flow\n"
        "- Manage food/beverage setup (Pizza, Gatorade, Snacks for players and volunteers)\n"
        "- Manage concessions\n"
        "- Ensure safety and first aid stations are ready\n"
        "- Cleanup after the event"
    )

    # Notes box for Event Day Logistics
    if "eventday_notes" not in st.session_state:
        st.session_state.eventday_notes = ""
    eventday_notes = st.text_area(
        "Add additional notes or tasks for Event Day Logistics:",
        value=st.session_state.eventday_notes,
        key="eventday_notes"
    )

    # Display saved notes
    if eventday_notes:
        st.session_state.eventday_notes = eventday_notes
        st.success(f"📝 Notes Saved: {eventday_notes}")

    # Close button for Event Day Logistics section
    if st.button("Close Event Day Logistics Section", key="close_eventday"):
        st.session_state.eventday_open = False




