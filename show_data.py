import pandas as pd

def main():

    bee_df = pd.read_csv("silver/cleaned_bees.csv")
    bloomberg_df = pd.read_csv("silver/cleaned_bloomberg.csv")
    df_crops = pd.read_csv("silver/cleaned_crops_new.csv")


    print("\n------------- Bee -------------")
    print(bee_df.info())
    print(bee_df.head(10))

    print("\n------------- Bloomberg -------------")
    print(bloomberg_df.info())
    print(bloomberg_df.head(10))

    print("\n------------- Crop -------------")
    print(df_crops.info())
    print(df_crops.head(10))


    crops = df_crops["Item"].unique().tolist()
    print(crops)




if __name__ == '__main__':
    main()