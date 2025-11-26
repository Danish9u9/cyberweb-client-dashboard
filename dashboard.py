import streamlit as st
import pandas as pd
import os

# --- Application Configuration ---
st.set_page_config(
    page_title="CyberWeb Labs | Client Dashboard",
    page_icon="🛡️",
    layout="wide"
)

class DashboardApp:
    """
    Main application class for the Sales Intelligence Dashboard.
    Encapsulates data processing and UI rendering logic.
    """
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None

    def load_data(self):
        """
        Ingests and processes raw sales data.
        Performs cleaning, type casting, and feature engineering (Profit).
        """
        if not os.path.exists(self.data_path):
            st.error(f"⚠️ Data Source Not Found: {self.data_path}")
            return False

        try:
            raw_data = pd.read_csv(self.data_path)
            
            # Data Cleaning Pipeline
            raw_data['Date'] = pd.to_datetime(raw_data['Date'], format='mixed', errors='coerce')
            raw_data['Sales'] = pd.to_numeric(raw_data['Sales'], errors='coerce')
            
            # Imputation & Deduplication
            raw_data['Sales'] = raw_data['Sales'].fillna(raw_data['Sales'].mean())
            self.df = raw_data.drop_duplicates(subset='TransactionID', keep='first')

            # Feature Engineering: Profit Calculation (20% Margin Assumption)
            self.df['Profit'] = self.df['Sales'] * 0.20
            
            return True
        except Exception as e:
            st.error(f"Data Processing Error: {str(e)}")
            return False

    def render_sidebar(self):
        """Renders the sidebar controls."""
        with st.sidebar:
            st.header("Control Panel")
            st.success("System Status: Online 🟢")
            st.markdown("---")
            st.caption("© 2025 CyberWeb Labs")

    def render_metrics(self):
        """Displays the top-level KPI metrics."""
        if self.df is None: return

        total_sales = self.df['Sales'].sum()
        total_profit = self.df['Profit'].sum()
        avg_transaction = self.df['Sales'].mean()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Revenue", f"${total_sales:,.2f}")
        c2.metric("Net Profit (Est.)", f"${total_profit:,.2f}", delta="20% Margin")
        c3.metric("Avg. Transaction", f"${avg_transaction:,.2f}")

    def render_charts(self):
        """Visualizes the sales trends."""
        if self.df is None: return

        st.divider()
        st.subheader("📈 Sales Trend Analysis")
        
        # Time-series chart
        chart_data = self.df.set_index('Date')['Sales']
        st.line_chart(chart_data, height=350)

    def render_raw_data(self):
        """Optional raw data inspector."""
        if self.df is None: return
        
        with st.expander("View Raw Database Records"):
            st.dataframe(self.df, use_container_width=True)

    def run(self):
        """Main execution flow."""
        st.title("🛡️ CyberWeb Labs Analytics")
        st.markdown("### Secure Sales Intelligence Dashboard")
        
        self.render_sidebar()
        
        if self.load_data():
            self.render_metrics()
            self.render_charts()
            self.render_raw_data()

# --- Entry Point ---
if __name__ == "__main__":
    # Initialize and run the dashboard with the target dataset
    app = DashboardApp('broken_sales.csv')
    app.run()
