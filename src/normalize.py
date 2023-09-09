import argparse
import os

import pandas as pd

from google_sheet import save_to_google_sheet
from mongo_dump import export_mongo_collection

_TITLE_MAPPINGS = {
    r'\bsopr\b': "sopracciglia",
    r'\bc\'era\b': "cera",
    r'\btratt\b': "trattemento",
    r'\btratta\b': "trattemento",
    r'\bing\b': "inguine",
    r'\basc\b': "ascelle",
    r'\bbs\b': "baffetti e sopracciglia",
    r'\bebs\b': "e baffetti e sopracciglia",
    r'bsv': "e baffetti e sopracciglia",
    r'\bebse\b': "e baffetti e sopracciglia e",
    r'\bebraccia\b': "e braccia",
    r'\bbaff\b': "baffetti",
    r'\bep\b': "epilazione",
    r'\beinguine\b': "e inguine",
    r'\bcer\b': "cera",
    r'\bxompleta\b': "completa",
    r'\btrattemento\b': "trattamento",
    r'\bsemi\b': "semipermanente",
    r'\bmanisemi\b': "mani semipermanente",
    r'\bera\b': "cera"
}

_COUNTER_MAPPING = {
    r'\s*x1\s*': "",
    r'\s*x2\s*': "",
    r'\bper due\b': "",
    r'\s*x 2\s*': "",
    r'\s*omaggi\s*': "",
    r"\bparrucchiere\b": "",
    r"\bmamma\b": ""
}


def split_by_congiuntions(column):
    return (column.str.replace(r'\+', ',', regex=True)
            .str.replace(r'\s+(e|o)\s+', ',', regex=True)
            .str.split(','))


def remove_extra_white_spaces(colum):
    return colum.str.replace(r'\s+', ' ', regex=True).str.strip()


def normalize(input_file_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_file_path)

    # lower cases and replace with mappings
    df["title"] = df["title"].str.lower().replace(_TITLE_MAPPINGS, regex=True)
    # remove useless counters // TODO: x2 could produce two records
    df["title"] = df["title"].replace(_COUNTER_MAPPING, regex=True)

    df["title"] = remove_extra_white_spaces(df["title"])

    # split and remap after splitting
    df["title"] = split_by_congiuntions(column=df["title"])
    df = df.explode("title")
    df["title"] = df["title"].str.strip()

    df["title"] = df["title"].str.lower().replace(_TITLE_MAPPINGS, regex=True)

    # Count the distinct values in the 'title' column
    distinct_count = df['title'].nunique()
    print("Distinct Count:", distinct_count)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--connection-string", default=os.getenv("MONGO_CONNECTION_STRING"),
                        help="MongoDB connection string")
    parser.add_argument("--service-account", default=os.getenv("SERVICE_ACCOUNT"),
                        help="Path to the Google service account JSON file")
    parser.add_argument("--sheet-id", default=os.getenv("SHEET_ID"), help="Google Sheet ID")
    args = parser.parse_args()

    export_csv = export_mongo_collection(
        connection_str=args.connection_string,
        db="appointment",
        collection="appointments",
        csv_target_file="./export.csv"
    )
    normalize_df = normalize(export_csv)
    save_to_google_sheet(
        service_account_path=args.service_account,
        sheet_id=args.sheet_id,
        dataframe=normalize_df,
        worksheet_name="normalized"
    )
