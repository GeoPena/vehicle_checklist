# ----------------------------------------
# PREDEFINED NOTES
# ----------------------------------------

DEFAULT_NOTES = [

    "Checked - Working Properly",

    "Replaced",

    "Adjusted",

    "Cleaned",

    "Detailed",

    "Repaired",

    "Lubricated",

    "Needs Inspection",

    "Waiting for Parts",

    "Part Ordered",

    "Requires Replacement",

    "Not Applicable",

    "Other"

]


# ----------------------------------------
# SUGGESTED REPLACEMENT TEXT
# ----------------------------------------

REPLACEMENT_TEXT = {

    "Oil Change":
        "Replaced engine oil",

    "Oil Filter":
        "Replaced oil filter",

    "Air Filter":
        "Replaced air filter",

    "Cabin Filter":
        "Replaced cabin air filter",

    "Battery":
        "Replaced battery",

    "Brake Fluid":
        "Brake fluid replaced",

    "Coolant Level":
        "Coolant refilled",

    "Transmission Fluid":
        "Transmission fluid serviced",

    "Front Tires":
        "Replaced front tires",

    "Rear Tires":
        "Replaced rear tires",

    "Windshield":
        "Replaced windshield",

    "Head Lights":
        "Replaced headlight",

    "Tail Lights":
        "Replaced tail light",

    "Brake Lights":
        "Replaced brake light",

    "Turn Signals":
        "Replaced turn signal bulb",

    "Power Windows":
        "Window regulator replaced",

    "Power Mirrors":
        "Mirror replaced",

    "Power Locks":
        "Door lock actuator replaced",

    "Keys Available":
        "New key programmed"

}


# ----------------------------------------
# BUILD FINAL NOTE
# ----------------------------------------

def build_note(selected_note, item, custom_note=""):

    if selected_note == "Other":
        return custom_note

    if selected_note == "Replaced":

        if item in REPLACEMENT_TEXT:
            return REPLACEMENT_TEXT[item]

        return "Replaced"

    return selected_note