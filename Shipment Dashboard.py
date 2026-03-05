menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Production Dashboard",
        "Shipment Planning",
        "AI Defect Detection",
        "Defect History"
    ]
    
    elif menu == "Shipment Planning":
    
    st.header("🚚 Shipment Planning")

    query = "SELECT * FROM shipment_plan"

    df = pd.read_sql_query(query, conn)

    if len(df) == 0:
        st.warning("No shipment scheduled")
    else:
        st.dataframe(df)
)
