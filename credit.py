import streamlit as st
import pandas as pd
from xbbg import blp

# Function to get Bloomberg data using xbbg
def get_bloomberg_data(cusip):
    """Retrieve Bloomberg data for the given CUSIP."""
    try:
        # Requesting data for the given CUSIP
        fields = [
            'SALES_REV_TURN', 'IS_TOT_OPER_EXP', 'IS_DEPR_EXP', 'IS_INT_EXPENSE',
            'EBITDA', 'EBITDA_TO_REVENUE', 'EBIDA', 'EBIDA_MARGIN',
            'OPERATING_EBIDA', 'OPERATING_EBIDA_MARGIN', 'ARDR_Annual_debt_service',
            'BS_MAXIMUM_ANN_DEBT_SERVICE', 'IS_INTEREST_EXPENSES_OPERATING',
            'BS_ANN_DEBT_SERVICE', 'CASH_AND_MARKETABLE_SECURITIES',
            'BS_CASH_NEAR_CASH_ITEM', 'BS_TOTAL_DEBT_OUTSTANDING', 'BS_LT_BORROW',
            'BS_PENSIONS_LT_LIABS', 'BS_OPRB_LT_LIABS'
        ]
        data = blp.bdp(cusip, flds=fields)
        
        if data.empty:
            st.write("No data found for the provided CUSIP.")
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return pd.DataFrame()

def get_comparables(cusip):
    """Retrieve comparable CUSIPs in the same sector."""
    try:
        # Retrieve the sector code for the given CUSIP
        sector_code = blp.bdp(cusip, flds=['SECTOR'])
        sector_code = sector_code['SECTOR'].values[0] if not sector_code.empty else None
        
        if not sector_code:
            st.write("Sector code not found for the provided CUSIP.")
            return pd.DataFrame()
        
        # Request comparable data based on sector
        comparables = blp.bds(f"Sector:{sector_code}", flds=[
            'SECTOR', 'NAME', 'LAST_PRICE'
        ])
        return comparables
    except Exception as e:
        st.error(f"An error occurred while fetching comparables: {e}")
        return pd.DataFrame()

def show_data(cusip):
    """Fetch and display data for the given CUSIP and its comparables."""
    fundamentals = get_bloomberg_data(cusip)
    
    if fundamentals.empty:
        st.write("No data found for the provided CUSIP.")
        return
    
    sector_code = fundamentals.get('SECTOR', [None])[0]
    if sector_code:
        comparables = get_comparables(cusip)
        st.write(f"Fundamentals for CUSIP: {cusip}")
        st.dataframe(fundamentals)
        
        st.write(f"Comparable CUSIPs in sector {sector_code}")
        st.dataframe(comparables)
    else:
        st.write("No sector code found for the provided CUSIP.")

def main():
    """Streamlit app main function."""
    st.title('Credit Analysis App')
    cusip_input = st.text_input("Enter CUSIP:")
    
    if cusip_input:
        show_data(cusip_input)

if __name__ == '__main__':
    main()
