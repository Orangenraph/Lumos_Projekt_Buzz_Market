import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

def main():
    '''reads data'''
    df_bees = pd.read_csv("silver/cleaned_bees.csv")
    df_crops3 = pd.read_csv("silver/cleaned_crops3.csv")
    df_bloomberg = pd.read_csv("silver/cleaned_bloomberg.csv")

    pearson_correlation(df_bees, df_crops3, df_bloomberg)
    pearson_correlation_by_continent(df_bees, df_crops3, df_bloomberg)

def pearson_correlation(df_bees,df_crops3,df_bloomberg):
    '''calc correlations between Crops with Bee/Bloomberg
    Outputs: correlations from 0-1'''
    results = []

    crop_items = [item for item in df_crops3["Item"].unique()]
    for item in crop_items:
        # filter for spefic item
        df_item = df_crops3[df_crops3["Item"] == item]

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

        # compute correlations for bees and yields
        bee_prod_corr = df_merged["Bee_Values"].corr(df_merged.get("Production"))

        bee_yield_corr = df_merged["Bee_Values"].corr(df_merged.get("Yield"))


        results.append({
            "Item": item,
            "bee_prod_corr": bee_prod_corr,
            "bee_yield_corr": bee_yield_corr,
        })

    # out of loop
    # create results df
    df_results = pd.DataFrame(results).reset_index(drop=True)

    df_results.to_csv("gold/corr_bee_crop.csv")
    return df_results

def pearson_correlation_by_continent(df_bees, df_crops3, df_bloomberg):
    '''calc correlations between Crops with Bee/Bloomberg for each continent separately
    Outputs: correlations from 0-1 grouped by Continent and Item'''
    results = []

    continents = df_bees["Continent"].unique()
    crop_items = [item for item in df_crops3["Item"].unique()]

    for continent in continents:
        # filter bees data for the current continent
        df_bees_continent = df_bees[df_bees["Continent"] == continent]

        # get unique areas in this continent
        continent_areas = df_bees_continent["Area"].unique()

        for item in crop_items:
            # filter crops data for specific item and areas in this continent
            df_item = df_crops3[df_crops3["Item"] == item]
            df_item_continent = df_item[df_item["Area"].isin(continent_areas)]

            # skip if no data
            if len(df_item_continent) == 0:
                continue

            # pivot
            df_wide = (df_item_continent.pivot_table(
                index=["Area", "Year"],
                columns="Element",
                values="Crop_Values"
            ).reset_index())

            # skip if insufficient
            if len(df_merged) < 3:
                continue

            # compute correlations Production and Yield
            bee_prod_corr = df_merged["Bee_Values"].corr(df_merged.get("Production"))
            bee_yield_corr = df_merged["Bee_Values"].corr(df_merged.get("Yield"))


            results.append({
                "Continent": continent,
                "Item": item,
                "bee_prod_corr": bee_prod_corr,
                "bee_yield_corr": bee_yield_corr,
                "data_points": len(df_merged)
            })

    # create results df
    df_results = pd.DataFrame(results).reset_index(drop=True)

    # Save results grouped by continent
    for continent in continents:
        df_continent = df_results[df_results["Continent"] == continent]
        if not df_continent.empty:
            df_continent.to_csv(f"gold/corr_bee_crop_{continent}.csv")

    return df_results



if __name__ == '__main__':
    main()
