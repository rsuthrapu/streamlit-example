import streamlit as st
import snowflake.connector

def authenticate_with_oauth(client_id, client_secret, redirect_uri):
    # Redirect the user to Snowflake's OAuth authorization endpoint
    authorization_url = "https://rea00670.snowflakecomputing.com/oauth/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
    }
    # ... (handle the redirect and obtain the authorization code)

    # Exchange the authorization code for an access token
    token_url = "https://login.snowflakecomputing.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }
    # ... (make the request and obtain the access token)

    return access_token

def connect_to_snowflake(access_token):
    conn = snowflake.connector.connect(
        account="YOUR_ACCOUNT",
        user="YOUR_USER",
        password=access_token,  # Use the OAuth access token
        warehouse="YOUR_WAREHOUSE",
        database="YOUR_DATABASE",
        schema="YOUR_SCHEMA",
    )
    return conn

def main():
    st.title("Snowflake Integration with Streamlit")

    client_id = "R%2FykyhaxXg8WlftPZd6Ih0Y4auOsVg%3D%3D"
    client_secret = "YOUR_CLIENT_SECRET"
    redirect_uri = "http://localhost:8501/"  # Adjust if necessary

    if "access_token" not in st.session_state:
        # Redirect to Snowflake's OAuth authorization endpoint
        st.write(f"Please authorize your Snowflake account: <a href='{authorization_url}'>Click here</a>")
    else:
        # Use the access token to connect to Snowflake
        conn = connect_to_snowflake(st.session_state.access_token)

        # Perform Snowflake operations using the connection
        cursor = conn.cursor()
        sql_template =  """
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


if __name__ == "__main__":
    main()