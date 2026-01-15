import streamlit as st

st.set_page_config(
    page_title="Machine Failure Prediction",
    page_icon="🛠️",
    layout="wide"
)

# -------- HEADER --------
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: 700;
}
.subtitle {
    font-size: 18px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛠️ Machine Failure Prediction System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">IoT • Digital Twin • AI Predictive Maintenance</div>', unsafe_allow_html=True)

st.divider()

# -------- INFO SECTION --------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Machine Status", "Healthy ✅")

with col2:
    st.metric("Failure Risk", "Low")

with col3:
    st.metric("Uptime", "99.2 %")

#st.info("⬅️ Use the left sidebar to navigate between dashboard sections.")