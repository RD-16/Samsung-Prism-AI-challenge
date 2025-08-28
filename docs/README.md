Project Overview

The User Behavior Monitoring System is a real-time monitoring and anomaly detection tool designed to track user interaction, detect unusual behavior, and provide system-level metrics. It combines rule-based and optional machine learning logic to flag deviations from predefined behavior baselines.

Objective:
1. Identify behavioral anomalies such as:
2. Excessive user actions
3. Login from unfamiliar IP addresses
4. Activity outside working hours
5. Extended user sessions
6. Provide a visual dashboard for monitoring and configuration.
The system is particularly useful for system administrators, cybersecurity teams, or developers who need real-time visibility into user behavior within an application or system.


Technical Stack
Programming Language-	Python 3.11 for	Core logic
UI Framework-Streamlit for Real-time dashboard interface
System Monitoring-psutil for CPU and performance tracking
Data Simulation-NumPy for Random user activity & stats
Data Handling-Pandas for Tabular data manipulation
Storage-JSON File for	Persistent storage for behavior baselines



Architecture
+----------------------------+
|    UserBehaviourAgent      |
|----------------------------|
| • Tracks actions           |
| • Logs IP and login time   |
| • CPU monitoring           |
| • Session time monitoring  |
| • Baseline comparison      |
| • Anomaly detection        |
| • Alerts generation        |
+----------------------------+
              |
              v
+----------------------------+
|   Streamlit Frontend UI    |
|----------------------------|
| • Charts & visualizations  |
| • Anomaly tables           |
| • Alerts and status logs   |
| • Baseline editor (sidebar)|
| • Current session metrics  |
+----------------------------+



Implementation Details
This file newfeatures.py defines the UserBehaviourAgent class which is the core component of the monitoring logic.
Key Functionalities:

1. __init__()
Initializes the agent, loads baseline configuration from a JSON file, and sets up internal variables for session tracking and alert management.
2.load_baseline() / save_baseline()
Reads or writes a JSON file (baseline.json) to configure: Allowed login hours, Max actions per minute, Known IP addresses
3.log_action(action_type)
Logs a user action with a timestamp and checks if the action rate exceeds the threshold.
4.monitor_system()
Called periodically to:Fetch current CPU usage, Check session duration, Detect anomalies, Compare behavior to baselines, Trigger alerts if deviations are detected,detect_anomaly(hour, cpu, action_rate)
5.send_alert(message)
Adds alerts to an internal list and prints them to the console (can be extended to send emails or logs).

Frontend(Streamlit)
This is the real-time dashboard that:
Visualizes simulated or real-time data
Displays user actions and session info
Tracks and shows triggered alerts
Lets users modify behavior baselines from the sidebar

Key Components:
Data Simulation
Generates synthetic activity using numpy to populate the dashboard.
Anomaly Detection
Identifies outliers using a simple statistical method: values that deviate beyond a threshold number of standard deviations.
Sidebar Settings
Users can set:
Allowed login hours via slider
Max allowed actions per minute
Add a known IP address
Live Status Monitoring
Shows current:IP address
Session duration
CPU usage
Time and login hour



Installation Instructions
Prerequisites:
Python 3.11
pip

Step-by-step:

Clone the Repository
git clone <your-repo-url>
cd <project-directory>
pip install -r requirements.txt
streamlit run dashboard.py
Open your browser to the Streamlit local address shown (e.g., http://localhost:8501)

User Guide
When You Launch the Dashboard:

The main area shows:
A line chart for activity values
A table of detected anomalies
System metrics and current status
A list of recent alerts
The sidebar displays:
Session duration
IP address
Editable baseline configuration (login hours, max actions/min, known IP)
A button to save new baseline settings

How to Use:

Let the dashboard simulate or monitor user actions.
Observe how metrics update every second.
If activity is abnormal (e.g., 20+ actions/min), alerts are triggered.
Adjust baseline settings from the sidebar as needed.
Review session duration and system usage continuously.

Salient Features

Real-time Monitoring: Constant observation of user behavior and system usage
Custom Alerts: Detects abnormal action rates, unknown IPs, and extended sessions
Session Tracking: Logs and monitors time since session started
IP Detection: Compares current IP to baseline
Anomaly Detection (Optional): Uses ML models for behavior analysis
Streamlit UI: Clean, responsive dashboard for admins
Baseline Persistence: Saves configuration across sessions using JSON
Simulated Data: Built-in random data generation for testing



Conclusion

This User Behavior Monitoring System provides a lightweight yet powerful way to monitor, visualize, and react to abnormal user behavior or system metrics. With real-time updates, customizable thresholds, and optional machine learning, it's well-suited for development, QA, or production environments requiring visibility into user actions.

End of Document
📄 To save as .docx, paste into Word or Google Docs and export accordingly.
