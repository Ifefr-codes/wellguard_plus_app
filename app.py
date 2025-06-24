import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 🔹 Read secrets
PASSCODE = st.secrets.get("admin_passcode", "")

# 🔹 Set Page Config
st.set_page_config(page_title="WellGuard+ Analyzer", layout="wide")

st.title("🛡️ WellGuard+ | Group 1 Well Completion Analyzer")

# 🔹 Apply Background Image Styling (Ensuring Proper Detection)
bg_path = "background.png"
if os.path.exists(bg_path):
    st.image(bg_path, use_container_width=True)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("background.png") no-repeat center center fixed;
            background-size: 25% auto;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning(f"⚠️ Background image not found. Ensure '{bg_path}' is in your project folder.")

# 🔹 Hourly Data Options (User Must Manually Select Values)
time_stamps = [f"{i:02d}:00" for i in range(10)]
pressure_options = {ts: ["Select a value...", low, high] for ts, (low, high) in zip(
    time_stamps,
    [(1200,1000),(1180,1480),(1150,1500),(1120,9000),(1100,1300),(1070,1080),(1050,1450),(1020,1022),(980,990),(750,950)]
)}
temperature_options = {ts: ["Select a value...", t1, t2] for ts, (t1, t2) in zip(
    time_stamps,
    [(68,67),(69,65),(70,62),(71,82),(72,83),(73,84),(74,64),(75,64),(76,86),(77,87)]
)}
material_options = ["Select a material...", "Steel", "Composite", "Ceramic"]

# 🔹 Sidebar Form for Data Entry
with st.sidebar.form("input_form"):
    st.subheader("📊 Enter Hourly Pressure, Temperature & Material Data")
    selected_data = []
    for timestamp in time_stamps:
        st.markdown(f"**🕒 {timestamp}**")
        p = st.selectbox(f"Pressure for {timestamp}", pressure_options[timestamp], key=f"pressure_{timestamp}")
        t = st.selectbox(f"Temperature for {timestamp}", temperature_options[timestamp], key=f"temperature_{timestamp}")
        m = st.selectbox(f"Material Type for {timestamp}", material_options, key=f"material_{timestamp}")
        selected_data.append({"Timestamp": timestamp, "Pressure": p, "Temperature": t, "Material": m})
    submitted = st.form_submit_button("Run Analysis")

# 🔹 Convert Selections to DataFrame
if submitted:
    df_selected = pd.DataFrame(selected_data)

    # Only proceed if all values are selected
    if not df_selected.isin(["Select a value...", "Select a material..."]).any().any():
        st.subheader("📊 Pressure & Temperature Trends Over Time")
        fig, ax = plt.subplots()
        ax.plot(df_selected["Timestamp"], df_selected["Pressure"], label="Pressure (psi)", marker="o")
        ax.plot(df_selected["Timestamp"], df_selected["Temperature"], label="Temperature (°C)", marker="s")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Values")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # 🔹 Integrity Analysis
        st.subheader("🛠️ Integrity Analysis")
        avg_pressure = df_selected["Pressure"].mean()
        avg_temperature = df_selected["Temperature"].mean()
        st.write(f"✅ **Average Pressure:** {avg_pressure:.2f} psi")
        st.write(f"✅ **Average Temperature:** {avg_temperature:.2f} °C")
        if avg_pressure > 2000 or avg_temperature > 85:
            st.warning("⚠️ **Potential Risk: Extreme conditions detected! Review mitigation strategies.**")
        else:
            st.success("✅ **Integrity Stable: No critical risks detected.**")

        # 🔹 Material Suggestions
        st.subheader("📌 Material Selection Review")
        unsuit = df_selected[df_selected["Material"].isin(["Ceramic"])]
        if not unsuit.empty:
            st.warning("⚠️ Some selected materials may be unsuitable for high-pressure environments.")
            st.write("🔹 **Recommended Alternative:** Steel or Composite for enhanced durability.")
    else:
        st.error("Please select a real value for every field before running analysis.")

# 🔹 Admin Access Control
st.subheader("🔐 Admin Access")
admin_input = st.text_input("Enter Admin Passcode:", type="password")
if admin_input and PASSCODE and admin_input == PASSCODE:
    st.success("✅ Access Granted: Viewing Admin Data")
    st.dataframe(df_selected if 'df_selected' in locals() else pd.DataFrame())
elif admin_input:
    st.warning("🔒 **Access Denied. Enter correct Passcode.**")
