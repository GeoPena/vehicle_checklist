import streamlit as st

from modules.checklist import CHECKLIST

from modules.storage import (
    get_vehicle_checklist
)

from modules.category_view import show_category

from modules.pdf_report import create_pdf



def calculate_progress(
    saved_checklist
):

    total = 0
    completed = 0


    for category, items in CHECKLIST.items():

        for item in items:

            total += 1


            existing = saved_checklist[

                saved_checklist["item"] == item

            ]


            if not existing.empty:


                if existing.iloc[0]["status"] == "Completed":

                    completed += 1



    return completed, total




def show_vehicle_page(vehicle):


    # --------------------------------------
    # HEADER
    # --------------------------------------

    st.title(
        "🚗 Vehicle Reconditioning Checklist"
    )



    # --------------------------------------
    # VEHICLE INFORMATION
    # --------------------------------------

    st.subheader(
        "Vehicle Information"
    )


    c1, c2, c3 = st.columns(3)



    with c1:

        st.metric(
            "Stock Number",
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



    # --------------------------------------
    # LOAD CHECKLIST
    # --------------------------------------

    saved_checklist = get_vehicle_checklist(

        vehicle["stock_number"]

    )



    # --------------------------------------
    # REPORT BUTTON
    # --------------------------------------

    st.subheader(
        "Reports"
    )


    if st.button(

        "📄 Generate PDF Report",

        use_container_width=True

    ):


        pdf_file = create_pdf(

            vehicle,

            saved_checklist

        )


        st.download_button(

            label="⬇ Download PDF",

            data=pdf_file,

            file_name=
            f"{vehicle['stock_number']}_Report.pdf",

            mime="application/pdf",

            use_container_width=True

        )



    st.divider()



    # --------------------------------------
    # CHECKLIST
    # --------------------------------------

    st.subheader(
        "Reconditioning Checklist"
    )



    for category, items in CHECKLIST.items():


        show_category(

            vehicle,

            category,

            items,

            saved_checklist

        )



    # --------------------------------------
    # OVERALL PROGRESS
    # --------------------------------------

    st.divider()


    completed, total = calculate_progress(

        saved_checklist

    )


    progress = 0


    if total > 0:

        progress = completed / total



    st.subheader(
        "Overall Progress"
    )



    st.progress(
        progress
    )



    st.success(

        f"{completed}/{total} completed "
        f"({int(progress*100)}%)"

    )