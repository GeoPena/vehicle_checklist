from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER



def create_pdf(vehicle, checklist):


    buffer = BytesIO()



    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )



    styles = getSampleStyleSheet()



    # Centrar título

    styles["Title"].alignment = TA_CENTER



    elements = []



    # ----------------------------------
    # HEADER
    # ----------------------------------

    elements.append(

        Paragraph(
            "AUTO TECK LLC",
            styles["Title"]
        )

    )


    elements.append(

        Paragraph(
            "Vehicle Reconditioning Report",
            styles["Heading2"]
        )

    )


    elements.append(

        Paragraph(

            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",

            styles["Normal"]

        )

    )


    elements.append(
        Spacer(1,20)
    )



    # ----------------------------------
    # VEHICLE INFORMATION
    # ----------------------------------

    elements.append(

        Paragraph(
            "Vehicle Information",
            styles["Heading2"]
        )

    )


    vehicle_data = [

        [
            "Stock Number",
            str(vehicle["stock_number"])
        ],

        [
            "VIN",
            str(vehicle["vin"])
        ],

        [
            "Year",
            str(vehicle["year"])
        ],

        [
            "Make",
            str(vehicle["make"])
        ],

        [
            "Model",
            str(vehicle["model"])
        ],

        [
            "Mileage",
            str(vehicle["mileage"])
        ]

    ]



    vehicle_table = Table(

        vehicle_data,

        colWidths=[
            120,
            300
        ]

    )



    vehicle_table.setStyle(

        TableStyle(

            [

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    None
                ),

                (
                    "VALIGN",
                    (0,0),
                    (-1,-1),
                    "TOP"
                )

            ]

        )

    )



    elements.append(
        vehicle_table
    )


    elements.append(
        Spacer(1,20)
    )



    # ----------------------------------
    # CHECKLIST
    # ----------------------------------

    elements.append(

        Paragraph(
            "Reconditioning Checklist",
            styles["Heading2"]
        )

    )


    elements.append(
        Spacer(1,10)
    )



    checklist_data = [

        [

            "Category",
            "Item",
            "Status",
            "Date",
            "Notes"

        ]

    ]



    # Si no hay registros todavía

    if checklist.empty:


        checklist_data.append(

            [

                "-",

                "No checklist completed yet",

                "-",

                "-",

                "-"

            ]

        )


    else:


        for _, row in checklist.iterrows():


            checklist_data.append(

                [

                    str(row["category"]),

                    str(row["item"]),

                    str(row["status"]),

                    str(row["date"]),

                    str(row["notes"])

                ]

            )



    checklist_table = Table(

        checklist_data,

        colWidths=[

            80,
            130,
            70,
            70,
            120

        ],

        repeatRows=1

    )



    checklist_table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    None

                ),


                (

                    "VALIGN",

                    (0,0),

                    (-1,-1),

                    "TOP"

                )

            ]

        )

    )



    elements.append(

        checklist_table

    )



    elements.append(

        Spacer(1,20)

    )



    # ----------------------------------
    # FOOTER
    # ----------------------------------

    elements.append(

        Paragraph(

            "Prepared by: AUTO TECK LLC",

            styles["Normal"]

        )

    )



    doc.build(
        elements
    )



    buffer.seek(0)



    return buffer