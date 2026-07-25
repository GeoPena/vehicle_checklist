from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from modules.checklist import CHECKLIST



def create_pdf(vehicle, checklist):


    buffer = BytesIO()


    doc = SimpleDocTemplate(

        buffer,

        pagesize=letter,

        rightMargin=30,

        leftMargin=30,

        topMargin=30,

        bottomMargin=30

    )


    styles = getSampleStyleSheet()



    title_style = ParagraphStyle(

        "TitleCustom",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=16,

        spaceAfter=5

    )



    heading_style = ParagraphStyle(

        "HeadingCustom",

        parent=styles["Heading2"],

        fontSize=11,

        spaceBefore=8,

        spaceAfter=5

    )



    small_style = ParagraphStyle(

        "Small",

        parent=styles["Normal"],

        fontSize=7,

        leading=8

    )



    elements = []



    # ------------------------------------
    # HEADER
    # ------------------------------------


    elements.append(

        Paragraph(

            "AUTO TECK LLC",

            title_style

        )

    )


    elements.append(

        Paragraph(

            "Vehicle Reconditioning Report",

            heading_style

        )

    )


    elements.append(

        Paragraph(

            f"Generated: {datetime.now().strftime('%Y-%m-%d')}",

            small_style

        )

    )


    elements.append(
        Spacer(1,10)
    )



    # ------------------------------------
    # VEHICLE IDENTIFICATION
    # ------------------------------------


    elements.append(

        Paragraph(

            "Vehicle Identification",

            heading_style

        )

    )


    vehicle_data = [

        [

            "Stock",

            str(vehicle["stock_number"]),

            "Year",

            str(vehicle["year"])

        ],

        [

            "Make",

            str(vehicle["make"]),

            "Model",

            str(vehicle["model"])

        ],

        [

            "Mileage",

            str(vehicle["mileage"]),

            "VIN",

            str(vehicle["vin"])

        ]

    ]



    vehicle_table = Table(

        vehicle_data,

        colWidths=[60,100,60,220]

    )


    vehicle_table.setStyle(

        TableStyle(

            [

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.3,
                    colors.black
                ),

                (
                    "FONTSIZE",
                    (0,0),
                    (-1,-1),
                    8
                )

            ]

        )

    )


    elements.append(

        vehicle_table

    )



    elements.append(

        Spacer(1,10)

    )



    # ------------------------------------
    # RECONDITIONING TABLE
    # ------------------------------------


    elements.append(

        Paragraph(

            "Vehicle Reconditioning",

            heading_style

        )

    )



    table_data = [

        [

            "ITEM",

            "STATUS",

            "DATE / NOTES"

        ]

    ]



    for category, items in CHECKLIST.items():


        # CATEGORY HEADER


        table_data.append(

            [

                category.upper(),

                "",

                ""

            ]

        )



        for item in items:


            existing = checklist[

                checklist["item"] == item

            ]



            status = ""

            date_note = ""



            if not existing.empty:


                row = existing.iloc[0]


                if row["status"] == "Completed":


                    status = "✓"


                    date_note = str(
                        row["date"]
                    )



                elif row["status"] == "In Progress":


                    status = "IP"


                    date_note = str(
                        row["notes"]
                    )



                else:


                    status = ""

                    date_note = ""



            table_data.append(

                [

                    item,

                    status,

                    date_note

                ]

            )



    recon_table = Table(

        table_data,

        colWidths=[250,60,130],

        repeatRows=1

    )



    style_commands = [

        (

            "GRID",

            (0,0),

            (-1,-1),

            0.25,

            colors.black

        ),

        (

            "FONTSIZE",

            (0,0),

            (-1,-1),

            7

        ),

        (

            "VALIGN",

            (0,0),

            (-1,-1),

            "MIDDLE"

        ),

        (

            "BACKGROUND",

            (0,0),

            (-1,0),

            colors.black

        ),

        (

            "TEXTCOLOR",

            (0,0),

            (-1,0),

            colors.white

        ),

    ]



    # Category rows

    row_index = 1


    for category in CHECKLIST.keys():


        style_commands.extend(

            [

                (

                    "BACKGROUND",

                    (0,row_index),

                    (-1,row_index),

                    colors.black

                ),

                (

                    "TEXTCOLOR",

                    (0,row_index),

                    (-1,row_index),

                    colors.white

                ),

                (

                    "FONTNAME",

                    (0,row_index),

                    (-1,row_index),

                    "Helvetica-Bold"

                )

            ]

        )


        row_index += len(
            CHECKLIST[category]
        ) + 1



    recon_table.setStyle(

        TableStyle(

            style_commands

        )

    )



    elements.append(

        recon_table

    )



    elements.append(

        Spacer(1,10)

    )



    # ------------------------------------
    # OBSERVATIONS
    # ------------------------------------


    elements.append(

        Paragraph(

            "Observations",

            heading_style

        )

    )


    observations = """

    _______________________________________________________

    _______________________________________________________

    _______________________________________________________

    """



    elements.append(

        Paragraph(

            observations,

            small_style

        )

    )



    elements.append(

        Spacer(1,15)

    )



    elements.append(

        Paragraph(

            "Authorized Signature: ______________________________",

            small_style

        )

    )


    elements.append(

        Spacer(1,10)

    )


    elements.append(

        Paragraph(

            "Date: ____________________",

            small_style

        )

    )



    doc.build(

        elements

    )


    buffer.seek(0)


    return buffer