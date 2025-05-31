import streamlit as st
import pandas as pd

st.set_page_config(page_title="WellGuard+ Analyzer", layout="wide")
st.title("🛡️ WellGuard+ | Intelligent Well Completion Analyzer")

# Load dataset automatically
df = pd.read_csv("data/well_data.csv")

st.success("✅ Using preloaded dataset. Preview below:")
st.dataframe(df)

# 🔹 Dropdown for Material Type Selection
material_type = st.selectbox("Select Material Type", df['material_type'].unique())

# 🔹 Dropdown for Gas Type Selection
gas_type = st.selectbox("Select Gas Type", df['gas_type'].unique())

# 🔹 Slider for Temperature Selection
temperature = st.slider("Select Temperature (°C)", int(df["temperature"].min()), int(df["temperature"].max()), int(df["temperature"].mean()))

# 🔹 Slider for Pressure Selection
pressure = st.slider("Select Minimum Pressure (psi)", int(df["pressure"].min()), int(df["pressure"].max()), int(df["pressure"].mean()))

# 🔹 Checkbox for Casing Integrity Check
casing_check = st.checkbox("Show only wells with casing integrity issues")

# 🔹 Apply Filters to Dataset
filtered_df = df[
    (df["material_type"] == material_type) &
    (df["gas_type"] == gas_type) &
    (df["temperature"] <= temperature) &
    (df["pressure"] >= pressure)
]

# Apply casing integrity filter if selected
if casing_check:
    filtered_df = filtered_df[filtered_df["pressure"] < 1000]  # Example condition

st.write("🔍 Filtered Well Data Based on Selection")
st.dataframe(filtered_df)

# 🔹 Add Downloadable Report Feature
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_well_data.csv", "text/csv", key="download-csv")
