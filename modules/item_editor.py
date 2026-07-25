import streamlit as st
from datetime import date

from modules.storage import save_checklist_item
from modules.notes import DEFAULT_NOTES, build_note



def status_icon(status):

    if status == "Completed":
        return "🟢"

    elif status == "In Progress":
        return "🟡"

    else:
        return "🔴"



def edit_item(
    vehicle,
    category,
    item,
    saved_data
):


    # ------------------------------------
    # CURRENT VALUES
    # ------------------------------------

    saved_status = "Pending"
    saved_date = date.today()
    saved_note = ""


    if saved_data is not None:


        saved_status = saved_data["status"]

        saved_note = saved_data["notes"]


        try:

            saved_date = date.fromisoformat(
                str(saved_data["date"])
            )

        except:

            saved_date = date.today()



    # ------------------------------------
    # COLLAPSED TITLE
    # ------------------------------------

    icon = status_icon(saved_status)



    with st.expander(
    f"**{icon} {item}**",
    expanded=False
    ):


        # ------------------------------
        # STATUS
        # ------------------------------

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

            key=f"status_{vehicle['stock_number']}_{item}"

        )



        # ------------------------------
        # DATE
        # ------------------------------

        item_date = st.date_input(

            "Date",

            value=saved_date,

            key=f"date_{vehicle['stock_number']}_{item}"

        )



        # ------------------------------
        # NOTES
        # ------------------------------

        note_options = DEFAULT_NOTES


        current_note_index = 0


        if saved_note:

            if saved_note in note_options:

                current_note_index = note_options.index(
                    saved_note
                )

            else:

                current_note_index = note_options.index(
                    "Other"
                )



        selected_note = st.selectbox(

            "Notes",

            note_options,

            index=current_note_index,

            key=f"note_select_{vehicle['stock_number']}_{item}"

        )



        custom_note = ""


        if selected_note == "Other":


            custom_note = st.text_input(

                "Custom Note",

                value=saved_note,

                key=f"custom_{vehicle['stock_number']}_{item}"

            )



        final_note = build_note(

            selected_note,

            item,

            custom_note

        )



        # ------------------------------
        # SAVE BUTTON
        # ------------------------------

        if st.button(

            "💾 Save",

            key=f"save_{vehicle['stock_number']}_{item}"

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
                        final_note

                }

            )


            st.success(
                "Saved"
            )


            st.rerun()