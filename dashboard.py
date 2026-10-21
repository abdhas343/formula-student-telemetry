
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import math
import time

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

# Start time for the online demo
if "demo_start_time" not in st.session_state:
    st.session_state.demo_start_time = time.time()


# Generate simulated telemetry when no CSV file exists
def generate_demo_data():

    elapsed = int(time.time() - st.session_state.demo_start_time)

    rows = []

    for t in range(elapsed + 1):

        # Simulated vehicle speed
        speed = max(
            0,
            45 + 25 * math.sin(t / 7) + 10 * math.sin(t / 2.5)
        )

        # Simulated battery consumption
        battery = max(0, 100 - t * 0.025)

        # Simulated battery temperature
        temperature = (
            30
            + 0.055 * t
            + 3 * math.sin(t / 12)
        )

        # Diagnostic status
        status = "WARNING" if temperature >= 60 else "OK"

        rows.append({
            "Time": t,
            "Speed": round(speed, 2),
            "Battery": round(battery, 2),
            "Temperature": round(temperature, 2),
            "Status": status
        })

    return pd.DataFrame(rows)


# Automatically refresh dashboard every second
@st.fragment(run_every="1s")
def live_dashboard():

    # Use local CSV data when available.
    # Otherwise, automatically activate online demo mode.
    if DATA_FILE.exists():

        try:
            df = pd.read_csv(DATA_FILE)

            if df.empty:
                df = generate_demo_data()
                demo_mode = True
            else:
                demo_mode = False

        except (pd.errors.EmptyDataError, OSError):
            df = generate_demo_data()
            demo_mode = True

    else:
        df = generate_demo_data()
        demo_mode = True

    if demo_mode:
        st.info("🟢 ONLINE DEMO MODE — Generating simulated telemetry automatically.")
    else:
        st.success("🟢 CSV TELEMETRY MODE — Reading simulator data.")

    # Ensure correct numeric data
    for column in ["Time", "Speed", "Battery", "Temperature"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(
        subset=["Time", "Speed", "Battery", "Temperature"]
    )

    df = df.sort_values("Time").reset_index(drop=True)

    if df.empty:
        st.warning("No valid telemetry measurements available.")
        return

    latest = df.iloc[-1]

    # Vehicle Dynamics: calculate acceleration
    df["Speed_ms"] = df["Speed"] / 3.6

    time_difference = df["Time"].diff().replace(0, float("nan"))

    df["Acceleration"] = (
        df["Speed_ms"].diff() / time_difference
    ).fillna(0)

    max_acceleration = df["Acceleration"].max()
    max_braking = df["Acceleration"].min()

    # Main telemetry metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "SPEED",
        f"{latest['Speed']:.1f} km/h"
    )

    col2.metric(
        "BATTERY",
        f"{latest['Battery']:.1f}%"
    )

    col3.metric(
        "TEMPERATURE",
        f"{latest['Temperature']:.1f} °C"
    )

    col4.metric(
        "SYSTEM STATUS",
        latest["Status"]
    )

    # Vehicle Dynamics Analysis
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

    st.plotly_chart(
        speed_chart,
        use_container_width=True
    )

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

    # Raw telemetry
    with st.expander("Raw Telemetry Data"):
        st.dataframe(
            df,
            use_container_width=True
        )


live_dashboard()
