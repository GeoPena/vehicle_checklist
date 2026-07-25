from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
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



    # -------------------------------------------------
    # PAGE WITH NARROW MARGINS
    # -------------------------------------------------

    doc = BaseDocTemplate(

        buffer,

        pagesize=letter,

        rightMargin=20,

        leftMargin=20,

        topMargin=20,

        bottomMargin=20

    )


    # Main frame

    frame = Frame(

        20,

        20,

        letter[0]-40,

        letter[1]-40,

        id="normal"

    )


    doc.addPageTemplates(

        [

            PageTemplate(

                id="main",

                frames=frame

            )

        ]

    )



    styles = getSampleStyleSheet()



    title_style = ParagraphStyle(

        "Title",

        parent=styles["Title"],

        fontSize=14,

        alignment=TA_CENTER,

        spaceAfter=3

    )



    heading_style = ParagraphStyle(

        "Heading",

        parent=styles["Heading2"],

        fontSize=9,

        spaceBefore=4,

        spaceAfter=3

    )



    small_style = ParagraphStyle(

        "Small",

        parent=styles["Normal"],

        fontSize=6.5,

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

        colWidths=[45,70,45,60,45,220]

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
                    (-1,-1),
                    "Helvetica"
                ),

                (
                    "FONTSIZE",
                    (0,0),
                    (-1,-1),
                    7
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
    # CHECKLIST
    # -------------------------------------------------


    elements.append(

        Paragraph(

            "Vehicle Reconditioning",

            heading_style

        )

    )



    checklist_rows = [

        [

            "ITEM",

            "STATUS",

            "DATE / NOTE"

        ]

    ]



    for category, items in CHECKLIST.items():


        checklist_rows.append(

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

            info = ""



            if not existing.empty:


                row = existing.iloc[0]



                if row["status"] == "Completed":

                    status = "✓"

                    info = str(row["date"])



                elif row["status"] == "In Progress":

                    status = "IP"

                    info = str(row["notes"])



            checklist_rows.append(

                [

                    item,

                    status,

                    info

                ]

            )



    recon_table = Table(

        checklist_rows,

        colWidths=[220,45,90],

        repeatRows=1

    )



    commands = [

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

            6

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

        )

    ]



    row = 1



    for category, items in CHECKLIST.items():


        commands.extend(

            [

                (

                    "BACKGROUND",

                    (0,row),

                    (-1,row),

                    colors.black

                ),

                (

                    "TEXTCOLOR",

                    (0,row),

                    (-1,row),

                    colors.white

                ),

                (

                    "FONTNAME",

                    (0,row),

                    (-1,row),

                    "Helvetica-Bold"

                )

            ]

        )


        row += len(items)+1



    recon_table.setStyle(

        TableStyle(commands)

    )



    elements.append(

        recon_table

    )



    elements.append(

        Spacer(1,5)

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

            "Authorized Signature: _______________________________",

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