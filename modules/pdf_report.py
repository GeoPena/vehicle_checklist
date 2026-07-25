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



    # =================================================
    # HEADER
    # =================================================


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



    # =================================================
    # VEHICLE IDENTIFICATION
    # =================================================


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



    elements.append(vehicle_table)



    elements.append(
        Spacer(1,5)
    )



    # =================================================
    # VEHICLE RECONDITIONING
    # =================================================


    elements.append(

        Paragraph(

            "Vehicle Reconditioning",

            heading_style

        )

    )



    all_rows = []



    for category, items in CHECKLIST.items():


        all_rows.append(

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



            all_rows.append(

                [

                    item,

                    status,

                    info

                ]

            )



    # -----------------------------------------
    # Split into 3 balanced columns
    # -----------------------------------------


    total = len(all_rows)


    size = total // 3


    columns = [

        all_rows[:size],

        all_rows[size:size*2],

        all_rows[size*2:]

    ]



    def create_column(rows):


        table = Table(

            rows,

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



        for index, row in enumerate(rows):


            if row[1] == "" and row[2] == "":


                commands.extend(

                    [

                        (

                            "BACKGROUND",

                            (0,index),

                            (-1,index),

                            colors.black

                        ),


                        (

                            "TEXTCOLOR",

                            (0,index),

                            (-1,index),

                            colors.white

                        ),


                        (

                            "FONTNAME",

                            (0,index),

                            (-1,index),

                            "Helvetica-Bold"

                        )

                    ]

                )



        table.setStyle(

            TableStyle(commands)

        )



        return table



    table1 = create_column(columns[0])

    table2 = create_column(columns[1])

    table3 = create_column(columns[2])




    final_table = Table(

        [

            [

                table1,

                table2,

                table3

            ]

        ],

        colWidths=[175,175,175]

    )



    elements.append(final_table)



    elements.append(

        Spacer(1,8)

    )



    # =================================================
    # OVERALL STATUS
    # =================================================


    completed = 0

    in_progress = 0

    pending = 0



    for _, row in checklist.iterrows():


        if row["status"] == "Completed":

            completed += 1


        elif row["status"] == "In Progress":

            in_progress += 1


        else:

            pending += 1



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

        colWidths=[70,40,70,40,50,40]

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
                    colors.lightgrey
                ),


                (
                    "BACKGROUND",
                    (2,0),
                    (2,0),
                    colors.lightgrey
                ),


                (
                    "BACKGROUND",
                    (4,0),
                    (4,0),
                    colors.lightgrey
                ),


                (
                    "FONTNAME",
                    (0,0),
                    (-1,-1),
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


    elements.append(status_table)



    elements.append(

        Spacer(1,8)

    )



    # =================================================
    # OBSERVATIONS
    # =================================================


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



    doc.build(elements)



    buffer.seek(0)


    return buffer