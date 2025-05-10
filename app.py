import pandas as pd
import streamlit as st

def getFilteredDataFrame(
    csv_file,
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
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None

    if 'date_of_purchase' in df.columns:
        df['date_of_purchase'] = pd.to_datetime(df['date_of_purchase'], format='%d-%m-%Y', errors='coerce')

    if gender is not None:
        df = df[df['Gender'] == gender]

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
        try:
            if 'to' in date_of_purchase:
                start_date, end_date = date_of_purchase.split(' to ')
                start_date = pd.to_datetime(start_date, format='%d-%m-%Y')
                end_date = pd.to_datetime(end_date, format='%d-%m-%Y')
                df = df[(df['date_of_purchase'] >= start_date) & (df['date_of_purchase'] <= end_date)]
            else:
                date_value = pd.to_datetime(date_of_purchase, format='%d-%m-%Y')
                df = df[df['date_of_purchase'] == date_value]
        except Exception as e:
            print(f"Invalid date range: {date_of_purchase}. Error: {e}")

    if payment_method is not None:
        df = df[df['payment_method'] == payment_method]

    print("\nFiltered Dataset:")
    print(df)

    if 'profit' in df.columns:
        df['profit'] = pd.to_numeric(df['profit'], errors='coerce').fillna(0)
        total_profit = df['profit'].sum()
        print(f"\nTotal Profit for filtered data: {total_profit}")
    else:
        print("\n'Profit' column not found in the dataset.")

    return df


st.title("Revify Data Filter")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    gender = st.selectbox("Select Gender", options=["All", "Male", "Female"], index=0)
    age = st.text_input("Enter Age Range (e.g., 20-30)")
    units_sold = st.text_input("Enter Units Sold Range (e.g., 10-50)")
    price = st.text_input("Enter Price Range (e.g., 100-500)")
    item_type = st.text_input("Enter Item Type")
    city = st.text_input("Enter City")
    discount_applied = st.text_input("Enter Discount Applied (e.g., Yes/No)")
    return_status = st.text_input("Enter Return Status (e.g., Returned/Not Returned)")
    date_of_purchase = st.text_input("Enter Date of Purchase (e.g., 01-01-2023 or 01-01-2023 to 31-01-2023)")
    payment_method = st.text_input("Enter Payment Method")
    filter_button = st.button("Filter Data")
    if filter_button:
        gender = None if gender == "All" else gender
        filtered_df = getFilteredDataFrame(
            uploaded_file,
            gender=gender,
            age=age,
            units_sold=units_sold,
            price=price,
            item_type=item_type,
            city=city,
            discount_applied=discount_applied,
            return_status=return_status,
            date_of_purchase=date_of_purchase,
            payment_method=payment_method,
        )
        if filtered_df is not None:
            st.write("Filtered Data:")
            st.dataframe(filtered_df)