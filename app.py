
import streamlit as st
import pandas as pd

st.set_page_config(page_title="WellGuard+ Analyzer", layout="wide")
st.title("🛡️ WellGuard+ | Intelligent Well Completion Analyzer")

uploaded_file = st.file_uploader("📤 Upload Your Well Data (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
    st.success("✅ File uploaded successfully. Preview below:")
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

else:
    st.info("👆 Upload a CSV file to begin integrity analysis.")
