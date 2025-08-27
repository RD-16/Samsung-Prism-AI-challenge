import streamlit as st
import pandas as pd
import numpy as np
import time
# agent.py
import json, socket, psutil, smtplib
from datetime import datetime, timedelta
from collections import deque
from sklearn.ensemble import IsolationForest
import platform

class UserBehaviourAgent:
    def __init__(self, baseline_file="baseline.json"):
        self.baseline_file = baseline_file
        self.load_baseline()
        self.alerts = []
        self.action_log = deque(maxlen=1000)
        self.session_start = datetime.now()
        self.model = None  # Load trained model if available

    def load_baseline(self):
        try:
            with open(self.baseline_file, "r") as f:
                self.baseline = json.load(f)
        except FileNotFoundError:
            self.baseline = {
                "login_hours": [8, 18],
                "max_actions_per_minute": 15,
                "known_locations": ["127.0.0.1"]
            }
            self.save_baseline()

    def save_baseline(self):
        with open(self.baseline_file, "w") as f:
            json.dump(self.baseline, f, indent=2)

    def get_current_ip(self):
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "Unknown"

    def log_action(self, action_type):
        now = datetime.now()
        self.action_log.append((now, action_type))
        self.check_action_rate(now)

    def check_action_rate(self, current_time):
        one_minute_ago = current_time - timedelta(minutes=1)
        recent_actions = [t for t, _ in self.action_log if t > one_minute_ago]
        if len(recent_actions) > self.baseline["max_actions_per_minute"]:
            self.send_alert(f"High action rate: {len(recent_actions)} actions/min")

    def check_session_duration(self):
        duration = datetime.now() - self.session_start
        if duration > timedelta(hours=5):
            self.send_alert(f"Long session detected: {duration}")

    def detect_anomaly(self, hour, cpu, action_rate):
        if self.model:
            score = self.model.predict([[hour, cpu, action_rate]])[0]
            if score == -1:
                self.send_alert("Anomaly detected by ML model")

    def monitor_system(self):
        now = datetime.now()
        hour = now.hour
        ip = self.get_current_ip()
        cpu = psutil.cpu_percent(interval=1)
        self.check_session_duration()
        self.check_action_rate(now)
        self.detect_anomaly(hour, cpu, len(self.action_log))

        if not (self.baseline["login_hours"][0] <= hour <= self.baseline["login_hours"][1]):
            self.send_alert(f"Abnormal login hour: {hour}:00")

        if ip not in self.baseline["known_locations"]:
            self.send_alert(f"Login from unknown IP: {ip}")

        return {
            "time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": hour,
            "ip": ip,
            "cpu": cpu,
            "alerts": self.alerts[-5:]
        }

    def send_alert(self, message):
        alert_message = f"[ALERT] {message}"
        print(alert_message)
        self.alerts.append(alert_message)

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







