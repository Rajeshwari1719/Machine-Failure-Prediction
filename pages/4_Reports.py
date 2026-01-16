import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ------------------------------
# ThingSpeak configuration
# ------------------------------
MACHINES = {
    "Exhaust Fan": {"channel_id": "3225416", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "Refrigerator": {"channel_id": "3225417", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "Oven": {"channel_id": "3225418", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "Washing Machine": {"channel_id": "3225419", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "Air Conditioner": {"channel_id": "3225420", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "CNC Mill": {"channel_id": "3225421", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "Hydraulic Pump": {"channel_id": "3225422", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "Electric Motor": {"channel_id": "3225423", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "Conveyor Belt": {"channel_id": "3225424", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
    "CNC Lathe": {"channel_id": "3225425", "fields": {"temp":1, "vibration":2, "current":3, "risk":4}},
}

READ_API_KEY = "HAQ25PJNNX3R0JCR"

# ------------------------------
# Helper functions
# ------------------------------
def fetch_thingspeak(channel_id, field_num):
    """Fetch latest value from a ThingSpeak channel field safely"""
    url = f"https://api.thingspeak.com/channels/{channel_id}/fields/{field_num}.json?api_key={READ_API_KEY}&results=1"
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        feeds = data.get("feeds", [])
        if feeds and feeds[0].get(f"field{field_num}") is not None:
            return float(feeds[0][f"field{field_num}"]), feeds[0]["created_at"]
        else:
            return None, None
    except:
        return None, None

def get_status(risk):
    if risk is None:
        return "Unknown"
    if risk < 20:
        return "Healthy"
    elif risk < 60:
        return "Warning"
    else:
        return "Critical"

# ------------------------------
# Streamlit Page
# ------------------------------
st.set_page_config(page_title="Machine Reports", layout="wide")
st.title("📑 Machine Reports (Real-Time)")

# Collect data for all machines
report_data = []
for machine_name, config in MACHINES.items():
    temp, temp_time = fetch_thingspeak(config["channel_id"], config["fields"]["temp"])
    vibration, vib_time = fetch_thingspeak(config["channel_id"], config["fields"]["vibration"])
    current, curr_time = fetch_thingspeak(config["channel_id"], config["fields"]["current"])
    risk, risk_time = fetch_thingspeak(config["channel_id"], config["fields"]["risk"])
    
    # Latest timestamp among all fields
    timestamps = [t for t in [temp_time, vib_time, curr_time, risk_time] if t]
    last_updated = timestamps[0] if timestamps else "N/A"
    
    status = get_status(risk)
    
    report_data.append({
        "Machine": machine_name,
        "Temperature (°C)": temp if temp is not None else "N/A",
        "Vibration (mm/s)": vibration if vibration is not None else "N/A",
        "Current (A)": current if current is not None else "N/A",
        "Failure Risk (%)": int(risk) if risk is not None else "N/A",
        "Status": status,
        "Last Updated": last_updated
    })

# Convert to DataFrame
df_report = pd.DataFrame(report_data)

if df_report.empty:
    st.warning("⚠️ No real-time data available from ThingSpeak.")
    st.stop()

# Display table
st.subheader("Sensor Data Table")
st.dataframe(df_report, width="stretch")

# Download Excel
st.subheader("⬇ Download Real-Time Report")
excel_file = "machine_report.xlsx"
df_report.to_excel(excel_file, index=False)

with open(excel_file, "rb") as f:
    st.download_button(
        label="📥 Download Excel Report",
        data=f,
        file_name="machine_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
