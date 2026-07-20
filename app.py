import streamlit as st

from modules.auth import login
from modules.storage import (
    initialize_database,
    add_vehicle,
    find_vehicle,
    load_vehicles
)

from modules.vehicle_page import show_vehicle_page


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Vehicle Reconditioning Manager",
    page_icon="🚗",
    layout="wide"
)


# -----------------------------
# LOGIN
# -----------------------------

if not login():
    st.stop()



# -----------------------------
# SESSION STATE
# -----------------------------

if "create_vehicle" not in st.session_state:
    st.session_state.create_vehicle = False


if "search_vehicle" not in st.session_state:
    st.session_state.search_vehicle = False


if "selected_vehicle" not in st.session_state:
    st.session_state.selected_vehicle = None



# -----------------------------
# DATABASE
# -----------------------------

initialize_database()



# -----------------------------
# HEADER
# -----------------------------

st.title("AUTO TECK LLC")
st.subheader("Vehicle Reconditioning Manager")

st.divider()



# -----------------------------
# VEHICLE COUNT
# -----------------------------

vehicles = load_vehicles()


if len(vehicles) == 0:

    st.info(
        "No vehicles registered yet."
    )

else:

    st.success(
        f"Registered vehicles: {len(vehicles)}"
    )



st.divider()



# -----------------------------
# MAIN OPTIONS
# -----------------------------

option1, option2 = st.columns(2)



with option1:

    if st.button(
        "🔍 Search Vehicle",
        use_container_width=True
    ):

        st.session_state.search_vehicle = True



with option2:

    if st.button(
        "➕ Create New Vehicle",
        use_container_width=True
    ):

        st.session_state.create_vehicle = True



# -----------------------------
# SEARCH VEHICLE
# -----------------------------

if st.session_state.search_vehicle:


    st.divider()

    st.subheader(
        "Search Vehicle"
    )


    stock_number = st.text_input(
        "Enter Stock Number"
    )



    if st.button(
        "Find Vehicle"
    ):


        if stock_number:


            vehicle = find_vehicle(
                stock_number
            )


            if vehicle is not None:


                st.session_state.selected_vehicle = vehicle


                st.success(
                    "Vehicle Found"
                )


            else:


                st.warning(
                    "Vehicle not found."
                )



# -----------------------------
# SHOW SELECTED VEHICLE
# -----------------------------

if st.session_state.selected_vehicle is not None:


    show_vehicle_page(
        st.session_state.selected_vehicle
    )



# -----------------------------
# CREATE VEHICLE
# -----------------------------

if st.session_state.create_vehicle:


    st.divider()


    st.subheader(
        "Create New Vehicle"
    )


    with st.form(
        "vehicle_form"
    ):


        col1, col2 = st.columns(2)



        with col1:


            stock_number = st.text_input(
                "Stock Number *"
            )


            vin = st.text_input(
                "VIN"
            )


            year = st.text_input(
                "Year"
            )



        with col2:


            make = st.text_input(
                "Make"
            )


            model = st.text_input(
                "Model"
            )


            mileage = st.text_input(
                "Mileage"
            )



        submitted = st.form_submit_button(
            "Save Vehicle"
        )



        if submitted:


            if stock_number == "":


                st.error(
                    "Stock Number is required."
                )


            else:


                vehicle = {


                    "stock_number": stock_number.upper(),

                    "vin": vin,

                    "year": year,

                    "make": make,

                    "model": model,

                    "mileage": mileage

                }



                add_vehicle(
                    vehicle
                )


                st.success(
                    "Vehicle successfully created!"
                )


                st.session_state.create_vehicle = False


                st.session_state.selected_vehicle = vehicle


                st.rerun()