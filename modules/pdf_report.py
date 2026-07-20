from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter



def create_pdf(vehicle, checklist):

    buffer = BytesIO()


    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )


    styles = getSampleStyleSheet()


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
        Spacer(1,20)
    )


    # ----------------------------------
    # VEHICLE INFORMATION
    # ----------------------------------

    vehicle_data = [

        ["Stock Number", str(vehicle["stock_number"])],

        ["VIN", str(vehicle["vin"])],

        ["Year", str(vehicle["year"])],

        ["Make", str(vehicle["make"])],

        ["Model", str(vehicle["model"])],

        ["Mileage", str(vehicle["mileage"])]

    ]


    table = Table(
        vehicle_data,
        colWidths=[120,300]
    )


    table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None),
            ]
        )
    )


    elements.append(table)


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
        repeatRows=1
    )


    checklist_table.setStyle(

        TableStyle(

            [

                ("GRID",
                 (0,0),
                 (-1,-1),
                 0.5,
                 None),

                ("VALIGN",
                 (0,0),
                 (-1,-1),
                 "TOP")

            ]

        )

    )


    elements.append(
        checklist_table
    )


    elements.append(
        Spacer(1,20)
    )


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