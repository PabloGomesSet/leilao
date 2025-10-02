import os
import pandas as pd

def update_spreadsheets(dict_list: list):
    df = pd.DataFrame(dict_list)
    name_file = f"leilões.xlsx"

    with pd.ExcelWriter(name_file, engine="xlsxwriter") as writer:
        for auction_key, group in df.groupby("auction_key"):
            group.to_excel(writer, index=False, sheet_name=f"noite_{auction_key}")
        #close_and_open(name_file)

def close_and_open(name_file):
    os.system(f"libreoffice --calc {name_file}")
