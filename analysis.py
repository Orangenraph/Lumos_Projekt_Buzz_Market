import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

def main():
    '''reads data'''
    df_bees = pd.read_csv("silver/cleaned_bees.csv")
    df_crops = pd.read_csv("silver/cleaned_crops.csv")
    df_bloomberg = pd.read_csv("silver/cleaned_bloomberg.csv")


    pearson_correlation(df_bees, df_crops, df_bloomberg)

def pearson_correlation(df_bees,df_crops,df_bloomberg):
    '''calc correlations between Crops with Bee/Bloomberg
    Outputs: correlations from 0-1'''
    results = []

    crop_items = [item for item in df_crops["Item"].unique()]
    for item in crop_items:
        # filter for spefic item
        df_item = df_crops[df_crops["Item"] == item]

        # pivot
        df_wide = (df_item.pivot_table(
            index=["Area","Year"],
            columns="Element",
            values="Crop_Values"
        ).reset_index())
        #print(df_wide)

        # merg bees and prices
        df_merged = (df_wide.merge(df_bees, on=["Area", "Year"], how="outer").merge(df_bloomberg, on="Year", how="outer"))

        #df_merged.to_csv("test.csv")

        # compute correlations Production
        bee_prod_corr = df_merged["Bee_Values"].corr(df_merged.get("Production"))
        commodity_prod_corr = df_merged["Commodity_Price"].corr(df_merged.get("Production"))

        # compute corre Area harvestet
        bee_area_corr = df_merged["Bee_Values"].corr(df_merged.get("Area harvested"))
        commodity_area_corr = df_merged["Commodity_Price"].corr(df_merged.get("Area harvested"))

        bee_yield_corr = df_merged["Bee_Values"].corr(df_merged.get("Yield"))
        commodity_yield_corr = df_merged["Commodity_Price"].corr(df_merged.get("Yield"))

        bee_commodity_corr = df_merged["Commodity_Price"].corr(df_merged.get("Bee_Values"))

        results.append({
            "Item": item,
            "bee_commodity_corr": bee_commodity_corr,
            "bee_prod_corr": bee_prod_corr,
            "bee_area_corr": bee_area_corr,
            "bee_yield_corr": bee_yield_corr,
            "commodity_prod_corr": commodity_prod_corr,
            "commodity_area_corr": commodity_area_corr,
            "commodity_yield_corr": commodity_yield_corr,
        })

    # out of loop
    # create results df
    df_results = pd.DataFrame(results).reset_index(drop=True)

    df_results.to_csv("gold/corr_beeBloom_prodArea.csv")
    return df_results

if __name__ == '__main__':
    main()