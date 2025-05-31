import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🔹 Set Page Config First
st.set_page_config(page_title="WellGuard+ Analyzer", layout="wide")

st.title("🛡️ WellGuard+ | Intelligent Well Completion Analyzer")

# Load dataset
df = pd.read_csv("data/well_data.csv")

st.success("✅ Using preloaded dataset. Preview below:")
st.dataframe(df)

# 🔹 Completion Cost Estimation
completion_type = st.selectbox("Select Completion Type", ["Cased Hole", "Open Hole", "Hybrid"])
cost_mapping = {"Cased Hole": 2.5, "Open Hole": 1.8, "Hybrid": 3.2}  # Example cost multipliers
estimated_cost = cost_mapping[completion_type] * 1_000_000  # Example CAPEX scaling
st.write(f"💰 Estimated CAPEX for **{completion_type} Completion**: **${estimated_cost:,}**")

# 🔹 Microbial Corrosion Risk Check
if st.checkbox("Enable Microbial Corrosion Risk Alerts"):
    st.warning("⚠️ Hydrogen storage in porous media can trigger sulfate-reducing bacteria. Consider biocide treatment.")

# 🔹 Plot Pressure & Temperature Trends
fig, ax = plt.subplots()
ax.plot(df["pressure"], label="Pressure (psi)", color="blue")
ax.plot(df["temperature"], label="Temperature (°C)", color="red")
ax.set_xlabel("Well Data Entries")
ax.set_ylabel("Values")
ax.legend()
st.pyplot(fig)

# 🔹 Integrity Analysis
st.subheader("🧠 Integrity Analysis Results")
for i, row in df.iterrows():
    if row['gas_type'].lower() == "hydrogen":
        if row['material_type'].lower() != "13cr" and row['temperature'] > 70:
            st.error(f"⚠️ Row {i+2}: High risk of embrittlement — use CRA.")
        elif row['pressure'] < 1000:
            st.warning(f"🔻 Row {i+2}: Pressure drop detected. Check casing integrity.")
        else:
            st.success(f"✅ Row {i+2}: Conditions appear safe.")
