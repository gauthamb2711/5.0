import streamlit as st
import psutil
import random
import pandas as pd
import time

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Thermal Monitoring Dashboard",
    page_icon="🔥",
    layout="wide"
)

st.title("📊 Thermal-Aware System Dashboard")

# -------------------------------
# Session State (to keep history)
# -------------------------------
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []
if "gpu_history" not in st.session_state:
    st.session_state.gpu_history = []
if "bat_history" not in st.session_state:
    st.session_state.bat_history = []

# -------------------------------
# Thermal Monitoring Module
# -------------------------------
def get_temperatures():
    """Simulate CPU, GPU, Battery temperature"""
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps['coretemp'][0].current if 'coretemp' in temps else random.randint(40, 70)
    except Exception:
        cpu_temp = random.randint(40, 70)

    gpu_temp = random.randint(35, 75)  # Simulated GPU temp
    bat_temp = random.randint(30, 60)  # Simulated battery temp
    return cpu_temp, gpu_temp, bat_temp

# -------------------------------
# Dynamic Task Scheduling Module
# -------------------------------
def schedule_tasks(cpu_temp, gpu_temp):
    """Simple scheduling logic based on temperature"""
    if cpu_temp > 70:
        return "⚠️ High CPU temp – throttling tasks"
    elif gpu_temp > 70:
        return "⚠️ High GPU temp – migrating tasks"
    else:
        return "✅ Normal load distribution"

# -------------------------------
# Thermal Feedback & Control Module
# -------------------------------
def feedback(cpu_temp, gpu_temp, bat_temp):
    alerts = []
    if cpu_temp > 75:
        alerts.append("🔥 CPU Overheating! Consider cooling")
    if gpu_temp > 75:
        alerts.append("🔥 GPU Overheating! Reduce graphics load")
    if bat_temp > 55:
        alerts.append("🔋 Battery hot! Stop charging")
    return alerts

# -------------------------------
# Streamlit Layout
# -------------------------------
placeholder = st.empty()
chart_placeholder = st.empty()

for _ in range(20):  # simulate 20 readings
    cpu_temp, gpu_temp, bat_temp = get_temperatures()

    # save history
    st.session_state.cpu_history.append(cpu_temp)
    st.session_state.gpu_history.append(gpu_temp)
    st.session_state.bat_history.append(bat_temp)

    # Task scheduling decision
    decision = schedule_tasks(cpu_temp, gpu_temp)

    # Alerts
    alerts = feedback(cpu_temp, gpu_temp, bat_temp)

    # Live data
    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ CPU Temp", f"{cpu_temp} °C")
        col2.metric("🎮 GPU Temp", f"{gpu_temp} °C")
        col3.metric("🔋 Battery Temp", f"{bat_temp} °C")

        st.info(decision)
        for a in alerts:
            st.error(a)

    # Plotting
    df = pd.DataFrame({
        "CPU": st.session_state.cpu_history,
        "GPU": st.session_state.gpu_history,
        "Battery": st.session_state.bat_history
    })
    chart_placeholder.line_chart(df)

    time.sleep(1)  # refresh every second