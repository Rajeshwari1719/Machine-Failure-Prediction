import streamlit as st

st.title("📊 Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Machine Status", "⚠ Warning")
c2.metric("Uptime", "96.8 %")
c3.metric("MTBF", "410 hrs")
c4.metric("MTTR", "3.1 hrs")

st.divider()

st.subheader("🚨 Active Alerts")
st.warning("High vibration detected – inspection recommended")
st.error("Temperature approaching critical limit")

st.subheader("📌 System Summary")
st.markdown("""
- Machine operating with increased vibration  
- Failure risk detected within next 24 hours  
- Preventive maintenance advised  
""")
