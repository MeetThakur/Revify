import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import os


def getFilteredData(
    file_path,
    gender=None,
    age=None,
    units_sold=None,
    price=None,
    item_type=None,
    city=None,
    discount_applied=None,
    return_status=None,
    date_of_purchase=None,
    payment_method=None
):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None

    # Convert 'Date of Purchase' to datetime (DD-MM-YYYY format)
    if 'date_of_purchase' in df.columns:
        df['date_of_purchase'] = pd.to_datetime(df['date_of_purchase'], format='%d-%m-%Y', errors='coerce')

    if gender is not None:
        df = df[df['gender'] == gender]

    if age is not None:
        try:
            min_age, max_age = map(float, age.split('-'))
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
            df = df.dropna(subset=['age'])
            df = df[(df['age'] >= min_age) & (df['age'] <= max_age)]
        except Exception as e:
            print(f"Invalid age range: {age}. Error: {e}")

    if units_sold is not None:
        try:
            min_units, max_units = map(float, units_sold.split('-'))
            df['units_sold'] = pd.to_numeric(df['units_sold'], errors='coerce')
            df = df.dropna(subset=['units_sold'])
            df = df[(df['units_sold'] >= min_units) & (df['units_sold'] <= max_units)]
        except Exception as e:
            print(f"Invalid units sold range: {units_sold}. Error: {e}")

    if price is not None:
        try:
            min_price, max_price = map(float, price.split('-'))
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df = df.dropna(subset=['price'])
            df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
        except Exception as e:
            print(f"Invalid price range: {price}. Error: {e}")

    if item_type is not None:
        df = df[df['item_type'] == item_type]

    if city is not None:
        df = df[df['city'] == city]

    if discount_applied is not None:
        df = df[df['discount_applied'] == discount_applied]

    if return_status is not None:
        df = df[df['return_status'] == return_status]

    if date_of_purchase is not None:
        # Handle date range filter if the input is in the format "start_date to end_date"
        try:
            if 'to' in date_of_purchase:
                start_date, end_date = date_of_purchase.split(' to ')
                start_date = pd.to_datetime(start_date, format='%d-%m-%Y')
                end_date = pd.to_datetime(end_date, format='%d-%m-%Y')
                df = df[(df['date_of_purchase'] >= start_date) & (df['date_of_purchase'] <= end_date)]
            else:
                # Exact date match
                date_value = pd.to_datetime(date_of_purchase, format='%d-%m-%Y')
                df = df[df['date_of_purchase'] == date_value]
        except Exception as e:
            print(f"Invalid date range: {date_of_purchase}. Error: {e}")

    if payment_method is not None:
        df = df[df['payment_method'] == payment_method]

    # Show filtered result
    print("\nFiltered Dataset:")
    print(df)

    # Calculate and display total profit
    if 'profit' in df.columns:
        df['profit'] = pd.to_numeric(df['profit'], errors='coerce').fillna(0)
        total_profit = df['profit'].sum()
        print(f"\nTotal Profit for filtered data: {total_profit}")
    else:
        print("\n'Profit' column not found in the dataset.")

    return df



