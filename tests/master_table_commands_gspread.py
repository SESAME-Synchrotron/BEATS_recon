import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe


scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("./../keys/alrecon_v1-f048b037c351.json", scopes=scopes)

# access master
file = gspread.authorize(creds)
workbook = file.open('master')
sheet = workbook.sheet1

# print something to test connection
# print(sheet.range('A2:F2'))

COR = 45
pad = True
alpha = 0.0002

filename = "fiber_test_fast-20230731T185660"

# update master when button is pushed
master = get_as_dataframe(sheet).dropna(axis=0, how='all')

# check if scan is already in master
if np.any(master['scan'].isin([filename])):
    print("filename in master")

    # check if already reconstructed
    if master.loc[master["scan"] == filename, "reconstructed"][0]:

        # if already reconstructed create a new line
        newline = master.loc[master["scan"] == filename]

        # if multiple rows exist for 1 scan take the first one
        if len(newline) > 1:
            newline = newline.loc[[0]]

        # newline["reconstructed"] = False
        newline["cor"] = COR
        newline["pad"] = pad
        newline["alpha"] = alpha
        master = pd.concat([master, newline])
    else:
        master.loc[master["scan"] == filename, "cor"] = COR
        master.loc[master["scan"] == filename, "pad"] = pad
        master.loc[master["scan"] == filename, "alpha"] = alpha

        # master.loc[master["scan"] == filename, "reconstructed"] = True

else:
    print("filename not in master")
    master.loc[len(master), ["scan", "cor", "pad", "alpha"]] = [filename, COR, pad, alpha]

# update master sheet
set_with_dataframe(sheet, master)

# launch recon script on Rum


# launch watchdog on reconstruction



