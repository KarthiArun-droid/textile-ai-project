import sys
import os
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date
import tempfile
from ultralytics import YOLO

from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chatbot.textile_knowledge import textile_knowledge


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Textile AI Platform",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Textile AI Industrial Platform")
def load_css():
    
    css_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "styles",
        "style.css"
    )

    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# ---------------- MODERN STYLE ----------------

st.markdown("""
<style>

.main{
background-color:#f4f6fb;
}

section[data-testid="stSidebar"]{
background:#0f172a;
}

section[data-testid="stSidebar"] *{
color:white;
}

.block-container{
padding-top:1rem;
}

</style>
""", unsafe_allow_html=True)


# ---------------- DATABASE ----------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR,"database","inspection_history.db")

conn = sqlite3.connect(DB_PATH)


# ---------------- LOGIN ----------------

def check_login(email,password):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
    )

    return cursor.fetchone()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- LOGIN PAGE ----------------

if not st.session_state.logged_in:

    st.header("🔐 Factory Login")

    email = st.text_input("Email")
    password = st.text_input("Password",type="password")

    if st.button("Login"):

        user = check_login(email,password)

        if user:

            st.session_state.logged_in = True
            st.session_state.user_name = user[1]
            st.session_state.user_email = user[2]
            st.session_state.user_role = user[4]

            st.rerun()

        else:
            st.error("Invalid credentials")

    st.stop()


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 🏭 Textile AI")

st.sidebar.markdown("---")

st.sidebar.markdown(f"👤 {st.session_state.user_name}")
st.sidebar.markdown(f"Role: {st.session_state.user_role}")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Production",
        "Shipment",
        "AI Defect Detection",
        "AI Assistant",
        "Inspection History",
        "Profile"
    ]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in=False
    st.rerun()


# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.header("Factory Analytics")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Orders Running",12)
    col2.metric("Defects Today",8)
    col3.metric("Shipments Ready",3)
    col4.metric("Factory Efficiency","92%")

    style_metric_cards()

    st.divider()

    st.subheader("Production Analytics")

    data = {
        "Process":["Knitting","Dyeing","Cutting","Stitching","Packing"],
        "Orders":[5,3,6,4,2]
    }

    df = pd.DataFrame(data)

    fig = px.bar(df,x="Process",y="Orders",color="Process")

    st.plotly_chart(fig,use_container_width=True)


# ---------------- PRODUCTION ----------------

elif menu == "Production":

    st.header("Production Management")

    with stylable_container(
        key="production_card",
        css_styles="""
        {
        background:white;
        padding:20px;
        border-radius:12px;
        }
        """
    ):

        st.subheader("Create Production Order")

        with st.form("order_form"):

            order_id = st.text_input("Order ID")

            process = st.selectbox(
                "Process",
                [
                    "Knitting","Dyeing","Bleaching","Compacting",
                    "Printing","Cutting","Stitching",
                    "Quality Checking","Ironing","Packing"
                ]
            )

            quantity = st.number_input("Quantity",1)

            planned_date = st.date_input("Planned Date")

            status = st.selectbox(
                "Status",
                ["Pending","In Progress","Completed"]
            )

            submit = st.form_submit_button("Add Order")

            if submit:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO production_tasks
                    (order_id,process,quantity,status,planned_date)
                    VALUES(?,?,?,?,?)
                    """,
                    (order_id,process,quantity,status,planned_date)
                )

                conn.commit()

                st.success("Production order created")

    st.subheader("Production Tracker")

    try:

        df = pd.read_sql_query("SELECT * FROM production_tasks",conn)

        st.dataframe(df,use_container_width=True)

    except:
        st.warning("Production table not created")


# ---------------- SHIPMENT ----------------

elif menu == "Shipment":

    st.header("Shipment Planning")

    try:

        df = pd.read_sql_query("SELECT * FROM shipment_plan",conn)

        st.dataframe(df,use_container_width=True)

    except:
        st.warning("Shipment table missing")


# ---------------- DEFECT AI ----------------

elif menu == "AI Defect Detection":

    st.header("AI Fabric Inspection")

    uploaded_file = st.file_uploader(
        "Upload Fabric Image",
        type=["jpg","png","jpeg"]
    )

    if uploaded_file:

        st.image(uploaded_file)

        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())

        image_path = temp.name

        st.info("Running AI model...")

        try:

            model_path = os.path.join(BASE_DIR,"ai","weights","yolov8n.pt")

            model = YOLO(model_path)

            results = model(image_path)

            result_image = results[0].plot()

            st.image(result_image)

            st.success("Defect detection completed")

        except:
            st.error("Model not found")


# ---------------- AI ASSISTANT ----------------

elif menu == "AI Assistant":

    st.header("Textile AI Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask about textile manufacturing")

    if prompt:

        st.chat_message("user").write(prompt)

        response = None

        for key,value in textile_knowledge.items():
            if key in prompt.lower():
                response=value
                break

        if response is None:
            response="I can help with textile production, defects and dyeing."

        st.chat_message("assistant").write(response)

        st.session_state.messages.append({"role":"user","content":prompt})
        st.session_state.messages.append({"role":"assistant","content":response})


# ---------------- HISTORY ----------------

elif menu == "Inspection History":

    st.header("Defect Inspection Records")

    try:

        df = pd.read_sql_query("SELECT * FROM inspections",conn)

        st.dataframe(df,use_container_width=True)

    except:
        st.warning("No inspection data")


# ---------------- PROFILE ----------------

elif menu == "Profile":

    st.header("User Profile")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name,email,role FROM users WHERE email=?",
        (st.session_state.user_email,)
    )

    user = cursor.fetchone()

    st.text_input("Name",value=user[0])
    st.text_input("Email",value=user[1])
    st.text_input("Role",value=user[2],disabled=True)

    st.subheader("Change Password")

    new_password = st.text_input("New Password",type="password")

    if st.button("Update Password"):

        cursor.execute(
            "UPDATE users SET password=? WHERE email=?",
            (new_password,user[1])
        )

        conn.commit()

        st.success("Password updated")