import pandas as pd
import numpy as np

from Lumos.Anna.analysis2 import country
from helpers import continent_map, continent_map_large

def main():
    bee_df = pd.read_csv("bronze/FAOSTAT_bees.csv")
    crops_df = pd.read_csv("bronze/FAOSTAT_crops.csv")
    agro_df = pd.read_csv("bronze/agro.csv",delimiter=';')


    #clean_bee(bee_df)
    clean_crops(crops_df)

    #clean_bee_austria(bee_df)
    #clean_crops_austria(crops_df)

    clean_agro(agro_df)

def clean_bee(df):
    '''clean the bee bronze'''

    # put 0 and NaN in vlaues to  None
    df["Value"] = df["Value"].apply(lambda x: np.nan if pd.isna(x) or x == 0 else x)

    # calc statists for each country
    missing_stats = df.groupby("Area")["Value"].agg(
        missing=lambda x: x.isnull().sum(),
        not_missing=lambda x: x.notna().sum(),
        total="count"
    ).reset_index()

    area_sizes = df.groupby("Area").size()
    missing_stats = missing_stats.merge(area_sizes.rename('total_rows'), on='Area')
    missing_stats["missing_percent"] = round((missing_stats["missing"] / missing_stats["total_rows"]) * 100, 2)


    # filter countries with 10% missing values
    to_drop = missing_stats[missing_stats["missing_percent"] > 10]["Area"].tolist()

    temp = df.shape[0]
    df = df[~df["Area"].isin(to_drop)]
    dropped_rows = temp - df.shape[0]

    print(f"{dropped_rows} rows were dropped. Countries (>10% missing): {to_drop}")

    # fills NaN with mean value from country
    fill_values = df.groupby('Area')['Value'].transform('mean')
    df.loc[:, 'Value'] = df['Value'].fillna(fill_values)

    # add continent
    df["Continent"] = df["Area"].map(continent_map)
    df = df[df["Continent"] == "Europe"]

    # only pick the columns we need & rename
    df = df[["Area", "Value", "Year", "Continent", "Flag Description"]].rename(columns={"Value": "Bee_Values"})

    # typecast columns
    df["Year"] = df["Year"].astype(int)
    df["Bee_Values"] = df["Bee_Values"].astype(float)

    df.to_csv("./silver/cleaned_bees_europe.csv", index=False)
    return df

def clean_bloomberg(df):
    df = df[["Date","Price","Open","High","Low","Change %"]].copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year

    # calc mean and rounds by 2
    df = (df.groupby("Year")["Price"]).mean().reset_index()
    df["Price"] = df["Price"].round(2)

    # calc % from prev. years
    #df["Price_Percentage_Change"] = df["Price"].pct_change().round(2) * 100

    df = df.rename(columns={"Price": "Commodity_Price"})

    df.to_csv("./silver/cleaned_bloomberg.csv", index=False)
    return df



def clean_crops(df):
    # add continent
    df = df.copy()

    df["Continent"] = df["Area"].map(continent_map_large)

    df = df[df["Continent"] == "Europe"]

    #only take columns we need
    df = df[["Area","Item","Value", "Element", "Year","Continent", "Flag Description"]]

    # replace 0 or None with NA
    df["Value"] = df["Value"].apply(lambda x: np.nan if pd.isna(x) or x == 0 else x)

    missing_stats = df.groupby(["Area", "Item"])["Value"].agg(
        missing=lambda x: x.isnull().sum(),
        not_missing=lambda x: x.notna().sum(),
        total="count"
    ).reset_index()

    # calc percentage
    missing_stats["missing_percent"] = round((missing_stats["missing"] / missing_stats["total"]) * 100, 2)

    # find combinations of Area and Element with more 10% missing
    to_drop = missing_stats[missing_stats["missing_percent"] > 10][["Area", "Item"]].values.tolist()

    temp = df.shape[0]
    df = df[~df.apply(lambda row: [row["Area"], row["Item"]] in to_drop, axis=1)]

    dropped_rows = temp - df.shape[0]
    print(f"{dropped_rows} rows were dropped. Area-Item (>10% missing): {to_drop}")

    # fill missing values with mean value
    fill_values = df.groupby(["Area", "Item"])['Value'].transform('mean')
    df.loc[:, 'Value'] = df['Value'].fillna(fill_values)

    #rename column
    df = df.rename(columns={"Value": "Crop_Values"})

    #convert bronze types
    df["Year"] = df["Year"].astype(int)
    df["Crop_Values"] = df["Crop_Values"].astype(float)

    df.to_csv("./silver/cleaned_crops_europe.csv", index=False)
    return df


