import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CyberWeb Labs | Client Dashboard", page_icon="🛡️")

# --- THE CLEANING FUNCTION (Our "Secret Sauce") ---
def load_and_clean_data(file_path):
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)
    
    # 1. Fix Dates
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
    
    # 2. Fix Sales (Numeric Conversion)
    # Note: We assign it back to the column!
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    
    # 3. Handle Missing Sales (Impute with Mean)
    mean_sales = df['Sales'].mean()
    df['Sales'] = df['Sales'].fillna(mean_sales)
    
    # 4. Remove Duplicates
    df = df.drop_duplicates(subset='TransactionID', keep='first')
    
    return df

# --- THE APP LAYOUT ---
st.title("🛡️ CyberWeb Labs Analytics")
st.subheader("Secure Sales Intelligence Dashboard")

# Sidebar for "Client" Controls
st.sidebar.header("Control Panel")
st.sidebar.info("System Status: Online 🟢")

# Load the Data
file_path = 'broken_sales.csv'
df = load_and_clean_data(file_path)

if df is not None:
    # METRICS ROW (The "Executive Summary")
    total_sales = df['Sales'].sum()
    avg_sale = df['Sales'].mean()
    
    col1, col2 = st.columns(2)
    col1.metric("Total Revenue", f"${total_sales:,.2f}")
    col2.metric("Average Transaction", f"${avg_sale:,.2f}")

    st.divider()

    # CHART SECTION
    st.write("### 📈 Sales Trend Analysis")
    # Streamlit has built-in charts. Simple and fast.
    st.line_chart(df.set_index('Date')['Sales'])

    # RAW DATA TOGGLE
    if st.checkbox("Show Raw Database Records"):
        st.write(df)
        
else:
    st.error("⚠️ Data File Not Found. Please run the data generator script first.")