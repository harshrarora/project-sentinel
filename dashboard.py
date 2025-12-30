import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Project Sentinel", layout="wide")
st.title("Project Sentinel")
st.subheader("Agentic IoT Defense System")

def load_json(file):
    if not os.path.exists(file):
        return None
    with open(file, "r") as f:
        return json.load(f)

scan = load_json("scan.json")
decisions = load_json("decisions.json")
events = load_json("events.json") or []

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# DEVICE INVENTORY
with col1:
    st.header("Device Inventory")
    if scan:
        for d in scan["devices"]:
            st.write(f"IP: {d['ip']}")
            st.write(f"MAC: {d['mac']}")
            st.divider()
    else:
        st.write("No scan data")

# AGENT DECISIONS
with col2:
    st.header("Agent Decisions")
    if decisions:
        st.write(f"Last Updated: {decisions['timestamp']}")
        for d in decisions["decisions"]:
            st.write(f"Target: {d['ip']}")
            st.write(f"Action: {d['action']}")
            st.write(f"Reason: {d['reason']}")
            st.divider()
    else:
        st.write("No decisions")

# DECEPTION STATUS
with col3:
    st.header("Deception Status")
    if events:
        st.write(f"Total attack attempts: {len(events)}")
        last = events[-1]
        st.write(f"Last attacker IP: {last['source_ip']}")
        st.write(f"Last state: {last['state']}")
    else:
        st.write("No attacks observed yet")

# LIVE ALERTS
with col4:
    st.header("Live Alerts")
    if events:
        first = datetime.fromisoformat(events[0]["timestamp"])
        last = datetime.fromisoformat(events[-1]["timestamp"])
        containment_time = (last - first).seconds

        st.write("Threat detected")
        st.write(f"Containment time: {containment_time} seconds")
        st.write("Status: CONTAINED")
    else:
        st.write("No active threats")

st.divider()
st.write("Status: OPERATIONAL")
