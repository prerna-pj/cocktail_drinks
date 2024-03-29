import json
import sqlite3
import string
import sys

import numpy as np
import pandas as pd
import requests

from util.logger import setup_logger
from util.sqlite_conn import SQLiteConnection

API_URL = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f="
SQLITE_DB_NAME = "cocktail_drinks.db"

# create a logger instance
logger = setup_logger()

# create a sqlite db connection
sqlite_db = SQLiteConnection(db_name=SQLITE_DB_NAME)
sqlite_db.connect()


def test_internet_connection() -> None:
    """
    Function to check a working internet connection.
    """
    try:
        internet = requests.get("https://www.httpbin.org/status/200")
        # logger.info("You have an active interet connection. Proceeding to download drinks data from api.")
    except:
        logger.error("You don't have an active interet connection.")
        sys.exit()


def download_drinks_api(api_url, params):
    """
    Download the drinks details from the api
    - params api_url: The api from which the drinks needs to be downloaded
    - params params: The first letter of the cocktail which needs to be passed
                    as the param to the request api
    - return: Cocktail Drinks list downloded from the api requested
    """
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        if data.get("drinks"):
            return data["drinks"]
        else:
            logger.debug("No drinks found on api.")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading drinks: {e}")
        return []


def create_sqlite_tables() -> None:
    """
    Create tables on sqlite using sql query
    """
    try:
        with open("sql/create_tab_cocktails_details.sql", "r") as sql_file:
            sql_cocktails_details = sql_file.read()
        with open("sql/create_tab_cocktails_ingredients.sql", "r") as sql_file:
            sql_cocktails_ingredients = sql_file.read()

        sqlite_db.create_table(create_table_query=sql_cocktails_details)
        sqlite_db.create_table(create_table_query=sql_cocktails_ingredients)
    except Exception as e:
        logger.exception(f"Error in reading the sql files: {e}")


def insert_api_data(drinks_data) -> None:
    """
    Transform and load the data donloaded from the api into the SQLite Database
    - param drinks_data: Cotaining the cocktail drinks data
    """
    drinks_df = pd.DataFrame(drinks_data)
    drinks_df = drinks_df.drop_duplicates()
    drinks_df["strAlcoholic"] = drinks_df["strAlcoholic"] == "Alcoholic"

    col_map_cocktails_details = {
        "idDrink": "drink_id",
        "strDrink": "drink_name",
        "strDrinkAlternate": "drink_alternate_name",
        "strTags": "drink_tags",
        "strCategory": "drink_category",
        "strIBA": "drink_iba",
        "strGlass": "drink_glass",
        "strAlcoholic": "is_alcoholic",
        "strInstructionsDE": "instructions_de",
    }
    col_list_cocktails_details = [
        "drink_id",
        "drink_name",
        "drink_alternate_name",
        "drink_tags",
        "drink_category",
        "drink_iba",
        "is_alcoholic",
        "drink_glass",
        "instructions_de",
    ]

    unpivot_col_list = [
        "strIngredient1",
        "strIngredient2",
        "strIngredient3",
        "strIngredient4",
        "strIngredient5",
        "strIngredient6",
        "strIngredient7",
        "strIngredient8",
        "strIngredient9",
        "strIngredient10",
        "strIngredient11",
        "strIngredient9",
        "strIngredient10",
        "strIngredient11",
        "strIngredient12",
        "strIngredient13",
        "strIngredient14",
        "strIngredient15",
        "strMeasure1",
        "strMeasure2",
        "strMeasure3",
        "strMeasure4",
        "strMeasure5",
        "strMeasure6",
        "strMeasure7",
        "strMeasure8",
        "strMeasure9",
        "strMeasure10",
        "strMeasure11",
        "strMeasure12",
        "strMeasure13",
        "strMeasure14",
        "strMeasure15",
    ]

    drinks_df.rename(columns=col_map_cocktails_details, inplace=True)
    drinks_df.replace(to_replace=[None], value=np.nan, inplace=True)

    sqlite_db.insert_dataframe(
        table_name="cocktails_details", df=drinks_df[col_list_cocktails_details]
    )

    # Use melt to unpivot the DataFrame to transform cocktails ingredients and its measure
    drinks_ing_df = pd.melt(
        drinks_df,
        id_vars=["drink_id"],
        value_vars=unpivot_col_list,
        var_name="variable",
        value_name="value",
    )

    # Extract 'strIngredient' and 'strMeasure' from the 'variable' column
    drinks_ing_df[["variable", "index"]] = drinks_ing_df["variable"].str.extract(
        r"(\D+)(\d+)"
    )

    # Pivot the DataFrame to combine 'strIngredient' and 'strMeasure'
    drinks_ing_df = drinks_ing_df.pivot_table(
        index=["drink_id", "index"], columns="variable", values="value", aggfunc="first"
    ).reset_index()

    drinks_ing_df.drop("index", axis=1, inplace=True)
    drinks_ing_df.rename(
        columns={
            "strIngredient": "ingredient_name",
            "strMeasure": "ingredient_measure",
        },
        inplace=True,
    )
    drinks_ing_df["ingredient_measure"] = drinks_ing_df[
        "ingredient_measure"
    ].str.strip()
    drinks_ing_df["ingredient_name"] = drinks_ing_df["ingredient_name"].str.strip()

    sqlite_db.insert_dataframe(table_name="cocktails_ingredients", df=drinks_ing_df)


# main function
if __name__ == "__main__":
    # chceck for a valid internet connection before proceeding to download from the api
    test_internet_connection()

    # create the tables for the cocktail drinks database
    create_sqlite_tables()

    # Loop through all the ascii characters and download the drinks from the api
    char_list = list(string.ascii_lowercase + string.digits)
    for char in char_list:
        params = {"f": char}
        drinks = download_drinks_api(api_url=API_URL, params=params)
        if drinks:
            insert_api_data(drinks_data=drinks)

    # close the sqlite connection at the end
    sqlite_db.close_connection()
