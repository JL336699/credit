import streamlit as st
from xbbg import blp

def validate_cusip(cusip):
    # Ensure CUSIP is 9 characters long
    if len(cusip) == 9 and cusip.isalnum():
        return cusip.upper()
    else:
        raise ValueError("Invalid CUSIP. It must be 9 alphanumeric characters.")

def fetch_data(cusip):
    bloomberg_security = f"/cusip/{cusip}"
    fields = [
        'SALES_REV_TURN',
        'EBIDA',
        'EBIDA_MARGIN',
        'BS_TOTAL_DEBT_OUTSTANDING',
        'BS_MAXIMUM_ANN_DEBT_SERVICE',
        'IS_INT_EXPENSE',
        'ARDR_Annual_debt_service',
        'BS_LT_BORROW'
    ]
    
    results = {}
    for field in fields:
        data = blp.bdp(bloomberg_security, field)
        if data.empty:
            results[field] = "No data available."
        else:
            results[field] = data.iloc[0, 0]
    
    return results

def main():
    st.title("CUSIP Financial Data Fetcher")
    
    cusip = st.text_input("Enter a valid CUSIP (9 alphanumeric characters):")
    
    if cusip:
        try:
            validated_cusip = validate_cusip(cusip)
            data = fetch_data(validated_cusip)
            
            st.write(f"**CUSIP:** {validated_cusip}")
            for field, value in data.items():
                st.write(f"**{field}:** {value}")
        except ValueError as e:
            st.error(e)

if __name__ == "__main__":
    main()
