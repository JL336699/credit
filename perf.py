import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Define the path to the directory containing the files
directory_path = 'C:/Users/joseph.lapsley/Perf/static/'

# Function to find the latest file in the directory
def get_latest_file(directory_path):
    files = [f for f in os.listdir(directory_path) if f.endswith('.xlsx')]
    if not files:
        return None
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
    return os.path.join(directory_path, latest_file)

# Streamlit app title
st.title('Municipal Bond Performance Analysis')

# Get the latest file
latest_file_path = get_latest_file(directory_path)

if latest_file_path:
    st.write(f'Processing the latest file: {latest_file_path}')
    
    # Load the data from the Excel file
    data = pd.read_excel(latest_file_path)

    # Display the first few rows to understand the structure of the data
    st.write("Sample data:")
    st.write(data.head())

    # Display the columns to verify data loading
    st.write("Columns in the data:", data.columns)

    # Ensure the necessary columns are present
    required_columns = [
        'Price Date', 'Fund', 'CUSIP Number', 'Security Description',
        'Base Price Percent Change', 'Base Market Value Change'
    ]

    # Check if the required columns are present
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"Missing columns in the data: {', '.join(missing_columns)}")
    else:
        # Convert columns to numeric if necessary
        data['Base Price Percent Change'] = pd.to_numeric(data['Base Price Percent Change'], errors='coerce')
        data['Base Market Value Change'] = pd.to_numeric(data['Base Market Value Change'], errors='coerce')

        # Drop rows with NaN values in the relevant columns
        data.dropna(subset=['Base Price Percent Change', 'Base Market Value Change'], inplace=True)

        # Find the top 10 biggest positive and negative price changes
        top_10_positive_changes = data.sort_values(by='Base Price Percent Change', ascending=False).head(10)
        top_10_negative_changes = data.sort_values(by='Base Price Percent Change', ascending=True).head(10)

        # Find the top 10 biggest positive and negative market value changes
        top_10_positive_market_value_changes = data.sort_values(by='Base Market Value Change', ascending=False).head(10)
        top_10_negative_market_value_changes = data.sort_values(by='Base Market Value Change', ascending=True).head(10)

        # Display the results
        st.subheader('Top 10 Biggest Positive Price Changes')
        st.write(top_10_positive_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Price Percent Change']])

        st.subheader('Top 10 Biggest Negative Price Changes')
        st.write(top_10_negative_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Price Percent Change']])

        st.subheader('Top 10 Biggest Positive Market Value Changes')
        st.write(top_10_positive_market_value_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Market Value Change']])

        st.subheader('Top 10 Biggest Negative Market Value Changes')
        st.write(top_10_negative_market_value_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Market Value Change']])
else:
    st.write('No .xlsx files found in the directory.')

