import pandas as pd
import numpy as np

def main():
    bee_df = pd.read_csv("bronze/FAOSTAT_bees.csv")
    crops_df = pd.read_csv("bronze/FAOSTAT_crops.csv")
    bloomberg_df = pd.read_csv("bronze/Bloomberg_Commodity_Historical_Data.csv")

    cleaned_bee_df = clean_bee(bee_df)
    cleaned_bloomberg_df = clean_bloomberg(bloomberg_df)
    cleaned_crops_df = clean_crops(crops_df)

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

    # only pick the columns we need & rename
    df = df[["Area", "Value", "Year", "Flag Description"]].rename(columns={"Value": "Bee_Values"})

    # typecast columns
    df["Year"] = df["Year"].astype(int)
    df["Bee_Values"] = df["Bee_Values"].astype(float)

    df.to_csv("./silver/cleaned_bees.csv", index=False)
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

    #only take columns we need
    df = df[["Area","Item","Value", "Element", "Year","Flag Description"]].copy()

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

    df.to_csv("./silver/cleaned_crops.csv", index=False)
    return df


if __name__ == '__main__':
    main()