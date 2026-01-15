import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("⚙️ Machine Details")

time = pd.date_range(end=pd.Timestamp.now(), periods=30, freq="min")

df = pd.DataFrame({
    "Time": time,
    "Temperature (°C)": np.random.normal(45, 4, 30),
    "Vibration (mm/s)": np.random.normal(3.6, 0.7, 30),
    "Pressure (bar)": np.random.normal(6.1, 0.4, 30)
})

st.subheader("📈 Live Sensor Trends")
fig = px.line(df, x="Time", y=df.columns[1:])
st.plotly_chart(fig, use_container_width=True)

st.subheader("🛠 Maintenance Logs")
logs = pd.DataFrame({
    "Date": ["2026-01-05", "2025-12-18"],
    "Issue": ["Bearing wear", "Overheating"],
    "Action": ["Bearing replaced", "Motor cleaned"]
})
st.dataframe(logs, use_container_width=True)
