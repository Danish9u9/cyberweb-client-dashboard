import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(page_title="CyberWeb Labs | Client Dashboard", page_icon="🛡️")

def load_and_clean_data(file_path):
    """
    Loads sales data from CSV and performs cleaning operations:
    - Date format standardization
    - Numeric conversion for Sales
    - Mean imputation for missing values
    - Duplicate removal
    - Profit calculation feature engineering
    """
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)
    
    # Standardize data types
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    
    # Handle missing values and duplicates
    mean_sales = df['Sales'].mean()
    df['Sales'] = df['Sales'].fillna(mean_sales)
    
    df = df.drop_duplicates(subset='TransactionID', keep='first')

    # Feature Engineering: Calculate Profit (20% Margin)
    df['Profit'] = df['Sales'] * 0.20
    
    return df

# Main App Layout
st.title("🛡️ CyberWeb Labs Analytics")
st.subheader("Secure Sales Intelligence Dashboard")

# Sidebar
st.sidebar.header("Control Panel")
st.sidebar.info("System Status: Online 🟢")

# Data Loading
file_path = 'broken_sales.csv'
df = load_and_clean_data(file_path)

if df is not None:
    # Key Metrics Display
    total_sales = df['Sales'].sum()
    avg_sale = df['Sales'].mean()
    total_profit = df['Profit'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Avg Transaction", f"${avg_sale:,.2f}")

    st.divider()

    # Visualization Section
    st.write("### 📈 Sales Trend Analysis")
    st.line_chart(df.set_index('Date')['Sales'])

    # Raw Data Inspector
    if st.checkbox("Show Raw Database Records"):
        st.write(df)
        
else:
    st.error("⚠️ Data File Not Found. Please run the data generator script first.")