import pandas as pd

def main():
    bee_df = pd.read_csv("silver/cleaned_bees.csv")
    bloomberg_df = pd.read_csv("silver/cleaned_bloomberg.csv")
    crop_df = pd.read_csv("silver/cleaned_crops.csv")


    print("\n------------- Bee -------------")
    print(bee_df.info())
    print(bee_df.head(10))

    print("\n------------- Bloomberg -------------")
    print(bloomberg_df.info())
    print(bloomberg_df.head(10))

    print("\n------------- Crop -------------")
    print(crop_df.info())
    print(crop_df.head(10))


if __name__ == '__main__':
    main()