# Set page configuration
st.set_page_config(
    page_title="Revify",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    /* Color Variables */
    :root {
        --pastel-blue: #A7C7E7;
        --pastel-green: #C1E1C1;
        --pastel-pink: #FFB6C1;
        --pastel-purple: #D8BFD8;
        --pastel-yellow: #FFE4B5;
        --pastel-orange: #FFDAB9;
        --pastel-mint: #B5EAD7;
        --pastel-lavender: #E6E6FA;
        --text-dark: #4A4A4A;
        --text-light: #6B7280;
        --white: #FFFFFF;
        --shadow: rgba(0, 0, 0, 0.05);
    }

    /* Main Layout */
    .main {
        padding: 2rem;
        background: linear-gradient(180deg, var(--pastel-lavender) 0%, var(--white) 100%);
    }
    
    /* Metrics Styling */
    .stMetric {
        background-color: var(--white);
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 4px var(--shadow);
        border: 1px solid var(--pastel-lavender);
        transition: transform 0.2s;
    }
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px var(--shadow);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: var(--white);
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        color: var(--text-light);
        font-weight: 500;
        transition: all 0.2s;
        border: 1px solid var(--pastel-lavender);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--pastel-lavender);
        color: var(--text-dark);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--pastel-blue);
        color: var(--text-dark);
        border-color: var(--pastel-blue);
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: var(--pastel-blue);
        color: var(--text-dark);
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: var(--pastel-purple);
        box-shadow: 0 2px 4px var(--shadow);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: var(--white);
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px var(--shadow);
    }
    .sidebar .sidebar-content {
        background-color: var(--white);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div {
        background-color: var(--white);
        border-radius: 0.5rem;
        border: 1px solid var(--pastel-lavender);
    }
    
    /* File Uploader Styling */
    .stFileUploader > div {
        background-color: var(--white);
        border-radius: 0.5rem;
        border: 2px dashed var(--pastel-blue);
        padding: 2rem;
        transition: all 0.2s;
    }
    .stFileUploader > div:hover {
        border-color: var(--pastel-purple);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background-color: var(--white);
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px var(--shadow);
        padding: 1rem;
    }
    
    /* Chart Containers */
    .stPlotlyChart {
        background-color: var(--white);
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: 0 2px 4px var(--shadow);
    }
    
    /* Section Headers */
    .stSubheader {
        color: var(--pastel-blue);
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--pastel-lavender);
    }
    
    /* Info Messages */
    .stInfo {
        background-color: var(--pastel-mint);
        border-radius: 0.5rem;
        padding: 1rem;
        border: 1px solid var(--pastel-green);
    }
    
    /* Success Messages */
    .stSuccess {
        background-color: var(--pastel-green);
        border-radius: 0.5rem;
        padding: 1rem;
        border: 1px solid var(--pastel-mint);
    }
    
    /* Error Messages */
    .stError {
        background-color: var(--pastel-pink);
        border-radius: 0.5rem;
        padding: 1rem;
        border: 1px solid var(--pastel-orange);
    }
    
    /* Feature Boxes */
    .feature-box {
        background-color: var(--white);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px var(--shadow);
        border: 1px solid var(--pastel-lavender);
        transition: transform 0.2s;
    }
    .feature-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px var(--shadow);
    }
    
    /* Welcome Section */
    .welcome-section {
        text-align: center;
        padding: 3rem 2rem;
        background-color: var(--white);
        border-radius: 1rem;
        box-shadow: 0 4px 6px var(--shadow);
        margin: 2rem 0;
    }
    
    /* CTA Box */
    .cta-box {
        background: linear-gradient(135deg, var(--pastel-blue) 0%, var(--pastel-purple) 100%);
        color: var(--text-dark);
        padding: 2.5rem;
        border-radius: 1rem;
        margin: 2rem auto;
        text-align: center;
        max-width: 800px;
        box-shadow: 0 4px 6px var(--shadow);
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background-color: var(--white);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid var(--pastel-lavender);
    }
    
    /* Multiselect */
    .stMultiSelect > div {
        background-color: var(--white);
        border-radius: 0.5rem;
        border: 1px solid var(--pastel-lavender);
    }
    
    /* Date Input */
    .stDateInput > div {
        background-color: var(--white);
        border-radius: 0.5rem;
        border: 1px solid var(--pastel-lavender);
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background-color: var(--pastel-green);
        color: var(--text-dark);
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stDownloadButton > button:hover {
        background-color: var(--pastel-mint);
        box-shadow: 0 2px 4px var(--shadow);
    }

    /* Hide Streamlit's default footer */
    footer {visibility: hidden;}
    
    /* Hide Streamlit's default menu button */
    #MainMenu {visibility: hidden;}
    
    /* Improve spacing in sidebar */
    .css-1d391kg {
        padding: 1.5rem;
    }
    
    /* Add subtle hover effect to all interactive elements */
    .stButton > button,
    .stSelectbox > div,
    .stMultiSelect > div,
    .stDateInput > div,
    .stRadio > div {
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover,
    .stSelectbox > div:hover,
    .stMultiSelect > div:hover,
    .stDateInput > div:hover,
    .stRadio > div:hover {
        box-shadow: 0 2px 4px var(--shadow);
    }
    
    /* Improve table readability */
    .stDataFrame {
        font-size: 0.9rem;
    }
    
    .stDataFrame th {
        background-color: var(--pastel-lavender) !important;
        font-weight: 600 !important;
    }
    
    /* Add subtle animation to success messages */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stSuccess {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* Improve chart tooltips */
    .js-plotly-plot .plotly .main-svg {
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for data
if 'data' not in st.session_state:
    st.session_state.data = None

# Load data getFilteredDataction
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load sample data getFilteredDataction
@st.cache_data
def load_sample_data():
    try:
        # Create sample data
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        n_records = len(dates)
        
        data = {
            'Date': dates,
            'Gender': np.random.choice(['Male', 'Female'], n_records),
            'Age': np.random.randint(18, 70, n_records),
            'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_records),
            'ItemType': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], n_records),
            'Price': np.random.uniform(10, 1000, n_records).round(2),
            'UnitsSold': np.random.randint(1, 10, n_records),
            'Payment': np.random.choice(['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet'], n_records),
            'Return': np.random.choice(['Returned', 'Not Returned'], n_records, p=[0.1, 0.9]),
            'Discount': np.random.choice(['Yes', 'No'], n_records, p=[0.2, 0.8]),
            'Feedback': np.random.uniform(1, 5, n_records).round(1)
        }
        
        df = pd.DataFrame(data)
        df['Profit'] = (df['Price'] * df['UnitsSold'] * 0.3).round(2)  # 30% profit margin
        return df
    except Exception as e:
        st.error(f"Error loading sample data: {e}")
        return None

# Forecasting getFilteredDataction
def forecast_sales(data, days_to_forecast=30, metric='Price'):
    # Prepare data
    data = data.sort_values('Date')
    X = np.array(range(len(data))).reshape(-1, 1)
    y = data[metric].values
    
    # Create polynomial features
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    
    # Fit model
    model = LinearRegression()
    model.fit(X_poly, y)
    
    # Generate future dates
    last_date = data['Date'].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=days_to_forecast)
    
    # Predict
    future_X = np.array(range(len(data), len(data) + days_to_forecast)).reshape(-1, 1)
    future_X_poly = poly.transform(future_X)
    predictions = model.predict(future_X_poly)
    
    return future_dates, predictions

# Main app
st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #1f77b4;'>📊 Revify</h1>", unsafe_allow_html=True)

# Add a button to reset/upload new data in the sidebar
if st.session_state.data is not None:
    if st.sidebar.button("Upload New Data"):
        st.session_state.data = None
        st.rerun()

# File upload section
if st.session_state.data is None:
    st.markdown("""
        <div class="info-box">
            <h2 style='text-align: center; color: #1f77b4;'>Welcome to Revify</h2>
            <p style='text-align: center; font-size: 1.2rem; color: #666;'>Your intelligent sales analytics companion, transforming raw data into actionable business insights.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 What Revify Does")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <div class="feature-title">📈 Real-time Analytics</div>
                <div class="feature-description">Get instant insights into your sales performance with dynamic, interactive dashboards.</div>
            </div>
            <div class="feature-box">
                <div class="feature-title">🔮 Smart Forecasting</div>
                <div class="feature-description">Leverage machine learning to predict future sales trends and make data-driven decisions.</div>
            </div>
            <div class="feature-box">
                <div class="feature-title">👥 Customer Intelligence</div>
                <div class="feature-description">Understand your customer base through detailed demographic analysis and behavior insights.</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-box">
                <div class="feature-title">📊 Product Performance</div>
                <div class="feature-description">Track which products are driving your business and optimize your product strategy.</div>
            </div>
            <div class="feature-box">
                <div class="feature-title">🎯 Customizable Views</div>
                <div class="feature-description">Create personalized dashboards that focus on the metrics that matter most to your business.</div>
            </div>
            <div class="feature-box">
                <div class="feature-title">⚡ Instant Insights</div>
                <div class="feature-description">Get immediate answers to your business questions with our intuitive interface.</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### ✨ Why Choose Revify")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <div class="feature-title">🎨 User-Friendly</div>
                <div class="feature-description">No technical expertise required - just upload your data and start exploring.</div>
            </div>
            <div class="feature-box">
                <div class="feature-title">📊 Comprehensive Analysis</div>
                <div class="feature-description">From basic metrics to advanced forecasting, all the tools you need in one place.</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-box">
                <div class="feature-title">📈 Interactive Visualizations</div>
                <div class="feature-description">Engage with your data through dynamic charts and graphs that make complex information easy to understand.</div>
            </div>
            <div class="feature-box">
                <div class="feature-title">🔍 Flexible Filtering</div>
                <div class="feature-description">Drill down into specific aspects of your business with powerful filtering capabilities.</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="cta-box">
            <h2 style='color: white; margin-bottom: 1rem;'>Ready to transform your sales data?</h2>
            <p style='color: white; font-size: 1.2rem;'>Upload your CSV file or try our sample data to get started!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create a container with max-width
    st.markdown("""
        <div style='max-width: 600px; margin: 0 auto;'>
            <div style='text-align: center;'>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    st.markdown("""
            </div>
            <div style='text-align: center; margin-top: 1rem;'>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Load Sample Data", use_container_width=True):
        df = load_sample_data()
        if df is not None:
            st.session_state.data = df
            st.success("Sample data loaded successfully!")
            st.balloons()
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.session_state.data = df
            st.success("Data loaded successfully!")
            st.balloons()
            st.rerun()

# Show dashboard if data is loaded
if st.session_state.data is not None:
    df = st.session_state.data
    
    # Sidebar filters
    st.sidebar.title("Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [df['Date'].min(), df['Date'].max()]
    )
    
    # Gender filter with "All" option and multiple selection
    gender_options = ['All'] + list(df['Gender'].unique())
    gender_filter = st.sidebar.multiselect(
        "Select Gender (can select multiple)",
        options=gender_options,
        default=['All']
    )
    if 'All' in gender_filter:
        gender_filter = df['Gender'].unique()
    
    # City filter with "All" option and multiple selection
    city_options = ['All'] + list(df['City'].unique())
    city_filter = st.sidebar.multiselect(
        "Select City (can select multiple)",
        options=city_options,
        default=['All']
    )
    if 'All' in city_filter:
        city_filter = df['City'].unique()

    # Item Type filter with "All" option and multiple selection
    item_type_options = ['All'] + list(df['ItemType'].unique())
    item_type_filter = st.sidebar.multiselect(
        "Select Item Type (can select multiple)",
        options=item_type_options,
        default=['All']
    )
    if 'All' in item_type_filter:
        item_type_filter = df['ItemType'].unique()

    # Price range filter
    min_price = float(df['Price'].min())
    max_price = float(df['Price'].max())
    price_range = st.sidebar.slider(
        "Price Range",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )

    # Age range filter
    min_age = int(df['Age'].min())
    max_age = int(df['Age'].max())
    age_range = st.sidebar.slider(
        "Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

    # Apply filters
    mask = (
        (df['Date'].dt.date >= date_range[0]) &
        (df['Date'].dt.date <= date_range[1]) &
        (df['Gender'].isin(gender_filter)) &
        (df['City'].isin(city_filter)) &
        (df['ItemType'].isin(item_type_filter)) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['Age'] >= age_range[0]) &
        (df['Age'] <= age_range[1])
    )
    filtered_df = df[mask]

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Sales",
            f"${filtered_df['Price'].sum():,.2f}",
            f"{((filtered_df['Price'].sum() / df['Price'].sum() - 1) * 100):,.1f}%"
        )
    
    with col2:
        st.metric(
            "Total Profit",
            f"${filtered_df['Profit'].sum():,.2f}",
            f"{((filtered_df['Profit'].sum() / df['Profit'].sum() - 1) * 100):,.1f}%"
        )
    
    with col3:
        st.metric(
            "Units Sold",
            f"{filtered_df['UnitsSold'].sum():,}",
            f"{((filtered_df['UnitsSold'].sum() / df['UnitsSold'].sum() - 1) * 100):,.1f}%"
        )
    
    with col4:
        st.metric(
            "Average Feedback",
            f"{filtered_df['Feedback'].mean():.1f}",
            f"{((filtered_df['Feedback'].mean() / df['Feedback'].mean() - 1) * 100):,.1f}%"
        )

    # Additional Overview Metrics
    st.subheader("Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Payment Type Distribution
        payment_total = filtered_df.groupby('Payment')['Price'].sum()
        top_payment = payment_total.idxmax()
        st.metric(
            "Top Payment Method",
            top_payment,
            f"${payment_total[top_payment]:,.2f}"
        )
    
    with col2:
        # Return Rate
        return_rate = (filtered_df['Return'] == 'Returned').mean() * 100
        st.metric(
            "Return Rate",
            f"{return_rate:.1f}%",
            f"{((return_rate - (df['Return'] == 'Returned').mean() * 100)):,.1f}%"
        )
    
    with col3:
        # Average Order Value
        aov = filtered_df['Price'].mean()
        st.metric(
            "Average Order Value",
            f"${aov:,.2f}",
            f"{((aov / df['Price'].mean() - 1) * 100):,.1f}%"
        )
    
    with col4:
        # Discount Rate
        discount_rate = (filtered_df['Discount'] == 'Yes').mean() * 100
        st.metric(
            "Discount Rate",
            f"{discount_rate:.1f}%",
            f"{((discount_rate - (df['Discount'] == 'Yes').mean() * 100)):,.1f}%"
        )

    # Sales and Profit over time (separate charts)
    st.subheader("Sales and Profit Analysis")
    
    # Sales over time
    daily_sales = filtered_df.groupby('Date').agg({
        'Price': 'sum',
        'UnitsSold': 'sum'
    }).reset_index()
    
    fig_sales = go.Figure()
    fig_sales.add_trace(go.Scatter(
        x=daily_sales['Date'],
        y=daily_sales['Price'],
        name='Sales',
        mode='lines+markers',
        line=dict(color='#1f77b4', width=2)
    ))
    fig_sales.update_layout(
        title='Daily Sales Over Time',
        xaxis_title='Date',
        yaxis_title='Sales Amount ($)',
        height=400,
        showlegend=True,
        hovermode='x unified'
    )
    st.plotly_chart(fig_sales, use_container_width=True)
    
    # Profit over time
    daily_profit = filtered_df.groupby('Date').agg({
        'Profit': 'sum'
    }).reset_index()
    
    fig_profit = go.Figure()
    fig_profit.add_trace(go.Scatter(
        x=daily_profit['Date'],
        y=daily_profit['Profit'],
        name='Profit',
        mode='lines+markers',
        line=dict(color='#2ca02c', width=2)
    ))
    fig_profit.update_layout(
        title='Daily Profit Over Time',
        xaxis_title='Date',
        yaxis_title='Profit Amount ($)',
        height=400,
        showlegend=True,
        hovermode='x unified'
    )
    st.plotly_chart(fig_profit, use_container_width=True)

    # Sales and Profit Summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Total Sales",
            f"${daily_sales['Price'].sum():,.2f}",
            f"Daily Avg: ${daily_sales['Price'].mean():,.2f}"
        )
    
    with col2:
        st.metric(
            "Total Profit",
            f"${daily_profit['Profit'].sum():,.2f}",
            f"Daily Avg: ${daily_profit['Profit'].mean():,.2f}"
        )

    # Distribution Charts
    st.subheader("Distribution Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by city
        fig_city = px.bar(
            filtered_df.groupby('City')['Price'].sum().reset_index(),
            x='City',
            y='Price',
            title='Sales by City'
        )
        st.plotly_chart(fig_city, use_container_width=True)
        
        # Sales by gender
        fig_gender = px.pie(
            filtered_df,
            names='Gender',
            values='Price',
            title='Sales by Gender'
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    with col2:
        # Sales by item type
        fig_item = px.bar(
            filtered_df.groupby('ItemType')['Price'].sum().reset_index(),
            x='ItemType',
            y='Price',
            title='Sales by Item Type'
        )
        st.plotly_chart(fig_item, use_container_width=True)
        
        # Payment method distribution
        fig_payment = px.pie(
            filtered_df,
            names='Payment',
            values='Price',
            title='Sales by Payment Method'
        )
        st.plotly_chart(fig_payment, use_container_width=True)

    # Additional insights
    st.subheader("Additional Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        # Return rate analysis
        returns_data = filtered_df.groupby('Return')['Price'].sum().reset_index()
        fig_returns = px.pie(
            returns_data,
            names='Return',
            values='Price',
            title='Sales by Return Status'
        )
        st.plotly_chart(fig_returns, use_container_width=True)

    with col2:
        # Discount analysis
        discount_data = filtered_df.groupby('Discount')['Price'].sum().reset_index()
        fig_discount = px.pie(
            discount_data,
            names='Discount',
            values='Price',
            title='Sales by Discount Status'
        )
        st.plotly_chart(fig_discount, use_container_width=True)

    # Create tabs for different views
    tab1, tab2 = st.tabs(["Advanced Analytics", "Comparison View"])
    
    with tab1:
        st.subheader("Advanced Analytics")
        
        # Create tabs for different types of analysis
        analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs(["Sales Analysis", "Customer Analysis", "Product Analysis"])
        
        with analysis_tab1:
            st.write("### 📈 Sales Analysis")
            
            # Sales Forecasting
            st.write("#### Sales Forecasting")
            col1, col2 = st.columns(2)
            
            with col1:
                days_to_forecast = st.slider("Days to Forecast", 7, 90, 30)
                forecast_metric = st.selectbox(
                    "Select Metric to Forecast",
                    ['Price', 'UnitsSold', 'Profit']
                )
            
            # Prepare data for forecasting
            daily_sales = filtered_df.groupby('Date')[forecast_metric].sum().reset_index()
            future_dates, predictions = forecast_sales(daily_sales, days_to_forecast, forecast_metric)
            
            # Create forecast plot
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(
                x=daily_sales['Date'],
                y=daily_sales[forecast_metric],
                name='Historical Data',
                mode='lines+markers'
            ))
            fig_forecast.add_trace(go.Scatter(
                x=future_dates,
                y=predictions,
                name='Forecast',
                mode='lines',
                line=dict(dash='dash')
            ))
            fig_forecast.update_layout(
                title=f'{forecast_metric} Forecast',
                xaxis_title='Date',
                yaxis_title=forecast_metric
            )
            st.plotly_chart(fig_forecast, use_container_width=True)

            # Sales Trends
            st.write("#### Sales Trends")
            trend_metric = st.selectbox(
                "Select Metric for Trend Analysis",
                ['Price', 'UnitsSold', 'Profit']
            )
            
            # Calculate moving averages
            daily_data = filtered_df.groupby('Date')[trend_metric].sum().reset_index()
            daily_data['7_day_MA'] = daily_data[trend_metric].rolling(window=7).mean()
            daily_data['30_day_MA'] = daily_data[trend_metric].rolling(window=30).mean()
            
            fig_trend = px.line(
                daily_data,
                x='Date',
                y=[trend_metric, '7_day_MA', '30_day_MA'],
                title=f'{trend_metric} Trends with Moving Averages'
            )
            st.plotly_chart(fig_trend, use_container_width=True)

            # Sales Distribution
            st.write("#### Sales Distribution")
            fig_dist = px.histogram(
                filtered_df,
                x=trend_metric,
                nbins=50,
                title=f'Distribution of {trend_metric}'
            )
            st.plotly_chart(fig_dist, use_container_width=True)

        with analysis_tab2:
            st.write("### 👥 Customer Analysis")
            
            # Customer Segmentation
            st.write("#### Customer Segmentation")
            col1, col2 = st.columns(2)
            
            with col1:
                # Age groups
                filtered_df['AgeGroup'] = pd.cut(
                    filtered_df['Age'],
                    bins=[0, 25, 35, 45, 55, 100],
                    labels=['0-25', '26-35', '36-45', '46-55', '55+']
                )
                age_group_sales = filtered_df.groupby('AgeGroup')['Price'].sum()
                fig_age_group = px.bar(
                    age_group_sales.reset_index(),
                    x='AgeGroup',
                    y='Price',
                    title='Sales by Age Group'
                )
                st.plotly_chart(fig_age_group, use_container_width=True)
            
            with col2:
                # Payment method preference by age group
                payment_by_age = filtered_df.groupby(['AgeGroup', 'Payment'])['Price'].sum().reset_index()
                fig_payment_age = px.bar(
                    payment_by_age,
                    x='AgeGroup',
                    y='Price',
                    color='Payment',
                    title='Payment Method Preference by Age Group'
                )
                st.plotly_chart(fig_payment_age, use_container_width=True)

            # Customer Behavior Analysis
            st.write("#### Customer Behavior Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                # Return rate by age group
                returns_by_age = filtered_df.groupby(['AgeGroup', 'Return'])['Price'].count().reset_index()
                fig_returns_age = px.bar(
                    returns_by_age,
                    x='AgeGroup',
                    y='Price',
                    color='Return',
                    title='Return Rate by Age Group'
                )
                st.plotly_chart(fig_returns_age, use_container_width=True)
            
            with col2:
                # Feedback distribution by age group
                feedback_by_age = filtered_df.groupby('AgeGroup')['Feedback'].mean().reset_index()
                fig_feedback_age = px.bar(
                    feedback_by_age,
                    x='AgeGroup',
                    y='Feedback',
                    title='Average Feedback by Age Group'
                )
                st.plotly_chart(fig_feedback_age, use_container_width=True)

        with analysis_tab3:
            st.write("### 📦 Product Analysis")
            
            # Product Performance
            st.write("#### Product Performance")
            col1, col2 = st.columns(2)
            
            with col1:
                # Sales by item type
                item_sales = filtered_df.groupby('ItemType')['Price'].sum().sort_values(ascending=False)
                fig_item_sales = px.bar(
                    item_sales.reset_index(),
                    x='ItemType',
                    y='Price',
                    title='Sales by Item Type'
                )
                st.plotly_chart(fig_item_sales, use_container_width=True)
            
            with col2:
                # Profit margin by item type
                item_profit = filtered_df.groupby('ItemType')['Profit'].sum().sort_values(ascending=False)
                fig_item_profit = px.bar(
                    item_profit.reset_index(),
                    x='ItemType',
                    y='Profit',
                    title='Profit by Item Type'
                )
                st.plotly_chart(fig_item_profit, use_container_width=True)

            # Product Metrics
            st.write("#### Product Metrics")
            metrics_data = filtered_df.groupby('ItemType').agg({
                'Price': ['sum', 'mean'],
                'UnitsSold': ['sum', 'mean'],
                'Profit': ['sum', 'mean'],
                'Feedback': 'mean'
            }).round(2)
            
            metrics_data.columns = ['_'.join(col).strip() for col in metrics_data.columns.values]
            st.dataframe(metrics_data.style.format("{:.2f}"))

            # Product Trends
            st.write("#### Product Trends")
            trend_item = st.selectbox(
                "Select Item Type for Trend Analysis",
                filtered_df['ItemType'].unique()
            )
            
            item_trend = filtered_df[filtered_df['ItemType'] == trend_item].groupby('Date')['Price'].sum().reset_index()
            fig_item_trend = px.line(
                item_trend,
                x='Date',
                y='Price',
                title=f'Sales Trend for {trend_item}'
            )
            st.plotly_chart(fig_item_trend, use_container_width=True)

    with tab2:
        st.subheader("Comparison View")
        
        # Comparison settings
        col1, col2 = st.columns(2)
        
        with col1:
            # Select comparison metrics
            comparison_metrics = st.multiselect(
                "Select Metrics to Compare",
                ['Price', 'UnitsSold', 'Profit', 'Feedback'],
                default=['Price', 'Profit']
            )
            
            # Select comparison type
            comparison_type = st.radio(
                "Select Comparison Type",
                ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Heat Map']
            )
        
        with col2:
            # Select comparison dimensions
            comparison_dimensions = st.multiselect(
                "Select Dimensions to Compare",
                ['Gender', 'City', 'ItemType', 'Payment', 'AgeGroup'],
                default=['Gender', 'City']
            )
            
            # Select aggregation method
            aggregation_method = st.selectbox(
                "Select Aggregation Method",
                ['sum', 'mean', 'median', 'count']
            )

        # Create comparison visualizations
        if comparison_metrics and comparison_dimensions:
            st.write("### 📊 Comparison Analysis")
            
            # Time-based comparison
            st.write("#### Time Series Comparison")
            time_data = filtered_df.groupby('Date')[comparison_metrics].agg(aggregation_method).reset_index()
            fig_time = px.line(
                time_data,
                x='Date',
                y=comparison_metrics,
                title=f'Time Series Comparison of {", ".join(comparison_metrics)}'
            )
            st.plotly_chart(fig_time, use_container_width=True)

            # Dimension-based comparison
            st.write("#### Dimension Comparison")
            
            if comparison_type == 'Bar Chart':
                # Create grouped bar chart
                for dimension in comparison_dimensions:
                    dim_data = filtered_df.groupby(dimension)[comparison_metrics].agg(aggregation_method).reset_index()
                    fig_dim = px.bar(
                        dim_data,
                        x=dimension,
                        y=comparison_metrics,
                        title=f'{dimension} Comparison',
                        barmode='group'
                    )
                    st.plotly_chart(fig_dim, use_container_width=True)
            
            elif comparison_type == 'Line Chart':
                # Create line chart
                for dimension in comparison_dimensions:
                    dim_data = filtered_df.groupby(dimension)[comparison_metrics].agg(aggregation_method).reset_index()
                    fig_dim = px.line(
                        dim_data,
                        x=dimension,
                        y=comparison_metrics,
                        title=f'{dimension} Comparison',
                        markers=True
                    )
                    st.plotly_chart(fig_dim, use_container_width=True)
            
            elif comparison_type == 'Scatter Plot':
                # Create scatter plot matrix
                fig_scatter = px.scatter_matrix(
                    filtered_df,
                    dimensions=comparison_metrics,
                    color=comparison_dimensions[0] if comparison_dimensions else None,
                    title='Scatter Plot Matrix'
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            elif comparison_type == 'Heat Map':
                # Create heat map
                for dimension in comparison_dimensions:
                    pivot_data = filtered_df.pivot_table(
                        values=comparison_metrics[0],
                        index=dimension,
                        columns=comparison_metrics[1] if len(comparison_metrics) > 1 else None,
                        agggetFilteredDatac=aggregation_method
                    )
                    fig_heat = px.imshow(
                        pivot_data,
                        title=f'Heat Map: {dimension} vs {comparison_metrics[0]}',
                        color_continuous_scale='RdBu'
                    )
                    st.plotly_chart(fig_heat, use_container_width=True)

            # Statistical Summary
            st.write("### 📈 Statistical Summary")
            summary_data = filtered_df[comparison_metrics].describe()
            st.dataframe(summary_data.style.format("{:.2f}"))

            # Performance Metrics
            st.write("### 🎯 Performance Metrics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                for metric in comparison_metrics:
                    st.metric(
                        f"Total {metric}",
                        f"{filtered_df[metric].sum():,.2f}",
                        f"{((filtered_df[metric].sum() / df[metric].sum() - 1) * 100):,.1f}%"
                    )
            
            with col2:
                for metric in comparison_metrics:
                    st.metric(
                        f"Average {metric}",
                        f"{filtered_df[metric].mean():,.2f}",
                        f"{((filtered_df[metric].mean() / df[metric].mean() - 1) * 100):,.1f}%"
                    )
            
            with col3:
                for metric in comparison_metrics:
                    st.metric(
                        f"Median {metric}",
                        f"{filtered_df[metric].median():,.2f}",
                        f"{((filtered_df[metric].median() / df[metric].median() - 1) * 100):,.1f}%"
                    )

        else:
            st.info("Please select at least one metric and dimension to view comparisons.")

    # Data table with sorting and filtering
    st.subheader("Detailed Data")
    st.dataframe(
        filtered_df.style.format({
            'Price': '${:,.2f}',
            'Profit': '${:,.2f}',
            'Feedback': '{:.1f}'
        }),
        use_container_width=True
    )

    # Download button for filtered data
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )
