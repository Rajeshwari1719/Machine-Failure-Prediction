import streamlit as st
import pandas as pd
import tempfile
from datetime import datetime
from utils import fetch_realtime_data

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Reports", layout="wide")

# ----------------- AUTH CHECK -----------------
#if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
 #  st.stop()

# ----------------- TITLE -----------------
st.title("📄 Reports & Maintenance History")
st.caption("Live machine data → predictive reports")

# ----------------- FETCH REAL-TIME DATA -----------------
df = fetch_realtime_data(results=200)

if df.empty:
    st.error("No live data available.")
    st.stop()

# ----------------- FEATURE ENGINEERING -----------------
df["risk"] = (
    (df["temperature"] / 100) * 0.4 +
    (df["vibration"] / 10) * 0.3 +
    (df["current"] / 50) * 0.3
) * 100

df["risk"] = df["risk"].clip(0, 100)

# ----------------- SUMMARY METRICS -----------------
st.subheader("📊 Live System Summary")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Temperature", f"{df['temperature'].mean():.1f} °C")
c2.metric("Avg Vibration", f"{df['vibration'].mean():.2f} mm/s")
c3.metric("Avg Current", f"{df['current'].mean():.1f} A")
c4.metric("Avg Risk", f"{df['risk'].mean():.1f} %")

# ----------------- DATA TABLE -----------------
st.subheader("📑 Raw Live Data")
st.dataframe(df.tail(50), use_container_width=True)

# ----------------- EXPORT FUNCTIONS -----------------
def generate_excel(live_df):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    live_df.to_excel(temp_file.name, index=False)
    return temp_file.name

def generate_csv(live_df):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    live_df.to_csv(temp_file.name, index=False)
    return temp_file.name

# ----------------- EXPORT SECTION -----------------
st.subheader("📥 Export Live Reports")

col1, col2 = st.columns(2)

with col1:
    if st.button("⬇️ Export Excel", use_container_width=True):
        excel_path = generate_excel(df)
        with open(excel_path, "rb") as f:
            st.download_button(
                "📊 Download Excel Report",
                f,
                file_name=f"machine_report_{datetime.now().date()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with col2:
    if st.button("⬇️ Export CSV", use_container_width=True):
        csv_path = generate_csv(df)
        with open(csv_path, "rb") as f:
            st.download_button(
                "📄 Download CSV Report",
                f,
                file_name=f"machine_report_{datetime.now().date()}.csv",
                mime="text/csv",
                use_container_width=True
            )

# ----------------- FOOTER -----------------
st.markdown("---")
st.caption("Generated from real-time IoT sensor data")
