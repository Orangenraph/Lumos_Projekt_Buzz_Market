import pandas as pd

def main():
    bee_df = pd.read_csv("data/FAOSTAT_bees.csv")
    bloomberg_df = pd.read_csv("data/Bloomberg Commodity Historical Data.csv")
    crop_df = pd.read_csv("data/FAOSTAT_spefic_crops.csv")


    print("---- Bee ----")
    print(bee_df.info())
    print(bee_df.head(10))

    print("---- Bloomberg ----")
    print(bloomberg_df.info())
    print(bloomberg_df.head(10))

    print("---- Crop ----")
    print(crop_df.info())
    print(crop_df.head(10))

main()