def clean_bee_austria(df):
    '''Clean bee data for Austria only'''
    df = df[df["Area"] == "Austria"].copy()

    df["Value"] = df["Value"].apply(lambda x: np.nan if pd.isna(x) or x == 0 else x)

    missing = df["Value"].isnull().sum()
    total_rows = df.shape[0]
    missing_percent = round((missing / total_rows) * 100, 2)
    print(f"Austria missing values: {missing} of {total_rows} rows ({missing_percent}%)")

    fill_value = df["Value"].mean()
    print(fill_value)
    df["Value"] = df["Value"].fillna(fill_value)

    df["Continent"] = "Europe"

    df = df[["Area", "Value", "Year", "Continent", "Flag Description"]].rename(columns={"Value": "Bee_Values"})

    df["Year"] = df["Year"].astype(int)
    df["Bee_Values"] = df["Bee_Values"].astype(float)

    df.to_csv("./silver/cleaned_bees_austria.csv", index=False)
    return df

def clean_crops_austria(df):
    '''Clean crop data for Austria only'''

    df = df[df["Area"] == "Austria"].copy()

    # Kontinent setzen
    df["Continent"] = "Europe"

    # Nur benötigte Spalten
    df = df[["Area", "Item", "Value", "Element", "Year", "Continent", "Flag Description"]]

    # Ersetze 0 oder None durch NaN
    df["Value"] = df["Value"].apply(lambda x: np.nan if pd.isna(x) or x == 0 else x)

    # Fehlende Werte pro Item in Austria analysieren
    missing_stats = df.groupby("Item")["Value"].agg(
        missing=lambda x: x.isnull().sum(),
        not_missing=lambda x: x.notna().sum(),
        total="count"
    ).reset_index()

    # Prozentsatz berechnen
    missing_stats["missing_percent"] = round((missing_stats["missing"] / missing_stats["total"]) * 100, 2)

    # Items mit mehr als 10 % fehlend entfernen
    to_drop = missing_stats[missing_stats["missing_percent"] > 10]["Item"].tolist()
    temp = df.shape[0]
    df = df[~df["Item"].isin(to_drop)]
    dropped_rows = temp - df.shape[0]
    print(f"{dropped_rows} rows were dropped. Items (10% missing): {to_drop}")

    # Fehlende Werte mit Mittelwert pro Item füllen
    fill_values = df.groupby("Item")["Value"].transform("mean")
    df["Value"] = df["Value"].fillna(fill_values)

    # Spalte umbenennen
    df = df.rename(columns={"Value": "Crop_Values"})

    # Typkonvertierung
    df["Year"] = df["Year"].astype(int)
    df["Crop_Values"] = df["Crop_Values"].astype(float)

    df.to_csv("./silver/cleaned_crops_austria.csv", index=False)
    return df

def clean_agro(df):
    df = df.copy()

    # 1. Clean column names
    df.columns = df.columns.str.strip()

    # 2. Convert date to datetime and extract year
    df['Year'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y').dt.year

    # 3. Clean numeric columns (German formatting)
    numeric_cols = ['Eröffnungspreis', 'Tageshoch', 'Tagestief',
                    'Schlusspreis', 'Diff.%', 'Geldumsatz1', 'Stückumsatz1']

    for col in numeric_cols:
        df[col] = (df[col].astype(str)
                   .str.replace('.', '', regex=False)  # Remove thousand separators
                   .str.replace(',', '.', regex=False)  # Convert decimal comma
                   )

        if col == 'Diff.%':
            df[col] = df[col].str.replace('%', '', regex=False).str.strip()

        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Rename columns to English
    df = df.rename(columns={
        'Schlusspreis': 'Close',
        'Geldumsatz1': 'Volume_EUR',
        'Stückumsatz1': 'Volume'
    })

    # 5. Calculate yearly average closing price
    yearly_avg = df.groupby('Year')['Close'].mean().reset_index()
    yearly_avg.columns = ['Year', 'Yearly_Avg_Close']

    # 6. Save to CSV
    yearly_avg.to_csv("./silver/cleaned_agro.csv", index=False)

    return yearly_avg

if __name__ == '__main__':
    main()


if country.missing_data > 10%:
    remove(country)

if country.missing_data == True:
    country.missing_data = country.mean