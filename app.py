# app.py
# 🎮 A/B Test + Funnel Drop-off Visualization (Google Sheets Integration)

import streamlit as st
import pandas as pd
import uuid
import random
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="🧪 A/B Game Tutorial", layout="centered")

st.title("🎮 Product Analytics A/B Testing Simulation")

# ---- GOOGLE SHEETS CONNECTION ----
SHEET_NAME = "abtest_results"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1aWCy6RQeCQbSx7wDlA0M-ibHBNEZ2cU-nj8QJIGgQZY/edit?gid=0#gid=0"  # ⬅️ Replace with your sheet URL

# Define Google Sheets credentials scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# Open the Google Sheet
try:
    sheet = client.open_by_url(SPREADSHEET_URL).worksheet("Sheet1")
except gspread.WorksheetNotFound:
    sheet = client.open_by_url(SPREADSHEET_URL).add_worksheet(title="Sheet1", rows="1000", cols="10")
    sheet.append_row(["user_id", "group", "step_install", "step_tutorial", "step_reward", "step_purchase", "timestamp"])

# ---- STUDENT FLOW ----
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]
    st.session_state.group = random.choice(["A", "B"])

user_id = st.session_state.user_id
group = st.session_state.group

st.info(f"You are in **Group {group}** (User ID: {user_id})")

# Progress tracker
if "progress" not in st.session_state:
    st.session_state.progress = {
        "install": False,
        "tutorial": False,
        "reward": False,
        "purchase": False
    }

# Step 1: Install
st.header("Step 1: Install the Game")
if not st.session_state.progress["install"]:
    if st.button("📲 Install Now"):
        st.session_state.progress["install"] = True
        st.success("Game installed successfully!")
        st.balloons()

# Step 2: Tutorial
if st.session_state.progress["install"] and not st.session_state.progress["tutorial"]:
    st.header("Step 2: Complete the Tutorial")

    if group == "A":
        st.write("🧭 Welcome hero! Press start to learn your first move.")
        if st.button("▶️ Start Training"):
            st.session_state.progress["tutorial"] = True
            st.success("✅ Tutorial complete! You’ve mastered the basics.")
            st.snow()
    else:
        st.write("🧙 Choose your mentor to begin your training:")
        mentor = st.radio("Pick your guide:", ["⚔️ Warrior", "🏹 Archer", "🧙 Mage"])
        if st.button("✅ Begin Training"):
            st.session_state.progress["tutorial"] = True
            st.success(f"🎯 {mentor} training complete!")
            st.snow()

# Step 3: Reward (Group A only)
if group == "A" and st.session_state.progress["tutorial"] and not st.session_state.progress["reward"]:
    st.header("Step 3: Claim Your Reward")
    if st.button("🎁 Claim 100 Coins"):
        st.session_state.progress["reward"] = True
        st.success("💰 Reward collected! Visit the shop.")
        st.balloons()

# Step 4: Purchase
if st.session_state.progress["tutorial"] and (group == "B" or st.session_state.progress["reward"]) and not st.session_state.progress["purchase"]:
    st.header("Step 4: Make Your First Purchase")

    if group == "A":
        if st.button("🗡️ Buy Sword (5 coins)"):
            st.session_state.progress["purchase"] = True
            st.success("🗡️ Sword purchased! You’re ready for adventure!")
            st.balloons()
    else:
        st.write("Choose your weapon:")
        choice = st.selectbox("Weapon:", ["🗡️ Sword (5 coins)", "🏹 Bow (7 coins)", "🔮 Staff (10 coins)"])
        if st.button("🛒 Confirm Purchase"):
            st.session_state.progress["purchase"] = True
            st.success(f"{choice} purchased successfully!")
            st.balloons()

# Step 5: Summary
if st.session_state.progress["purchase"]:
    st.header("🏆 Mission Complete!")
    st.write("You’ve finished the onboarding experience.")
    st.progress(100)

# ---- LOG DATA TO GOOGLE SHEETS ----
if st.session_state.progress["install"]:
    row = [
        user_id,
        group,
        int(st.session_state.progress["install"]),
        int(st.session_state.progress["tutorial"]),
        int(st.session_state.progress.get("reward", False)),
        int(st.session_state.progress["purchase"]),
        datetime.now().isoformat()
    ]
    sheet.append_row(row)
