import streamlit as st
import pandas as pd

st.set_page_config(page_title="WellGuard+ Analyzer", layout="wide")
st.title("🛡️ WellGuard+ | Intelligent Well Completion Analyzer")

# Load dataset automatically
df = pd.read_csv("data/well_data.csv")

st.success("✅ Using preloaded dataset. Preview below:")
st.dataframe(df)

# 🔹 Dropdown for Material Type Selection
material_type = st.selectbox("Select Material Type", df["material_type"].unique())

# 🔹 Dropdown for Gas Type Selection
gas_type = st.selectbox("Select Gas Type", df["gas_type"].unique())

# 🔹 Slider for Temperature Selection
temperature = st.slider("Select Temperature (°C)", min_value=int(df["temperature"].min()), max_value=int(df["temperature"].max()), value=int(df["temperature"].mean()))

# 🔹 Filter Dataset Based on User Input
filtered_df = df[(df["material_type"] == material_type) & (df["gas_type"] == gas_type) & (df["temperature"] <= temperature)]
st.write("🔍 Filtered Well Data Based on Selection")
st.dataframe(filtered_df)

