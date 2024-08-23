import snowflake.connector

# Connect to Snowflake
conn = snowflake.connector.connect(
    user='RSUTHRAPU@CIGINSURANCE.COM',
    password='Welcome123@',
    account='REA00670'
)

# Create a cursor
cur = conn.cursor()

# Execute a query
cur.execute('SELECT * FROM claim_qa.MRG.CCTL_CLAIMSTATE')

# Fetch results
results = cur.fetchall()

# Close the connection
conn.close()