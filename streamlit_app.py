from collections import namedtuple
from io import StringIO
import altair as alt
import math
import pandas as pd
import streamlit as st
import tableauserverclient as TSC
from tkinter import *
from tkinter import ttk
"""
# Tableau Report intg. with Streamlit!
"""

# root =  Tk()


# Set up connection.
tableau_auth = TSC.TableauAuth('rsuthrapu', 'Rs050222@RAJ')
server = TSC.Server('http://pwtabmyn01/', use_server_version=True)

# with server.auth.sign_in(tableau_auth):
#     all_datasources, pagination_item = server.datasources.get()
#     print("\nThere are {} datasources on site: ".format(pagination_item.total_available))
#     print([datasource.name for datasource in all_datasources])     
#     st.write([datasource.name for datasource in all_datasources])

# Get various data.
# Explore the tableauserverclient library for more options.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query():
    with server.auth.sign_in(tableau_auth):

        # Get all workbooks.
        workbooks, pagination_item = server.workbooks.get()
        workbooks_names = [w.name for w in workbooks]

        # my_combo =  ttk.Combobox(root, values=workbooks_names)
        # my_combo.pack(pady=20)

        # Get views for first workbook.
        server.workbooks.populate_views(workbooks[0])
        views_names = [v.name for v in workbooks[0].views]

        # Get image & CSV for first view of first workbook.
        view_item = workbooks[0].views[1]
        server.views.populate_image(view_item)
        server.views.populate_csv(view_item)
        view_name = view_item.name
        view_image = view_item.image
        # `view_item.csv` is a list of binary objects, convert to str.
        view_csv = b"".join(view_item.csv).decode("utf-8")

        return workbooks_names, views_names, view_name, view_image, view_csv

workbooks_names, views_names, view_name, view_image, view_csv = run_query()


# Print results.
st.subheader("📓 Workbooks")
st.write("Found the following workbooks:", "".join(workbooks_names[0]))

st.subheader("👁️ Views")
st.write(
    f"Workbook *{workbooks_names[0]}* has the following views:",
    ", ".join(views_names),
)

# st.subheader("🖼️ Image")
# st.write(f"Here's what view *{view_name}* looks like:")
# st.image(view_image, width=300)

st.subheader("📊 Data")
st.write(f"And here's the data for view *{view_name}*:")
st.write(pd.read_csv(StringIO(view_csv)))

