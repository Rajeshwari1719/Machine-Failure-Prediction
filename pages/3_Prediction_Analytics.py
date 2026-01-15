import streamlit as st

st.title("🔮 Prediction & Analytics")

st.metric("Failure Probability (Next 24h)", "85 %")
st.metric("Remaining Useful Life (RUL)", "18 hours")

st.info("Confidence Interval: ± 3 hours")

st.subheader("🧠 AI Insights")
st.markdown("""
- Vibration trend increasing steadily  
- Current consumption above baseline  
- Temperature nearing safe threshold  
""")

st.subheader("📉 Historical Risk Trend")
st.line_chart([20, 35, 50, 65, 85])
