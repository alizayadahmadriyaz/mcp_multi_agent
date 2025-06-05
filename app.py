import streamlit as st
import requests
import json

st.set_page_config(page_title="Multi-Agent System", layout="wide")
st.title("📥 Multi-Format AI System")

format_options = ["email", "json", "pdf"]

with st.form("user_input_form"):
    input_format = st.selectbox("Select Input Format", format_options)

    if input_format == "email":
        sender = st.text_input("Sender Email")
        email_text = st.text_area("Email Body")
        input_data = {"sender": sender, "text": email_text}

    elif input_format == "json":
        raw_json = st.text_area("Paste Raw JSON")
        try:
            input_data = json.loads(raw_json)
        except:
            input_data = {}

    elif input_format == "pdf":
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        input_data = None  # Handled later

    submitted = st.form_submit_button("Process")

if submitted:
    if input_format == "pdf" and uploaded_file is not None:
        st.info("Sending PDF to classifier...")
        files = {"file": uploaded_file.getvalue()}
        res = requests.post("http://localhost:9000/classify/pdf", files=files)
        st.json(res.json())

    elif input_format in ["email", "json"] and input_data:
        st.info(f"Sending {input_format} input to classifier...")
        print(input_data)
        if(input_format=="email"):
            res = requests.post("http://127.0.0.1:9000/process", json={"entry_id":"1235" ,"input_text": input_data["text"]})
        else:
            
# Convert to plain string format without quotes
            data=input_data
            formatted = "{" + ", ".join(f"{k}: {v}" for k, v in data.items()) + "}"
            print(formatted)
            res = requests.post("http://127.0.0.1:9000/process", json={"entry_id":"1235" ,"input_text": formatted})
        print(res)
        st.json(res.json())
    else:
        st.error("Please provide valid input data.")