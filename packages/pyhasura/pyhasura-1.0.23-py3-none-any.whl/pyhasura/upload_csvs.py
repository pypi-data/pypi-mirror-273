import glob
import os
from enum import Enum
from pathlib import Path

import chardet
import numpy as np
import pandas as pd
import camelcaser as cc

from price_parser import Price
from sqlalchemy import create_engine


class Casing(Enum):
    none = None
    snake = 'Snake'
    camel = 'Camel'
    pascal = 'Pascal'

def predict_encoding(file_path: Path, n_lines: int = 20) -> str:
    with file_path.open('rb') as f:
        rawdata = b''.join([f.readline() for _ in range(n_lines)])
    result = chardet.detect(rawdata)
    return result['encoding']


def is_currency_string(input_string):
    try:
        price = Price.fromstring(str(input_string))
        return price.amount is not None and price.currency is not None
    except ValueError:
        return False


def get_currency_amount(input_string):
    try:
        if not pd.isnull(input_string):
            price = Price.fromstring(input_string)
            return price.amount
        else:
            return np.nan
    except ValueError:
        return np.nan


def fix_dates(df: pd.DataFrame, threshold=.1) -> pd.DataFrame:
    # Identify date columns and convert to timestamp
    for col in df.columns:
        if df[col].dtype == 'object':  # Check if the column contains string values
            valid_dates_mask = pd.to_datetime(df[col], errors='coerce').notnull()

            # Calculate the percentage of valid dates
            valid_dates_percentage = valid_dates_mask.sum() / len(df)

            if valid_dates_percentage > threshold:
                # Convert valid dates to datetime format
                df[col] = pd.to_datetime(df[col])
    return df


def fix_currency(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns[1:]:
        if df[col].dtype == 'object' and df[col].apply(is_currency_string).all():
            # Remove currency symbols and commas
            df[col] = df[col].apply(get_currency_amount).fillna(df[col])
            df[col] = df[col].astype(float)
    return df


def import_tables(csv_folder: str, uri: str, if_exists='replace', logging=None, casing=Casing.none) -> list[str]:
    """
    Imports tables from CSV files into a database using SQLAlchemy.

    Args:
        csv_folder (str): The path to the folder containing the CSV files.
        uri (str): The URI of the database.
        if_exists (str, optional): The action to take if the table already exists in the database. \
        Defaults to 'replace'. 'append' can also be used.
        logging (Logger, optional): The logging object to use for logging messages. Defaults to None.
        casing (Casing, optional): The casing style to apply to column names. Defaults to Casing.none.

    Returns:
        pd.DataFrame: A DataFrame containing the table names that were imported.

    """
    engine = create_engine(uri)
    logging.info("Connected to database")
    results = []

    # Loop through each CSV file
    for filename in glob.glob(os.path.join(csv_folder, "*.csv")):
        table_name = cc.make_camel_case(os.path.splitext(os.path.basename(filename))[0])
        results.append(table_name)
        df = pd.read_csv(filename, encoding=predict_encoding(Path(filename)))
        df = fix_dates(df)
        df = fix_currency(df)
        if casing == Casing.camel:
            df.columns = [cc.make_lower_camel_case(col) for col in df.columns]
        elif casing == Casing.snake:
            df.columns = [cc.make_snake_case(col.replace(' ', '_')) for col in df.columns]
        elif casing == Casing.pascal:
            df.columns = [cc.make_camel_case(col.replace(' ', '_')) for col in df.columns]
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        logging.info(f"Data loaded into '{table_name}'")

    logging.info("All tables created and data loaded successfully!")
    return results
