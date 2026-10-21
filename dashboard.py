
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="FS Live Telemetry",
    page_icon="🏎️",
    layout="wide"
)

# Custom racing design
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #FFFFFF;
}

[data-testid="stMetric"] {
    background-color: #1C2530;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #303B49;
}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ FS / LIVE TELEMETRY")
st.caption("Electric Race Car Monitoring System | Simulated Data")

DATA_FILE = Path(__file__).resolve().parent / "data" / "live_telemetry.csv"

# Automatically refresh this section every second
@st.fragment(run_every="1s")
def live_dashboard():

    if not DATA_FILE.exists():
        st.info("Waiting for simulator.py to start...")
        return

    try:
        df = pd.read_csv(DATA_FILE)
    except (pd.errors.EmptyDataError, OSError):
        st.info("Waiting for telemetry data...")
        return

    if df.empty:
        st.info("Waiting for first measurement...")
        return

    latest = df.iloc[-1]
    
    # Vehicle Dynamics: calculate acceleration
    df["Speed_ms"] = df["Speed"] / 3.6

    df["Acceleration"] = (
        df["Speed_ms"].diff() / df["Time"].diff()
    ).fillna(0)

    max_acceleration = df["Acceleration"].max()
    max_braking = df["Acceleration"].min()


    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("SPEED", f"{latest['Speed']} km/h")
    col2.metric("BATTERY", f"{latest['Battery']:.1f}%")
    col3.metric("TEMPERATURE", f"{latest['Temperature']:.1f} °C")
    col4.metric("SYSTEM STATUS", latest["Status"])

    
    st.subheader("Vehicle Dynamics Analysis")

    dyn1, dyn2 = st.columns(2)

    dyn1.metric(
        "MAX ACCELERATION",
        f"{max_acceleration:.2f} m/s²"
    )

    dyn2.metric(
        "MAX BRAKING",
        f"{max_braking:.2f} m/s²"
    )

    st.divider()


    # Interactive charts
    speed_chart = px.line(
        df,
        x="Time",
        y="Speed",
        title="Vehicle Speed",
        markers=True
    )

    temperature_chart = px.line(
        df,
        x="Time",
        y="Temperature",
        title="Battery Temperature"
    )

    battery_chart = px.line(
        df,
        x="Time",
        y="Battery",
        title="Battery Consumption"
    )

    speed_chart.update_layout(template="plotly_dark")
    temperature_chart.update_layout(template="plotly_dark")
    battery_chart.update_layout(template="plotly_dark")

    st.plotly_chart(speed_chart, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.plotly_chart(
            temperature_chart,
            use_container_width=True
        )

    with col_b:
        st.plotly_chart(
            battery_chart,
            use_container_width=True
        )

    # Warning system
    st.subheader("System Diagnostics")

    if latest["Status"] == "WARNING":
        st.error("⚠️ HIGH BATTERY TEMPERATURE")
    else:
        st.success("All systems operating normally.")

    with st.expander("Raw Telemetry Data"):
        st.dataframe(df, use_container_width=True)

live_dashboard()
