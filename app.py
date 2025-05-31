import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🔹 Set Page Config First
st.set_page_config(page_title="WellGuard+ Analyzer", layout="wide")

# 🔹 Apply Background Image (Update the file path!)
background_image = "background.jpg"  # Replace with the image file from your report/PPT
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{background_image}');
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ WellGuard+ | Intelligent Well Completion Analyzer")

# 🔹 Hourly Data Options
time_stamps = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00"]
pressure_options = {
    "00:00": [1200, 1000], "01:00": [1180, 1480], "02:00": [1150, 1500], "03:00": [1120, 9000],
    "04:00": [1100, 1300], "05:00": [1070, 1080], "06:00": [1050, 1450], "07:00": [1020, 1022],
    "08:00": [980, 990], "09:00": [750, 950]
}
temperature_options = {
    "00:00": [68, 67], "01:00": [69, 65], "02:00": [70, 62], "03:00": [71, 82], "04:00": [72, 83],
    "05:00": [73, 84], "06:00": [74, 64], "07:00": [75, 64], "08:00": [76, 86], "09:00": [77, 87]
}

# 🔹 User Input for Pressure & Temperature at Each Timestamp
selected_data = []
st.subheader("📊 Enter Hourly Pressure & Temperature Data")
for timestamp in time_stamps:
    st.markdown(f"**🕒 Timestamp: {timestamp}**")
    
    pressure_choice = st.selectbox(f"Select Pressure for {timestamp}", pressure_options[timestamp], key=f"pressure_{timestamp}")
    temperature_choice = st.selectbox(f"Select Temperature for {timestamp}", temperature_options[timestamp], key=f"temperature_{timestamp}")

    selected_data.append({"Timestamp": timestamp, "Pressure": pressure_choice, "Temperature": temperature_choice})

# 🔹 Convert Selections to DataFrame
df_selected = pd.DataFrame(selected_data)

# 🔹 Generate Graph AFTER Selections Are Made
if len(selected_data) == len(time_stamps):
    st.subheader("📊 Pressure & Temperature Trends Over Time")
    fig, ax = plt.subplots()
    ax.plot(df_selected["Timestamp"], df_selected["Pressure"], label="Pressure (psi)", color="blue", marker="o")
    ax.plot(df_selected["Timestamp"], df_selected["Temperature"], label="Temperature (°C)", color="red", marker="s")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Values")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 🔹 Admin Access Control: Show Logged Data Only for Admins
is_admin = st.checkbox("Admin Access")
if is_admin:
    st.subheader("🔍 Admin View: Logged Selections")
    st.dataframe(df_selected)
