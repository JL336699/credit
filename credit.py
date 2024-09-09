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
    
    # List of fields to fetch
    fields = {
        'SALES_REV_TURN': 'SALES_REV_TURN',
        'EBIDA': 'EBIDA',
        'EBIDA_MARGIN': 'EBIDA_MARGIN',
        'BS_TOTAL_DEBT_OUTSTANDING': 'BS_TOTAL_DEBT_OUTSTANDING',
        'BS_MAXIMUM_ANN_DEBT_SERVICE': 'BS_MAXIMUM_ANN_DEBT_SERVICE',
        'IS_INT_EXPENSE': 'IS_INT_EXPENSE',
        'ARDR_Annual_debt_service': 'ARDR_Annual_debt_service',
        'BS_LT_BORROW': 'BS_LT_BORROW',
        'Ultimate_Borrower_Name': 'ULTIMATE_BORROWER_NAME',
        'S&P Long Term Rating': 'S_AND_P_LONG_TERM_RATING',
        'Moody\'s Long Term Rating': 'MOODYS_LONG_TERM_RATING',
        'Fitch Long Term Rating': 'FITCH_LONG_TERM_RATING',
        'Current Yield': 'CURRENT_YIELD',
        'Coupon Maturity': 'COUPON_MATURITY',
        'Price': 'PX_LAST',
        'Call/Put Date': 'CALL_PUT_DATE'
    }
    
    results = {}
    for field, bloomberg_field in fields.items():
        try:
            data = blp.bdp(bloomberg_security, bloomberg_field)
            if data.empty:
                results[field] = "No data available."
            else:
                results[field] = data.iloc[0, 0]
        except Exception as e:
            results[field] = f"Error fetching data: {e}"
    
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

