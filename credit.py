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
        'EBIDA': 'EBITDA',
        'EBIDA_MARGIN': 'EBITDA_MARGIN',
        'BS_TOTAL_DEBT_OUTSTANDING': 'BS_TOTAL_DEBT_OUTSTANDING',
        'BS_MAXIMUM_ANN_DEBT_SERVICE': 'BS_MAXIMUM_ANN_DEBT_SERVICE',
        'IS_INT_EXPENSE': 'IS_INT_EXPENSE',
        'ARDR_Annual_debt_service': 'ARDR_Annual_debt_service',
        'BS_LT_BORROW': 'BS_LT_BORROW',
        'Ultimate_Borrower_Name': 'NAME',
        'S&P Long Term Rating': 'S&P_LT_RATING',
        'Moody\'s Long Term Rating': 'RTG_MOODY',
        'Fitch Long Term Rating': 'FITCH_LT_RATING',
        'Current Yield': 'YLD_YTM_MID',
        'Coupon Maturity': 'CPN_MATURITY',
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

