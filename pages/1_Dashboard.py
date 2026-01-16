import streamlit as st
from utils import fetch_realtime_data

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Machine Health Dashboard")

df = fetch_realtime_data(field_num=1, results=50)

# 🛑 SAFETY CHECK
if df.empty or "value" not in df.columns:
    st.error("❌ No valid real-time data received from ThingSpeak")
    st.stop()

latest_temp = df["value"].iloc[-1]

# 🔍 STATUS LOGIC
if latest_temp < 60:
    status = "✅ Healthy"
elif latest_temp < 75:
    status = "⚠ Warning"
else:
    status = "❌ Failure Risk"

# 📊 KPIs (calculated dynamically)
uptime = max(90, 100 - (latest_temp - 50) * 0.4)
mtbf = max(100, 500 - latest_temp * 3)
mttr = min(6, 1 + latest_temp / 60)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Machine Status", status)
c2.metric("Uptime (%)", f"{uptime:.1f}")
c3.metric("MTBF (hrs)", f"{mtbf:.0f}")
c4.metric("MTTR (hrs)", f"{mttr:.1f}")

st.divider()

# 🚨 ALERTS
st.subheader("🚨 Active Alerts")

if latest_temp >= 75:
    st.error(f"🔥 Critical temperature: {latest_temp:.1f} °C")
elif latest_temp >= 60:
    st.warning(f"⚠ Elevated temperature: {latest_temp:.1f} °C")
else:
    st.success("✅ Machine operating normally")

# 📈 LIVE TREND
st.subheader("📈 Temperature Trend (Real-Time)")
st.line_chart(
    df.set_index("timestamp")["value"],
    width="stretch"
)
