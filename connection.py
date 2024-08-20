# import snowflake.snowpark.session as session

# # Replace with your Snowflake credentials
# connection_parameters = {
#     "account": "your_account",
#     "user": "your_user",
#     "password": "your_password",
#     "role": "your_role",
#     "warehouse": "your_warehouse",
#     "database": "your_database",
#     "schema": "your_schema"
# }

# session = session.Session.builder.configs(connection_parameters).create()

# # Example query
# df = session.sql("SELECT * FROM your_table LIMIT 10")
# df.show()