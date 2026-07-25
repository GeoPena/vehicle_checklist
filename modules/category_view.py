import streamlit as st

from modules.item_editor import edit_item


# ----------------------------------
# CATEGORY STYLE
# ----------------------------------

st.markdown(
    """
    <style>

    div[data-testid="stExpander"] > details > summary {

        background-color: #e9ecef;
        border-radius: 8px;
        padding: 10px;
        font-weight: bold;

    }


    div[data-testid="stExpander"] > details > summary:hover {

        background-color: #d6d8db;

    }


    </style>
    """,
    unsafe_allow_html=True
)



def get_category_progress(
    items,
    saved_checklist
):

    completed = 0


    for item in items:


        existing = saved_checklist[

            saved_checklist["item"] == item

        ]


        if not existing.empty:


            if existing.iloc[0]["status"] == "Completed":

                completed += 1



    return completed



def get_status_icon(
    completed,
    total
):


    if completed == total and total > 0:

        return "🟢"


    elif completed > 0:

        return "🟡"


    else:

        return "🔴"




def show_category(
    vehicle,
    category,
    items,
    saved_checklist
):


    # ----------------------------------
    # CATEGORY PROGRESS
    # ----------------------------------

    completed = get_category_progress(

        items,

        saved_checklist

    )


    total = len(items)



    icon = get_status_icon(

        completed,

        total

    )



    title = (

        f"{icon} {category} "

        f"({completed}/{total})"

    )



    # ----------------------------------
    # CATEGORY EXPANDER
    # ----------------------------------

    with st.expander(

        title,

        expanded=False

    ):


        for item in items:


            existing = saved_checklist[

                saved_checklist["item"] == item

            ]


            saved_data = None



            if not existing.empty:

                saved_data = existing.iloc[0]



            edit_item(

                vehicle,

                category,

                item,

                saved_data

            )