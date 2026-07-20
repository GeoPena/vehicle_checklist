import pandas as pd
import os


FILE_PATH = "data/vehicles.csv"


def initialize_database():

    if not os.path.exists("data"):
        os.makedirs("data")


    if not os.path.exists(FILE_PATH):

        df = pd.DataFrame(
            columns=[
                "stock_number",
                "vin",
                "year",
                "make",
                "model",
                "mileage"
            ]
        )

        df.to_csv(FILE_PATH, index=False)



def load_vehicles():

    initialize_database()

    return pd.read_csv(
        FILE_PATH,
        dtype={
            "stock_number": str
        }
    )



def add_vehicle(vehicle):

    df = load_vehicles()

    df = pd.concat(
        [
            df,
            pd.DataFrame([vehicle])
        ],
        ignore_index=True
    )

    df.to_csv(
        FILE_PATH,
        index=False
    )



def find_vehicle(stock_number):

    df = load_vehicles()


    df["stock_number"] = (
        df["stock_number"]
        .astype(str)
    )


    result = df[
        df["stock_number"].str.upper()
        ==
        stock_number.upper()
    ]


    if len(result) > 0:
        return result.iloc[0]


    return None

# --------------------------------
# CHECKLIST STORAGE
# --------------------------------


CHECKLIST_FILE = "data/checklist.csv"



def initialize_checklist_database():

    if not os.path.exists("data"):
        os.makedirs("data")


    if not os.path.exists(CHECKLIST_FILE):

        df = pd.DataFrame(
            columns=[
                "stock_number",
                "category",
                "item",
                "status",
                "date",
                "notes"
            ]
        )

        df.to_csv(
            CHECKLIST_FILE,
            index=False
        )



def load_checklist():

    initialize_checklist_database()


    try:

        return pd.read_csv(
            CHECKLIST_FILE,
            dtype={
                "stock_number": str
            }
        )

    except pd.errors.EmptyDataError:


        df = pd.DataFrame(
            columns=[
                "stock_number",
                "category",
                "item",
                "status",
                "date",
                "notes"
            ]
        )


        df.to_csv(
            CHECKLIST_FILE,
            index=False
        )


        return df



def save_checklist_item(data):

    df = load_checklist()


    # eliminar registro anterior del mismo item

    df = df[
        ~(
            (df["stock_number"] == data["stock_number"])
            &
            (df["item"] == data["item"])
        )
    ]


    # agregar nuevo estado

    df = pd.concat(
        [
            df,
            pd.DataFrame([data])
        ],
        ignore_index=True
    )


    df.to_csv(
        CHECKLIST_FILE,
        index=False
    )



def get_vehicle_checklist(stock_number):

    df = load_checklist()


    result = df[
        df["stock_number"] == stock_number
    ]


    return result