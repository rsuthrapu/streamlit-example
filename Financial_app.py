# Import python packages
import streamlit as st
import snowflake.snowpark
from snowflake.snowpark.context import get_active_session
import snowflake.snowpark.session as session
import pandas as pd

st.set_page_config(layout="wide")
# Get the current credentials
session = get_active_session()

st.title("----------- Financials------------------ ")


# Replace with your actual Snowflake table name and schema
sql_template = """
SELECT C.CLAIMNUMBER,P.POLICYNUMBER, T.UPDATETIME AS TRANS_DATE,
C.LOSSDATE AS DATE_OF_LOSS ,TLCS.NAME AS CLAIM_STATUS,
CASE 
WHEN TLT.NAME = 'Payment' AND TLCT.NAME = 'Claim Cost' THEN 
NVL(TLI.TRANSACTIONAMOUNT,0) 
WHEN TLT.NAME  = 'Recovery' AND TLCT.NAME = 'Claim Cost' THEN
-TLI.TRANSACTIONAMOUNT 
ELSE 0 END 
AS LOSS_PAID,
CASE WHEN TLT.NAME = 'Payment' AND TLCT.NAME = 'Expense - A&O' THEN 
NVL(TLI.TRANSACTIONAMOUNT,0) 
WHEN TLT.NAME  = 'Recovery' AND TLCT.NAME = 'Expense - A&O' THEN
-TLI.TRANSACTIONAMOUNT ELSE 0 END AS UNALLOC_EXPENSE_PAID,
CASE WHEN TLT.NAME = 'Payment' AND TLCT.NAME = 'Expense - D&CC' THEN
NVL(TLI.TRANSACTIONAMOUNT,0)
WHEN TLT.NAME  = 'Recovery' AND TLCT.NAME = 'Expense - D&CC' THEN
-TLI.TRANSACTIONAMOUNT ELSE 0 END 
AS ALLOC_EXPENSE_PAID,
CASE WHEN TLT.NAME = 'Reserve' AND TLCT.NAME = 'Claim Cost' THEN 
NVL(TLI.TRANSACTIONAMOUNT,0) 
WHEN TLT.NAME  = 'RecoveryReserve' AND TLCT.NAME = 'Claim Cost' THEN
-TLI.TRANSACTIONAMOUNT WHEN TLT.NAME = 'Payment' 
AND TLPMT.NAME = 'Supplement' AND TLCT.NAME = 'Claim Cost' THEN
TLI.TRANSACTIONAMOUNT ELSE 0 END AS LOSS_RESERVE,
CASE WHEN TLT.NAME = 'Reserve' AND TLCT.NAME = 'Expense - A&O' THEN
NVL(TLI.TRANSACTIONAMOUNT,0)
WHEN TLT.NAME  = 'RecoveryReserve' AND TLCT.NAME = 'Expense - A&O' THEN
-TLI.TRANSACTIONAMOUNT 
WHEN TLT.NAME = 'Payment' AND TLPMT.NAME = 'Supplement'
AND TLCT.NAME = 'Expense - A&O' THEN 
TLI.TRANSACTIONAMOUNT ELSE 0 END AS UNALLOC_EXPENSE_RESERVE,
CASE WHEN TLT.NAME = 'Reserve' AND TLCT.NAME = 'Expense - D&CC' THEN 
NVL(TLI.TRANSACTIONAMOUNT,0) 
WHEN TLT.NAME  = 'RecoveryReserve' AND TLCT.NAME = 'Expense - D&CC' THEN
-TLI.TRANSACTIONAMOUNT WHEN TLT.NAME = 'Payment' 
AND TLPMT.NAME = 'Supplement' AND TLCT.NAME = 'Expense - D&CC' THEN
TLI.TRANSACTIONAMOUNT ELSE 0 END 
AS ALLOC_EXPENSE_RESERVE 
FROM CLAIMS_PROD.MRG.CC_TRANSACTION T 
LEFT JOIN CLAIMS_PROD.MRG.CC_TRANSACTIONLINEITEM TLI ON TLI.TRANSACTIONID = T.ID 
LEFT JOIN CLAIMS_PROD.MRG.CCTL_PAYMENTTYPE TLPMT ON TLPMT.ID = T.PAYMENTTYPE
LEFT JOIN CLAIMS_PROD.MRG.CC_EXPOSURE E ON E.ID = T.EXPOSUREID
LEFT JOIN CLAIMS_PROD.MRG.CCTL_LOSSPARTYTYPE TLLPTY ON TLLPTY.ID = E.LOSSPARTY 
LEFT JOIN CLAIMS_PROD.MRG.CC_CLAIM C ON C.ID = NVL(E.CLAIMID, T.CLAIMID)
LEFT JOIN CLAIMS_PROD.MRG.CC_POLICY   P ON P.ID = C.POLICYID 
LEFT JOIN CCTL_TRANSACTION TLT ON TLT.ID = T.SUBTYPE 
LEFT JOIN CCTL_COSTTYPE TLCT ON TLCT.ID = T.COSTTYPE
LEFT JOIN CCTL_CLAIMSTATE TLCS ON TLCS.ID = C.STATE
"""

# WHERE C.CLAIMNUMBER = '{claim_number}'

# Input field for claim number
claim_number = st.text_input("Enter Claim Number (Optional)", "")
# Build the complete SQL query based on input
if claim_number:
  sql = sql_template + f" WHERE C.CLAIMNUMBER = '{claim_number}'"
else:
  sql = sql_template  # Retrieve all data if no claim number entered

try:
  # Execute the query and fetch results
  df = session.sql(sql).to_pandas()

  # Display results
 # st.subheader("Results from Snowflake Table")
  st.dataframe(df, use_container_width=True)

except Exception as e:
  st.error(f"Error executing Snowflake query: {e}")


# if st.button("Run Analysis"):
#  try:
    # Build the final SQL query with claim number
    # sql = sql_template.format(claim_number=claim_number)

      
    
    # Execute query and display results
 #   df = session.sql(sql).to_pandas()
 #   st.dataframe(df, use_container_width=True)
#  except Exception as e:
 #   st.error(f"Error executing Snowflake query: {e}") 
