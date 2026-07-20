import streamlit as st
import pandas as pd
from datetime import date


from modules.checklist import CHECKLIST


from modules.storage import (
    save_checklist_item,
    get_vehicle_checklist
)


from modules.pdf_report import create_pdf



def show_vehicle_page(vehicle):


    st.title(
        "🚗 Vehicle Reconditioning Checklist"
    )



    # ----------------------------------------------------
    # VEHICLE INFORMATION
    # ----------------------------------------------------

    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Stock",
            vehicle["stock_number"]
        )

        st.write(
            f"**VIN:** {vehicle['vin']}"
        )


    with c2:

        st.metric(
            "Year",
            vehicle["year"]
        )

        st.write(
            f"**Make:** {vehicle['make']}"
        )


    with c3:

        st.metric(
            "Mileage",
            vehicle["mileage"]
        )

        st.write(
            f"**Model:** {vehicle['model']}"
        )


    st.divider()



    saved_checklist = get_vehicle_checklist(
        vehicle["stock_number"]
    )



    total_items = 0
    completed_items = 0



    # ----------------------------------------------------
    # CHECKLIST
    # ----------------------------------------------------


    st.subheader(
        "Reconditioning Checklist"
    )



    for category, items in CHECKLIST.items():


        category_completed = 0



        for item in items:


            existing = saved_checklist[
                saved_checklist["item"] == item
            ]


            if (
                not existing.empty
                and existing.iloc[0]["status"] == "Completed"
            ):

                category_completed += 1



        with st.expander(

            f"📂 {category} "
            f"({category_completed}/{len(items)})"

        ):



            for item in items:


                total_items += 1


                saved_status = "Pending"
                saved_notes = ""
                saved_date = date.today()



                existing = saved_checklist[
                    saved_checklist["item"] == item
                ]



                if not existing.empty:


                    saved_status = existing.iloc[0]["status"]

                    saved_notes = existing.iloc[0]["notes"]



                    try:

                        saved_date = date.fromisoformat(

                            str(
                                existing.iloc[0]["date"]
                            )

                        )

                    except:

                        saved_date = date.today()



                c1,c2,c3 = st.columns(
                    [3,2,3]
                )


                with c1:

                    st.write(item)



                with c2:


                    options=[

                        "Pending",
                        "In Progress",
                        "Completed"

                    ]


                    status = st.selectbox(

                        "Status",

                        options,

                        index=options.index(
                            saved_status
                        ),

                        key=f"{vehicle['stock_number']}_{item}"

                    )



                    if status == "Completed":

                        completed_items += 1



                with c3:


                    item_date = st.date_input(

                        "Date",

                        value=saved_date,

                        key=f"date_{vehicle['stock_number']}_{item}"

                    )


                    notes = st.text_input(

                        "Notes",

                        value=saved_notes,

                        key=f"notes_{vehicle['stock_number']}_{item}"

                    )



                if (

                    status != saved_status

                    or notes != saved_notes

                    or str(item_date) != str(saved_date)

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



    # ----------------------------------------------------
    # PROGRESS
    # ----------------------------------------------------


    st.divider()


    progress = 0


    if total_items > 0:

        progress = completed_items / total_items



    st.subheader(
        "Overall Progress"
    )


    st.progress(
        progress
    )


    st.success(

        f"{completed_items}/{total_items} completed "
        f"({int(progress*100)}%)"

    )



    # ----------------------------------------------------
    # PDF REPORT
    # ----------------------------------------------------


    st.divider()


    st.subheader(
        "Reports"
    )



    if st.button(
        "📄 Generate PDF Report"
    ):


        pdf_file = create_pdf(

            vehicle,

            saved_checklist

        )


        st.download_button(

            label="⬇ Download PDF",

            data=pdf_file,

            file_name=f"{vehicle['stock_number']}_Report.pdf",

            mime="application/pdf"

        )