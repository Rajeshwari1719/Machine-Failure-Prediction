import streamlit as st
from utils import fetch_realtime_data

st.set_page_config(page_title="Reports", layout="wide")
st.title("📑 Machine Reports")

df = fetch_realtime_data(results=200)

if df.empty:
    st.warning("⚠️ No data received from ThingSpeak.")
    st.stop()

st.subheader("Sensor Data Table")
st.dataframe(df, width="stretch")

# 🔽 EXCEL DOWNLOAD
st.subheader("⬇ Download Report")

excel_file = "machine_report.xlsx"
df.to_excel(excel_file, index=False)

with open(excel_file, "rb") as f:
    st.download_button(
        label="📥 Download Excel Report",
        data=f,
        file_name="machine_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
