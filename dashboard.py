import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
from newfeatures import UserBehaviourAgent

# ------------------ CONFIG ------------------
st.set_page_config(page_title="User Behavior Monitor", layout="wide")
st.title("📊 Real-Time User Behavior Dashboard")

# ------------------ SESSION TRACKING ------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

session_duration = (datetime.now() - st.session_state.start_time).seconds
st.sidebar.metric("Session Duration (s)", session_duration)

# ------------------ DATA SIMULATION ------------------
@st.cache_data(ttl=10)
def generate_data():
    timestamps = pd.date_range(datetime.now(), periods=100, freq="S")
    actions = np.random.choice(["click", "scroll", "hover", "idle"], size=100)
    values = np.random.normal(loc=50, scale=10, size=100)
    df = pd.DataFrame({"timestamp": timestamps, "action": actions, "value": values})
    return df

data = generate_data()

# ------------------ ANOMALY DETECTION ------------------
def detect_anomalies(df, threshold=2.5):
    mean = df["value"].mean()
    std = df["value"].std()
    df["anomaly"] = np.abs(df["value"] - mean) > threshold * std
    return df

data = detect_anomalies(data)

# ------------------ DASHBOARD DISPLAY ------------------
st.subheader("📈 Activity Overview")
st.line_chart(data.set_index("timestamp")["value"])

st.subheader("🚨 Detected Anomalies")
anomalies = data[data["anomaly"]]
st.dataframe(anomalies, use_container_width=True)


# ------------------ LOGGING ------------------
st.sidebar.subheader("📝 Action Log")
st.sidebar.write(data[["timestamp", "action"]].tail(10))

agent=UserBehaviourAgent()
# ------------------ SESSION METRICS ------------------
session_duration = (pd.Timestamp.now() - pd.Timestamp(agent.session_start)).seconds
st.sidebar.metric("⏱ Session Duration (s)", session_duration)
st.sidebar.metric("📍 Current IP", agent.get_current_ip())


# ------------------ SYSTEM MONITOR ------------------
st.subheader("🖥️ System Status")
status = agent.monitor_system()
st.write(f"**Time:** {status['time']}")
st.write(f"**Hour:** {status['hour']}")
st.write(f"**CPU Usage (%):** {status['cpu']}")
st.write(f"**IP Address:** {status['ip']}")

# ------------------ ALERTS PANEL ------------------
st.subheader("🚨 Recent Alerts")
if status["alerts"]:
    for alert in status["alerts"]:
        st.warning(alert)
else:
    st.info("No alerts triggered yet.")



# ------------------ Baseline Editor ------------------
st.sidebar.subheader("⚙️ Baseline Settings")
login_hours = st.sidebar.slider("Allowed Login Hours", 0, 23, (8, 18))
max_actions = st.sidebar.number_input("Max Actions/Minute", value=15)
known_ip = st.sidebar.text_input("Known IP", value="127.0.0.1")

if st.sidebar.button("Update Baseline"):
    agent.baseline["login_hours"] = list(login_hours)
    agent.baseline["max_actions_per_minute"] = max_actions
    agent.baseline["known_locations"] = [known_ip]
    agent.save_baseline()
    st.sidebar.success("Baseline updated!")





