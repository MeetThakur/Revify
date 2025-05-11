 # Revify

Revify is an intelligent sales analytics dashboard built with Streamlit. It transforms raw sales data into actionable business insights through interactive visualizations, advanced analytics, and smart forecasting.

## Features

- **Real-time Analytics:** Instant insights into sales performance with dynamic dashboards.
- **Smart Forecasting:** Machine learning-based predictions for future sales trends.
- **Customer Intelligence:** Demographic and behavioral analysis of your customer base.
- **Product Performance:** Track and optimize product strategy.
- **Customizable Views:** Personalized dashboards and flexible filtering.
- **Interactive Visualizations:** Engaging charts and graphs for easy data exploration.
- **Comparison View:** Compare metrics and dimensions with various chart types.
- **Downloadable Data:** Export filtered data as CSV.

## Getting Started

### Prerequisites
- Python 3.8+
- Recommended: Create a virtual environment

### Installation
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
Start the Streamlit app with:
```bash
streamlit run app.py
```

The dashboard will open in your browser. You can upload your own CSV sales data or use the provided sample data.

## Data Format
Your CSV file should have columns similar to:
- `Date` (YYYY-MM-DD)
- `Gender`
- `Age`
- `City`
- `ItemType`
- `Price`
- `UnitsSold`
- `Payment`
- `Return`
- `Discount`
- `Feedback`
- `Profit`

## Usage
- **Upload Data:** Use the sidebar to upload your CSV or load sample data.
- **Filter Data:** Apply filters for date, gender, city, item type, price, and age.
- **View Metrics:** See key sales, profit, and customer metrics at a glance.
- **Explore Visualizations:** Analyze sales, profit, product, and customer trends.
- **Advanced Analytics:** Use tabs for forecasting, segmentation, and comparison.
- **Download:** Export filtered data for further analysis.

## Customization
You can modify the dashboard by editing `app.py` to add new features, metrics, or visualizations.

## License
This project is for educational and demonstration purposes.

---

**Revify** – Your intelligent sales analytics companion.
