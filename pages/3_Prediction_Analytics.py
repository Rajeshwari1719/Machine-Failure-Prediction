import streamlit as st
import requests

st.set_page_config(page_title="Predictive Analysis", layout="wide")
st.title("📊 Predictive Analysis Dashboard")

# -----------------------------
# ThingSpeak Config
# -----------------------------
MACHINES = [
    {"name":"Exhaust Fan", "desc":"Industrial Exhaust Fan", "channel_id":"3225416", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"Refrigerator", "desc":"Industrial Refrigerator", "channel_id":"3225417", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"Washing Machine", "desc":"Industrial Washing Machine", "channel_id":"3225418", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"Oven", "desc":"Industrial Oven", "channel_id":"3225419", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"Air Conditioner", "desc":"Industrial AC", "channel_id":"3225420", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"CNC Mill #001", "desc":"CNC Milling Machine", "channel_id":"3225421", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"Hydraulic Pump #002", "desc":"Industrial Pump", "channel_id":"3225422", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"Electric Motor #003", "desc":"AC Induction Motor", "channel_id":"3225423", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"Air Compressor #004", "desc":"Rotary Screw Compressor", "channel_id":"3225424", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
    {"name":"Conveyor Belt #005", "desc":"Belt Conveyor System", "channel_id":"3225425", "fields":{"temp":1,"vibration":2,"current":3,"risk":4}},
]

READ_API_KEY = "HAQ25PJNNX3R0JCR"

# -----------------------------
# Helper Functions
# -----------------------------
def fetch_latest(channel_id, field_num):
    """Fetch latest field value from ThingSpeak."""
    try:
        url = f"https://api.thingspeak.com/channels/{channel_id}/fields/{field_num}.json?api_key={READ_API_KEY}&results=1"
        resp = requests.get(url, timeout=5).json()
        val = resp.get("feeds", [{}])[0].get(f"field{field_num}")
        ts = resp.get("feeds", [{}])[0].get("created_at")
        return float(val) if val else 0, ts
    except:
        return 0, "N/A"

def get_status_color(risk):
    if risk < 20:
        return "Healthy", "#4caf50"
    elif risk < 60:
        return "Warning", "#ff9800"
    else:
        return "Critical", "#f44336"

def generate_alerts(machine):
    alerts = []
    precautions = []

    # Example thresholds
    if machine['temp'] > 70:
        alerts.append("High Temperature!")
        precautions.append("Check cooling system and reduce load.")
    if machine['vibration'] > 5:
        alerts.append("High Vibration!")
        precautions.append("Inspect bearings and tighten loose parts.")
    if machine['current'] > 30:
        alerts.append("Over Current!")
        precautions.append("Check for short circuits or overloaded motors.")

    return alerts, precautions

# -----------------------------
# Fetch Data
# -----------------------------
fleet_data = []
for machine in MACHINES:
    temp, t_time = fetch_latest(machine["channel_id"], machine["fields"]["temp"])
    vib, v_time = fetch_latest(machine["channel_id"], machine["fields"]["vibration"])
    curr, c_time = fetch_latest(machine["channel_id"], machine["fields"]["current"])
    risk, r_time = fetch_latest(machine["channel_id"], machine["fields"]["risk"])
    status, color = get_status_color(risk)
    alerts, precautions = generate_alerts({"temp":temp, "vibration":vib, "current":curr})
    fleet_data.append({
        "name": machine["name"],
        "desc": machine["desc"],
        "temp": temp,
        "vibration": vib,
        "current": curr,
        "risk": risk,
        "status": status,
        "color": color,
        "last_updated": t_time or v_time or c_time or r_time,
        "alerts": alerts,
        "precautions": precautions
    })

# -----------------------------
# Display as Cards
# -----------------------------
st.markdown("<div style='display:flex; flex-wrap:wrap; gap:20px;'>", unsafe_allow_html=True)
for machine in fleet_data:
    alerts_html = "<br>".join([f"⚠️ {a}" for a in machine['alerts']]) or "No alerts"
    prec_html = "<br>".join([f"🛡 {p}" for p in machine['precautions']]) or "No precautions"
    
    st.markdown(f"""
    <div style='background:#1f1f23; padding:15px; border-radius:12px; width:350px;'>
        <h4 style='margin:0'>{machine['name']}</h4>
        <small style='color:#aaa'>{machine['desc']}</small>
        <span style='float:right; background:{machine['color']}; color:white; padding:3px 8px; border-radius:8px; font-size:12px;'>{machine['status']}</span>
        <div style='margin-top:10px; display:flex; justify-content:space-between;'>
            <div>🌡 {machine['temp']:.0f}°C</div>
            <div>🌊 {machine['vibration']:.1f} mm/s</div>
            <div>⚡ {machine['current']:.1f} A</div>
        </div>
        <div style='margin-top:10px; font-size:12px;'>Failure Risk: {machine['risk']}%</div>
        <div style='background:#333; border-radius:5px; width:100%; height:8px;'>
            <div style='width:{machine['risk']}%; background-color:{machine['color']}; height:8px; border-radius:5px;'></div>
        </div>
        <div style='font-size:12px; margin-top:5px; color:#ff9800;'>{alerts_html}</div>
        <div style='font-size:12px; margin-top:5px; color:#4caf50;'>{prec_html}</div>
        <div style='font-size:12px; mar Q1gin-top:5px; color:#aaa;'>Last updated: {machine['last_updated']}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
