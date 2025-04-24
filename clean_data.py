import pandas as pd
import numpy as np

def main():
    bee_df = pd.read_csv("./data/FAOSTAT_bees.csv")
    crops_df = pd.read_csv("./data/FAOSTAT_crops.csv")
    bloomberg_df = pd.read_csv("./data/Bloomberg_Commodity_Historical_Data.csv")

    cleaned_bee_df = clean_bee(bee_df)





def clean_bee(df):
    '''clean the bee data'''

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


    # filter countries with 20% missing values
    to_drop = missing_stats[missing_stats["missing_percent"] > 10]["Area"].tolist()

    temp = df.shape[0]
    df = df[~df["Area"].isin(to_drop)]
    dropped_rows = temp - df.shape[0]

    print(f"{dropped_rows} rows were dropped. Countries (>10% missing): {to_drop}")

    # fills NaN with mean value from country
    fill_values = df.groupby('Area')['Value'].transform('mean')
    df.loc[:, 'Value'] = df['Value'].fillna(fill_values)

    # only pick the columns we need & rename
    df = df[["Area", "Value", "Year", "Flag", "Flag Description"]].rename(columns={"Value": "Bee_Values"})

    # typecast columns
    df["Year"] = df["Year"].astype(int)
    df["Bee_Values"] = df["Bee_Values"].astype(float)

    df.to_csv("./cleaned_data/cleaned_FAOSTAT_bees", index=False)
    return df


if __name__ == '__main__':
    main()