import csv

import numpy as np
import pandas as pd


def get_translation_table(filename):
    file_path = "Data_Translation_Tables\{}.csv"
    with open(file_path.format(filename), "r") as inp:
        reader = csv.reader(inp)
        dict_csv = {rows[0]: rows[1] for rows in reader}
    return dict_csv


def save_df_to_zip(dataframe, filename):
    file = "{}.csv"
    compress_df = dict(method="zip", archive_name=file.format(filename))
    zipfile = "{}.zip"
    dataframe.to_csv(zipfile.format(filename), index=False, compression=compress_df)


data_raw = pd.read_csv("Crimes_2021_Dataset.csv")


# Drop the following arbitrary columns:
# "ID","Case Number","Updated On", "Year", "Location", "Year", "Block"
data = pd.read_csv("Crimes_2021_Dataset.csv")
data = data.drop(
    ["ID", "Case Number", "Updated On", "Location", "Year", "Block"], axis=1
)


# Convert the following bool types to integer values 1/True, 0/False:
# "Arrest", "Domestic"
boolean_dict = {True: 1, False: 0}
data["Arrest"] = data_raw["Arrest"].map(boolean_dict)
data["Domestic"] = data_raw["Domestic"].map(boolean_dict)


# Convert the following columns using the translation tables:
# "IUCR", "Primary Type", "Location Description", "Description", "FBI Code"
primary_type_dict = get_translation_table("Primary_Type_Translation_Table")
location_description_dict = get_translation_table(
    "Location_Description_Translation_Table"
)
iucr_dict = get_translation_table("IUCR_Translation_Table")
fbi_code_dict = get_translation_table("FBI_Code_Translation_Table")
description_dict = get_translation_table("Description_Translation_Table")

data["Primary Type"] = (
    data_raw["Primary Type"].map(primary_type_dict).fillna("0").astype(np.int64)
)
data["Location Description"] = (
    data_raw["Location Description"]
    .map(location_description_dict)
    .fillna("0")
    .astype(np.int64)
)
data["IUCR"] = data_raw["IUCR"].map(iucr_dict).fillna("0").astype(np.int64)
data["FBI Code"] = data_raw["FBI Code"].map(fbi_code_dict).fillna("0").astype(np.int64)
data["Description"] = (
    data_raw["Description"].map(description_dict).fillna("0").astype(np.int64)
)


# Convert date to readable format using the following format:
# '%m/%d/%Y %H:%M'
# Then, seperate Date into individual day, month, week, hour, minute, and dayofweek columns for analysis
data["Date"] = pd.to_datetime(
    data_raw["Date"], format="%m/%d/%Y %H:%M", errors="coerce"
)
data["Date_day"] = data["Date"].dt.day
data["Date_month"] = data["Date"].dt.month
data["Date_week"] = data["Date"].dt.week
data["Date_hour"] = data["Date"].dt.hour
data["Date_minute"] = data["Date"].dt.minute
data["Date_dayofweek"] = data["Date"].dt.dayofweek


# Remove heavily coorelated features and drop samples with no Lo/La data
data_s = data.drop(
    ["Ward", "FBI Code", "X Coordinate", "Y Coordinate", "Date_week", "Date", "Beat"],
    axis=1,
)
data_s = data_s.dropna(subset=["Latitude", "Longitude"])
data_s.info()


# Save processed and optimized datasets to zip/csv
save_df_to_zip(data, "Non-Dropped Processed Dataset")
save_df_to_zip(data_s, "Processed Dataset")
