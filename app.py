import streamlit as st
import pandas as pd

st.set_page_config(page_title="WellGuard+ Analyzer", layout="wide")
st.title("🛡️ WellGuard+ | Intelligent Well Completion Analyzer")

# 🔹 Load dataset automatically—no file upload needed
df = pd.read_csv("data/well_data.csv")

st.success("✅ Using preloaded dataset. Preview below:")
st.dataframe(df)

st.subheader("🧠 Integrity Analysis Results")
for i, row in df.iterrows():
    if row['gas_type'].lower() == "hydrogen":
        if row['material_type'].lower() != "13cr" and row['temperature'] > 70:
            st.error(f"Row {i+2}: ⚠️ High risk of embrittlement — use CRA instead of {row['material_type']}")
        elif row['pressure'] < 1000:
            st.warning(f"Row {i+2}: 🔻 Pressure drop detected. Check for casing integrity.")
        else:
            st.success(f"Row {i+2}: ✅ Conditions appear safe.")
    else:
        st.info(f"Row {i+2}: ℹ️ Gas type '{row['gas_type']}' — no hydrogen-specific risk.")

# 🔹 Allow users to select specific rows dynamically
selected_row = st.selectbox("Select a well entry for analysis", df.index)
selected_data = df.loc[selected_row]

st.write("🔍 Selected Well Data for Analysis")
st.write(selected_data)
