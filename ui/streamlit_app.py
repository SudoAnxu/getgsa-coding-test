import streamlit as st
import requests
import json

st.set_page_config(page_title="GetGSA Mini", layout="wide")
st.title("GetGSA — AI + RAG mini-slice")

left, right = st.columns(2)

with left:
    st.subheader("Input")
    sample = st.selectbox("Samples", ["-- choose --","Company Profile (A)","Past Performance (PP-1)","Past Performance (PP-2)","Pricing (simple)"])
    sample_map = {
        "Company Profile (A)": "data/samples/company_profile_A.txt",
        "Past Performance (PP-1)": "data/samples/past_performance_1.txt",
        "Past Performance (PP-2)": "data/samples/past_performance_2.txt",
        "Pricing (simple)": "data/samples/pricing_simple.txt",
    }
    docs = st.session_state.get("docs", [])
    if sample != "-- choose --":
        with open(sample_map[sample], "r", encoding="utf-8") as f:
            st.text_area("Preview", f.read(), height=200, key="preview")
        if st.button("Add sample to batch"):
            with open(sample_map[sample], "r", encoding="utf-8") as f:
                docs.append({"name": sample, "type_hint": None, "text": f.read()})
            st.session_state["docs"] = docs

    st.write("Or paste your own:")
    name = st.text_input("Doc name", "pasted.txt")
    type_hint = st.selectbox("Type hint (optional)", [None, "profile", "past_performance", "pricing"])
    text = st.text_area("Text", "", height=200)
    if st.button("Add pasted doc to batch"):
        docs.append({"name": name, "type_hint": type_hint if type_hint else None, "text": text})
        st.session_state["docs"] = docs

    st.write("Current batch:", len(docs), "doc(s)")
    if st.button("Clear batch"):
        st.session_state["docs"] = []

    if st.button("Ingest"):
        r = requests.post("http://127.0.0.1:8000/ingest", json={"documents": docs})
        st.session_state["ingest"] = r.json()
        st.success(f"Ingested. request_id={st.session_state['ingest']['request_id']}")

with right:
    st.subheader("Results")
    req_id = st.text_input("request_id (from Ingest)", value=st.session_state.get("ingest",{}).get("request_id",""))
    if st.button("Analyze"):
        if not req_id:
            st.error("Provide request_id")
        else:
            r = requests.post("http://127.0.0.1:8000/analyze", params={"request_id": req_id})
            if r.status_code == 200:
                data = r.json()
                st.json(data["parsed"])
                st.write("### Checklist")
                st.json(data["checklist"])
                st.write("### Brief")
                st.code(data["brief"])
                st.write("### Client Email")
                st.code(data["client_email"])
                st.write("### Citations")
                st.json(data["citations"])
            else:
                st.error(r.text)
