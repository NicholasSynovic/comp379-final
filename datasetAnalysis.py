import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def get_translation_table(filename):
    file_path = "Data_Translation_Tables\{}.csv"
    with open(file_path.format(filename), "r") as inp:
        reader = csv.reader(inp)
        dict_csv = {rows[0]: rows[1] for rows in reader}
    return dict_csv


def correlation_matrix(df: pd.DataFrame):
    """
    A function to calculate and plot
    correlation matrix of a DataFrame.
    """
    # Create the matrix
    matrix = df.corr()

    # Create cmap
    cmap = sns.diverging_palette(250, 15, s=75, l=40, n=9, center="light", as_cmap=True)
    # Create a mask
    mask = np.triu(np.ones_like(matrix, dtype=bool))

    # Make figsize bigger
    fig, ax = plt.subplots(figsize=(16, 12))

    # Plot the matrix
    _ = sns.heatmap(
        matrix,
        mask=mask,
        center=0,
        annot=True,
        fmt=".2f",
        square=True,
        cmap=cmap,
        ax=ax,
    )
    saveable = _.get_figure()


#     saveable.savefig("Dataset_Coorelation_Matrix.jpg")

data_raw = pd.read_csv("Crimes_2021_Dataset.csv")
data_raw.head()

# Shows the information regarding the original dataset and it's types
data_raw.info()

# Drop the following arbitrary columns:
# "ID","Case Number","Updated On", "Year", "Location"
data = pd.read_csv("Crimes_2021_Dataset.csv")
data = data.drop(
    ["ID", "Case Number", "Updated On", "Location", "Year", "Block"], axis=1
)
# data.head()

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

data.tail()


data.info()


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
data.tail()
data.info()


# Sample testing for pairplots and pairwise coorelation matrices
correlation_matrix(data)


data_s = data.drop(
    ["Ward", "FBI Code", "X Coordinate", "Y Coordinate", "Date_week", "Beat"], axis=1
)
correlation_matrix(data_s)
