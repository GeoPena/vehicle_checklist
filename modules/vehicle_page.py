import streamlit as st
import pandas as pd
from datetime import date

from modules.checklist import CHECKLIST

from modules.storage import (
    save_checklist_item,
    get_vehicle_checklist
)



def show_vehicle_page(vehicle):


    st.divider()


    st.title(
        "VEHICLE READY FOR SALE CHECKLIST"
    )



    # -----------------------------
    # VEHICLE INFORMATION
    # -----------------------------

    st.subheader(
        "Vehicle Information"
    )


    col1, col2, col3 = st.columns(3)



    with col1:

        st.write("**Stock Number**")
        st.write(
            vehicle["stock_number"]
        )


        st.write("**VIN**")
        st.write(
            vehicle["vin"]
        )



    with col2:

        st.write("**Year**")
        st.write(
            vehicle["year"]
        )


        st.write("**Make**")
        st.write(
            vehicle["make"]
        )



    with col3:

        st.write("**Model**")
        st.write(
            vehicle["model"]
        )


        st.write("**Mileage**")
        st.write(
            vehicle["mileage"]
        )



    st.divider()



    # -----------------------------
    # LOAD SAVED CHECKLIST
    # -----------------------------

    saved_checklist = get_vehicle_checklist(
        vehicle["stock_number"]
    )



    total_items = 0

    completed_items = 0



    # -----------------------------
    # CHECKLIST
    # -----------------------------

    st.subheader(
        "Reconditioning Checklist"
    )



    for category, items in CHECKLIST.items():


        st.subheader(
            category
        )


        for item in items:


            total_items += 1


            # Default values

            saved_status = "Pending"

            saved_notes = ""

            saved_date = date.today()



            # Look for saved data

            if not saved_checklist.empty:


                existing = saved_checklist[
                    saved_checklist["item"] == item
                ]



                if not existing.empty:


                    saved_status = existing.iloc[0]["status"]

                    saved_notes = existing.iloc[0]["notes"]


                    try:

                        saved_date = existing.iloc[0]["date"]
                        if pd.isna(saved_date):
                            saved_date = date.today()
                        else:
                            saved_date = date.fromisoformat(
                                str(saved_date)
                            )

                    except:

                        saved_date = date.today()



            col1, col2, col3 = st.columns(
                [3, 2, 3]
            )



            with col1:

                st.write(
                    item
                )



            with col2:


                status_options = [

                    "Pending",
                    "In Progress",
                    "Completed"

                ]


                status = st.selectbox(

                    "Status",

                    status_options,

                    index=status_options.index(
                        saved_status
                    ),

                    key=f"{vehicle['stock_number']}_{item}"

                )



                if status == "Completed":

                    completed_items += 1



            with col3:


                notes = st.text_input(

                    "Notes",

                    value=saved_notes,

                    key=f"notes_{vehicle['stock_number']}_{item}"

                )



                item_date = st.date_input(

                    "Date",

                    value=saved_date,

                    key=f"date_{vehicle['stock_number']}_{item}"

                )



            # SAVE CHANGES

            if (

                status != saved_status

                or

                notes != saved_notes

                or

                str(item_date) != str(saved_date)

            ):


                save_checklist_item(

                    {

                        "stock_number":
                            vehicle["stock_number"],


                        "category":
                            category,


                        "item":
                            item,


                        "status":
                            status,


                        "date":
                            str(item_date),


                        "notes":
                            notes

                    }

                )



    st.divider()



    # -----------------------------
    # PROGRESS
    # -----------------------------

    if total_items > 0:


        progress = (

            completed_items

            /

            total_items

        )



        st.subheader(
            "Overall Progress"
        )



        st.progress(
            progress
        )



        percentage = int(
            progress * 100
        )



        st.success(
            f"{percentage}% Complete "
            f"({completed_items}/{total_items} items)"
        )