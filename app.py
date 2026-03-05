import streamlit as st
import requests
from ultralytics import YOLO
from PIL import Image
import cv2
from datetime import datetime
import pandas as pd
from auth import login_screen
from database.db import cursor, conn
from auth import login_screen
from Admin import admin_panel
from flask import Flask
from models.production_model import db
from routes.production_routes import production_bp
from chatbot.textile_knowledge import textile_knowledge

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///factory.db"

db.init_app(app)

app.register_blueprint(production_bp)

if __name__ == "__main__":
   app.run(debug=True, use_reloader=False)
# -------------------------
# LOGIN CHECK
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()

# -------------------------
# LOAD MODEL
# -------------------------
@st.cache_resource
def load_model():
    return YOLO("models/best.pt")
model = load_model()

# -------------------------
# MAIN PAGE
# -------------------------
st.set_page_config(page_title="TextileAI", layout="wide")
st.title(f"🧵 TextileAI Dashboard - Welcome {st.session_state.username} (ID: {st.session_state.user_id})")
if st.session_state.role == "superadmin":
    admin_panel()
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Fabric Defect Detection",
    "📊 Inspection History",
    "📦 Shipment Delay Advisor",
    "💬 AI Assistant"
])

# ======================================================
# TAB 1 – DEFECT DETECTION
# ======================================================
with tab1:
    st.header("🔍 Fabric Defect Detection")

    uploaded_files = st.file_uploader(
        "Upload fabric images",
        type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
        accept_multiple_files=True
    )

    confidence = st.slider("Confidence Threshold", 0.01, 0.9, 0.1)

    if uploaded_files and st.button("Detect Defects"):

        with st.spinner("Analyzing Fabric..."):

            report_data = []

            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file).convert("RGB")
                results = model(image, conf=confidence)

                defect_count = len(results[0].boxes)
                status = "Reject" if defect_count > 0 else "Pass"

                result_img = results[0].plot()
                result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

                st.image(result_img, caption=uploaded_file.name, width=600)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Save to database
                cursor.execute(
                    "INSERT INTO inspections (user_id, image, defect_count, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (
                        st.session_state.user_id,
                        uploaded_file.name,
                        defect_count,
                        status,
                        timestamp
                    )
                )
                conn.commit()

                report_data.append({
                    "Image": uploaded_file.name,
                    "Defect Count": defect_count,
                    "Status": status,
                    "Timestamp": timestamp
                })

            report = pd.DataFrame(report_data)
            st.subheader("Inspection Summary")
            st.dataframe(report)

# ======================================================
# TAB 2 – HISTORY
# ======================================================
with tab2:
    st.header("📊 Inspection History")

    history = pd.read_sql_query(
        f"SELECT image, defect_count, status, timestamp FROM inspections WHERE user_id={st.session_state.user_id}",
        conn
    )

    if not history.empty:
        st.dataframe(history)
        st.bar_chart(history["status"].value_counts())
    else:
        st.info("No inspection history yet.")

# ======================================================
# TAB 3 – SHIPMENT
# ======================================================
with tab3:
    st.header("📦 Shipment Delay Advisor")

    ship_date = st.date_input("Target Shipment Date")

    if st.button("Check Shipment Status"):
        today = datetime.today().date()

        if today > ship_date:
            st.error("⚠ Shipment Delayed")
        else:
            st.success("✅ Shipment On Track")

# ======================================================
# TAB 4 – AI ASSISTANT
# ======================================================
with tab4:
    st.header("💬 Textile AI Assistant")

    question = st.text_input("Ask about textile operations")

    if st.button("Ask AI"):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": question,
                "stream": False
            }
        )

        result = response.json()
        st.write(result.get("response", "No response"))