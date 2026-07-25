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

        rightMargin=20,

        leftMargin=20,

        topMargin=20,

        bottomMargin=20

    )



    styles = getSampleStyleSheet()



    title_style = ParagraphStyle(

        "TitleCustom",

        parent=styles["Title"],

        fontSize=14,

        alignment=TA_CENTER,

        spaceAfter=3

    )



    heading_style = ParagraphStyle(

        "HeadingCustom",

        parent=styles["Heading2"],

        fontSize=9,

        spaceBefore=3,

        spaceAfter=3

    )



    small_style = ParagraphStyle(

        "Small",

        parent=styles["Normal"],

        fontSize=6,

        leading=7

    )



    elements = []



    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------

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

        Spacer(1,5)

    )



    # -------------------------------------------------
    # VEHICLE IDENTIFICATION
    # -------------------------------------------------

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

            str(vehicle["year"]),

            "Make",

            str(vehicle["make"])

        ],

        [

            "Model",

            str(vehicle["model"]),

            "Mileage",

            str(vehicle["mileage"]),

            "VIN",

            str(vehicle["vin"])

        ]

    ]



    vehicle_table = Table(

        vehicle_data,

        colWidths=[45,75,45,55,45,220]

    )



    vehicle_table.setStyle(

        TableStyle(

            [

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.25,
                    colors.black
                ),

                (
                    "BACKGROUND",
                    (0,0),
                    (0,-1),
                    colors.lightgrey
                ),

                (
                    "BACKGROUND",
                    (2,0),
                    (2,-1),
                    colors.lightgrey
                ),

                (
                    "BACKGROUND",
                    (4,0),
                    (4,-1),
                    colors.lightgrey
                ),

                (
                    "FONTNAME",
                    (0,0),
                    (-1,-1),
                    "Helvetica"
                ),

                (
                    "FONTNAME",
                    (0,0),
                    (0,-1),
                    "Helvetica-Bold"
                ),

                (
                    "FONTNAME",
                    (2,0),
                    (2,-1),
                    "Helvetica-Bold"
                ),

                (
                    "FONTNAME",
                    (4,0),
                    (4,-1),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0,0),
                    (-1,-1),
                    7
                )

            ]

        )

    )



    elements.append(

        vehicle_table

    )


    elements.append(

        Spacer(1,5)

    )



    # -------------------------------------------------
    # VEHICLE RECONDITIONING
    # -------------------------------------------------

    elements.append(

        Paragraph(

            "Vehicle Reconditioning",

            heading_style

        )

    )



    # Crear filas para una columna

    def create_column(categories):


        data = []


        for category in categories:


            # Category Header

            data.append(

                [

                    category.upper(),

                    "",

                    ""

                ]

            )



            for item in CHECKLIST[category]:


                existing = checklist[

                    checklist["item"] == item

                ]


                status = ""

                info = ""



                if not existing.empty:


                    row = existing.iloc[0]



                    if row["status"] == "Completed":

                        status = "✓"

                        info = str(row["date"])



                    elif row["status"] == "In Progress":

                        status = "IP"

                        info = str(row["notes"])



                data.append(

                    [

                        item,

                        status,

                        info

                    ]

                )



        table = Table(

            data,

            colWidths=[90,25,55]

        )



        commands = [

            (

                "GRID",

                (0,0),

                (-1,-1),

                0.2,

                colors.black

            ),

            (

                "FONTSIZE",

                (0,0),

                (-1,-1),

                5.5

            ),

            (

                "VALIGN",

                (0,0),

                (-1,-1),

                "MIDDLE"

            )

        ]



        row_number = 0



        for category in categories:


            commands.extend(

                [

                    (

                        "BACKGROUND",

                        (0,row_number),

                        (-1,row_number),

                        colors.black

                    ),

                    (

                        "TEXTCOLOR",

                        (0,row_number),

                        (-1,row_number),

                        colors.white

                    ),

                    (

                        "FONTNAME",

                        (0,row_number),

                        (-1,row_number),

                        "Helvetica-Bold"

                    )

                ]

            )


            row_number += len(

                CHECKLIST[category]

            ) + 1



        table.setStyle(

            TableStyle(commands)

        )



        return table



    categories = list(CHECKLIST.keys())



    column_1 = categories[0:3]

    column_2 = categories[3:6]

    column_3 = categories[6:8]



    table_1 = create_column(column_1)

    table_2 = create_column(column_2)

    table_3 = create_column(column_3)



    main_table = Table(

        [

            [

                table_1,

                table_2,

                table_3

            ]

        ],

        colWidths=[175,175,175]

    )



    elements.append(

        main_table

    )



    elements.append(

        Spacer(1,8)

    )



    # -------------------------------------------------
    # OBSERVATIONS
    # -------------------------------------------------

    elements.append(

        Paragraph(

            "Observations",

            heading_style

        )

    )



    elements.append(

        Paragraph(

            "_________________________________________________________<br/>"
            "_________________________________________________________",

            small_style

        )

    )



    elements.append(

        Spacer(1,10)

    )



    elements.append(

        Paragraph(

            "Authorized Signature: ______________________________",

            small_style

        )

    )



    elements.append(

        Spacer(1,5)

    )



    elements.append(

        Paragraph(

            "Date: ___________________",

            small_style

        )

    )



    doc.build(

        elements

    )



    buffer.seek(0)



    return buffer