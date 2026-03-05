import streamlit as st
import pandas as pd
from database.db import conn

def admin_panel():

    st.header("👑 Super Admin Dashboard")

    users = pd.read_sql_query("SELECT id, username, email, role FROM users", conn)
    inspections = pd.read_sql_query("SELECT * FROM inspections", conn)

    st.subheader("👥 Registered Users")
    st.dataframe(users)

    st.subheader("📊 Total Inspections")
    st.dataframe(inspections)

    st.metric("Total Users", len(users))
    st.metric("Total Inspections", len(inspections))

    if not inspections.empty:
        st.bar_chart(inspections["status"].value_counts())
        
        