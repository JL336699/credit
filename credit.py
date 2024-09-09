import streamlit as st
import pandas as pd
from xbbg import blp

def get_bloomberg_data(cusip):
    """Fetches data from Bloomberg using the xbbg library."""
    try:
        data = blp.bdp(cusip, [
            'SALES_REV_TURN',
            'IS_TOT_OPER_EXP',
            'IS_DEPR_EXP',
            'IS_INT_EXPENSE',
            'EBITDA',
            'EBITDA_TO_REVENUE',
            'EBIDA',
            'EBIDA_MARGIN',
            'OPERATING_EBIDA',
            'OPERATING_EBIDA_MARGIN',
            'ARDR_Annual_debt_service',
            'BS_MAXIMUM_ANN_DEBT_SERVICE',
            'IS_INTEREST_EXPENSES_OPERATING',
            'ARDR_Annual_debt_service',
            'BS_ANN_DEBT_SERVICE',
            'CASH_AND_MARKETABLE_SECURITIES',
            'BS_CASH_NEAR_CASH_ITEM',
            'BS_TOTAL_DEBT_OUTSTANDING',
            'BS_LT_BORROW',
            'BS_PENSIONS_LT_LIABS',
            'BS_OPRB_LT_LIABS'
        ])
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None

def main():
    st.title("Credit Analysis App")
    cusip_input = st.text_input("Enter CUSIP:")

    if cusip_input:
        st.write("Fetching Bloomberg Data...")

        # Fetch data from Bloomberg
        fundamentals = get_bloomberg_data(cusip_input)

        if fundamentals is not None and not fundamentals.empty:
            st.write("Fetched Bloomberg Data:")
            st.write(fundamentals)
        else:
            st.write(f"No data found for the provided CUSIP: {cusip_input}")

if __name__ == "__main__":
    main()
