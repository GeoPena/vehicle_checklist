import streamlit as st
from config import PASSWORD


def login():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False


    if st.session_state.authenticated:
        return True


    st.title("AUTO TECK LLC")
    st.subheader("Vehicle Reconditioning Manager")

    password = st.text_input(
        "Enter Password",
        type="password"
    )


    if st.button("Login"):

        if password == PASSWORD:
            st.session_state.authenticated = True
            st.success("Access granted")
            st.rerun()

        else:
            st.error("Incorrect password")


    return False