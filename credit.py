import blpapi
import streamlit as st
import pandas as pd
from blpapi import SessionOptions, Session, Service, Request

# Bloomberg API configuration
BLOOMBERG_SERVER = 'localhost'
BLOOMBERG_PORT = 8194

def create_bloomberg_session():
    """Create and start a Bloomberg session."""
    session_options = blpapi.SessionOptions()
    # Correctly set server address and port
    session_options.setServerHost(BLOOMBERG_SERVER)
    session_options.setServerPort(BLOOMBERG_PORT)
    
    session = blpapi.Session(session_options)
    if not session.start():
        st.error("Failed to start Bloomberg session.")
        return None
    if not session.openService('//blp/refdata'):
        st.error("Failed to open Bloomberg service.")
        return None
    return session

def get_bloomberg_data(cusip):
    """Retrieve Bloomberg data for the given CUSIP."""
    session = create_bloomberg_session()
    if session is None:
        return pd.DataFrame()
    
    service = session.getService('//blp/refdata')
    request = service.createRequest('ReferenceDataRequest')
    request.getElement('securities').appendValue(cusip)
    
    fields = [
        'SALES_REV_TURN', 'IS_TOT_OPER_EXP', 'IS_DEPR_EXP', 'IS_INT_EXPENSE',
        'EBITDA', 'EBITDA_TO_REVENUE', 'EBIDA', 'EBIDA_MARGIN',
        'OPERATING_EBIDA', 'OPERATING_EBIDA_MARGIN', 'ARDR_Annual_debt_service',
        'BS_MAXIMUM_ANN_DEBT_SERVICE', 'IS_INTEREST_EXPENSES_OPERATING',
        'BS_ANN_DEBT_SERVICE', 'CASH_AND_MARKETABLE_SECURITIES',
        'BS_CASH_NEAR_CASH_ITEM', 'BS_TOTAL_DEBT_OUTSTANDING', 'BS_LT_BORROW',
        'BS_PENSIONS_LT_LIABS', 'BS_OPRB_LT_LIABS'
    ]
    
    for field in fields:
        request.getElement('fields').appendValue(field)
    
    session.sendRequest(request)
    data = {}
    
    while True:
        event = session.nextEvent()
        for msg in event:
            if msg.hasElement('securityData'):
                security_data = msg.getElement('securityData')
                if security_data.hasElement('fieldData'):
                    field_data = security_data.getElement('fieldData')
                    for field in field_data.elements():
                        data[field.name()] = field.getValueAsString()
        if event.eventType() == blpapi.Event.RESPONSE:
            break
    
    session.stop()
    df = pd.DataFrame([data])
    st.write("Fetched Bloomberg Data:")
    st.write(df)
    return df

def get_comparables(cusip, sector_code):
    """Retrieve comparable CUSIPs in the same sector."""
    session = create_bloomberg_session()
    if session is None:
        return pd.DataFrame()
    
    service = session.getService('//blp/refdata')
    request = service.createRequest('ReferenceDataRequest')
    request.getElement('securities').appendValue(f"Sector:{sector_code}")
    
    session.sendRequest(request)
    comparables = []
    
    while True:
        event = session.nextEvent()
        for msg in event:
            if msg.hasElement('securityData'):
                security_data = msg.getElement('securityData')
                if security_data.hasElement('fieldData'):
                    field_data = security_data.getElement('fieldData')
                    comparables.append(field_data)
        if event.eventType() == blpapi.Event.RESPONSE:
            break
    
    session.stop()
    df = pd.DataFrame(comparables)
    st.write("Fetched Comparable Data:")
    st.write(df)
    return df

def show_data(cusip):
    """Fetch and display data for the given CUSIP and its comparables."""
    fundamentals = get_bloomberg_data(cusip)
    
    if fundamentals.empty:
        st.write("No data found for the provided CUSIP.")
        return
    
    # Assuming sector code is available in the fundamentals DataFrame
    sector_code = fundamentals.get('SECTOR_CODE', [None])[0]
    if sector_code:
        comparables = get_comparables(cusip, sector_code)
    
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
