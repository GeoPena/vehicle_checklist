from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from modules.checklist import CHECKLIST


def create_pdf(vehicle, checklist):

    buffer = BytesIO()

    doc = SimpleDocTemplate(

        buffer,

        pagesize=letter,

        leftMargin=18,
        rightMargin=18,
        topMargin=18,
        bottomMargin=18

    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(

        "TitleCustom",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=13,

        spaceAfter=2

    )

    heading_style = ParagraphStyle(

        "HeadingCustom",

        parent=styles["Heading2"],

        fontSize=8,

        spaceBefore=2,

        spaceAfter=2

    )

    small_style = ParagraphStyle(

        "Small",

        parent=styles["Normal"],

        fontSize=5.5,

        leading=6

    )

    elements = []

    # =====================================================
    # HEADER
    # =====================================================

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
        Spacer(1,4)
    )

    # =====================================================
    # VEHICLE IDENTIFICATION
    # =====================================================

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

        colWidths=[42,72,42,52,42,225]

    )

    vehicle_table.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),0.25,colors.black),

                ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#DDDDDD")),
                ("BACKGROUND",(2,0),(2,-1),colors.HexColor("#DDDDDD")),
                ("BACKGROUND",(4,0),(4,-1),colors.HexColor("#DDDDDD")),

                ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
                ("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
                ("FONTNAME",(4,0),(4,-1),"Helvetica-Bold"),

                ("FONTSIZE",(0,0),(-1,-1),6),

                ("VALIGN",(0,0),(-1,-1),"MIDDLE")

            ]

        )

    )

    elements.append(vehicle_table)

    elements.append(
        Spacer(1,4)
    )

    # =====================================================
    # VEHICLE RECONDITIONING
    # =====================================================

    elements.append(

        Paragraph(

            "Vehicle Reconditioning",

            heading_style

        )

    )

    all_rows = []

    completed = 0
    in_progress = 0

    total_items = sum(
        len(items)
        for items in CHECKLIST.values()
    )

    for category, items in CHECKLIST.items():

        # True = Category Header

        all_rows.append(

            [

                category.upper(),
                "",
                "",
                True

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

                    completed += 1

                elif row["status"] == "In Progress":

                    status = "IP"

                    info = str(row["notes"])

                    in_progress += 1

            # False = Normal row

            all_rows.append(

                [

                    item,
                    status,
                    info,
                    False

                ]

            )

    pending = total_items - completed - in_progress

    # ------------------------------------------
    # Divide into 3 balanced columns
    # ------------------------------------------

    total_rows = len(all_rows)

    rows_per_column = (total_rows + 2) // 3

    column1 = all_rows[:rows_per_column]

    column2 = all_rows[
        rows_per_column:rows_per_column*2
    ]

    column3 = all_rows[
        rows_per_column*2:
    ]

     # =====================================================
    # CREATE A COLUMN
    # =====================================================

    def create_column(rows):

        # Solo las tres columnas visibles
        display_rows = [row[:3] for row in rows]

        table = Table(

            display_rows,

            colWidths=[90, 18, 55]

        )

        commands = [

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.20,
                colors.black
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "LEADING",
                (0, 0),
                (-1, -1),
                5.5
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                2
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                2
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                2
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                2
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.white
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.black
            )

        ]

        # Solo las categorías llevan fondo negro
        for index, row in enumerate(rows):

            if row[3]:

                commands.extend(

                    [

                        (
                            "BACKGROUND",
                            (0, index),
                            (-1, index),
                            colors.black
                        ),

                        (
                            "TEXTCOLOR",
                            (0, index),
                            (-1, index),
                            colors.white
                        ),

                        (
                            "FONTNAME",
                            (0, index),
                            (-1, index),
                            "Helvetica-Bold"
                        )

                    ]

                )

        table.setStyle(

            TableStyle(commands)

        )

        return table


    table1 = create_column(column1)
    table2 = create_column(column2)
    table3 = create_column(column3)


    # =====================================================
    # MAIN 3-COLUMN TABLE
    # =====================================================

    final_table = Table(

        [

            [

                table1,
                table2,
                table3

            ]

        ],

        colWidths=[175, 175, 175]

    )


    final_table.setStyle(

        TableStyle(

            [

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0
                )

            ]

        )

    )


    elements.append(final_table)

    elements.append(
        Spacer(1, 4)
    )

     # =====================================================
    # OVERALL STATUS
    # =====================================================

    elements.append(

        Paragraph(

            "Overall Status",

            heading_style

        )

    )

    status_table = Table(

        [

            [

                "Completed",
                str(completed),

                "In Progress",
                str(in_progress),

                "Pending",
                str(pending)

            ]

        ],

        colWidths=[60,30,65,30,45,30]

    )

    status_table.setStyle(

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
                    (0,0),
                    colors.HexColor("#DDDDDD")
                ),

                (
                    "BACKGROUND",
                    (2,0),
                    (2,0),
                    colors.HexColor("#DDDDDD")
                ),

                (
                    "BACKGROUND",
                    (4,0),
                    (4,0),
                    colors.HexColor("#DDDDDD")
                ),

                (
                    "FONTNAME",
                    (0,0),
                    (0,0),
                    "Helvetica-Bold"
                ),

                (
                    "FONTNAME",
                    (2,0),
                    (2,0),
                    "Helvetica-Bold"
                ),

                (
                    "FONTNAME",
                    (4,0),
                    (4,0),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0,0),
                    (-1,-1),
                    6
                ),

                (
                    "ALIGN",
                    (0,0),
                    (-1,-1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0,0),
                    (-1,-1),
                    "MIDDLE"
                )

            ]

        )

    )

    elements.append(status_table)

    elements.append(
        Spacer(1,4)
    )

    # =====================================================
    # OBSERVATIONS
    # =====================================================

    elements.append(

        Paragraph(

            "Observations",

            heading_style

        )

    )

    observations_table = Table(

        [

            [" "],

            [" "]

        ],

        colWidths=[530],

        rowHeights=[14,14]

    )

    observations_table.setStyle(

        TableStyle(

            [

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.25,
                    colors.black
                )

            ]

        )

    )

    elements.append(observations_table)

    elements.append(
        Spacer(1,4)
    )

    # =====================================================
    # SIGNATURE
    # =====================================================

    signature_table = Table(

        [

            [

                "Authorized Signature:",

                "________________________",

                "Date:",

                "____________"

            ]

        ],

        colWidths=[90,150,35,60]

    )

    signature_table.setStyle(

        TableStyle(

            [

                (
                    "FONTNAME",
                    (0,0),
                    (0,0),
                    "Helvetica-Bold"
                ),

                (
                    "FONTNAME",
                    (2,0),
                    (2,0),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0,0),
                    (-1,-1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0,0),
                    (-1,-1),
                    0
                ),

                (
                    "TOPPADDING",
                    (0,0),
                    (-1,-1),
                    0
                )

            ]

        )

    )

    elements.append(signature_table)

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(elements)

    buffer.seek(0)

    return buffer