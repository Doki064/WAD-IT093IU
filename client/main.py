import streamlit as st
import requests

welcome = requests.get("http://localhost:8080/api/")
st.header(welcome.json()["message"])


username = st.text_input("Username: ", value="")
password = st.text_input("Password: ", value="")
if st.button("Register") and username and password:
    requests.post(
        "http://localhost:8080/api/users/",
        json={
            "username": username,
            "password": password,
        },
    )

if st.button("Get") and username:
    user = requests.get(f"http://localhost:8080/api/users/{username}")
    st.write(user.json())
