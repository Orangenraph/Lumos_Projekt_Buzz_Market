import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score


import matplotlib.pyplot as plt
import seaborn as sns

def main():
    '''reads data'''
    df_bees_europe = pd.read_csv("silver/cleaned_bees_europe.csv")
    df_crops_europe = pd.read_csv("silver/cleaned_crops_europe.csv")

    df_crops_austria = pd.read_csv("silver/cleaned_crops_austria.csv")
    df_bees_austria = pd.read_csv("silver/cleaned_bees_austria.csv")

    df_agro = pd.read_csv("silver/cleaned_agro.csv")

    #top_10_items_per_continent(df_crops)

    #pearson_correlation(df_bees_europe, df_crops_europe)
    #pearson_correlation_austria(df_bees_austria, df_crops_austria)

    regression_analysis_linear(df_bees_europe, df_agro)

    #top_items_austria(df_crops_austria)

def pearson_correlation(df_bees,df_crops):
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
        df_merged = (df_wide.merge(df_bees, on=["Area", "Year"], how="outer"))

        #df_merged.to_csv("test.csv")

        # compute correlations Production
        bee_prod_corr = df_merged["Bee_Values"].corr(df_merged.get("Production"))

        # compute corre Area harvestet
        bee_area_corr = df_merged["Bee_Values"].corr(df_merged.get("Area harvested"))

        bee_yield_corr = df_merged["Bee_Values"].corr(df_merged.get("Yield"))

        results.append({
            "Item": item,
            "bee_prod_corr": bee_prod_corr,
            "bee_area_corr": bee_area_corr,
            "bee_yield_corr": bee_yield_corr,
        })

    # out of loop
    # create results df
    df_results = pd.DataFrame(results).reset_index(drop=True)

    df_results.to_csv("gold/corr_Crops_Bees_europe.csv")
    return df_results

def pearson_correlation_austria(df_bees, df_crops):
    """Calculate correlation for Austria only"""
    df_bees = df_bees[df_bees["Area"] == "Austria"]
    df_crops = df_crops[df_crops["Area"] == "Austria"]

    results = []
    crop_items = df_crops["Item"].unique()

    for item in crop_items:
        df_item = df_crops[df_crops["Item"] == item]
        df_wide = df_item.pivot_table(index=["Area", "Year"], columns="Element", values="Crop_Values").reset_index()
        df_merged = df_wide.merge(df_bees, on=["Area", "Year"], how="inner")

        if len(df_merged) < 3:
            continue

        results.append({
            "Item": item,
            "bee_prod_corr": df_merged["Bee_Values"].corr(df_merged.get("Production")),
            "bee_area_corr": df_merged["Bee_Values"].corr(df_merged.get("Area harvested")),
            "bee_yield_corr": df_merged["Bee_Values"].corr(df_merged.get("Yield")),
        })

    df_results = pd.DataFrame(results)
    df_results.to_csv("gold/corr_Crops_Bees_austria.csv", index=False)
    return df_results

def top_items_austria(df):
    """Identify top crops for Austria based on total value"""
    df_austria = df[df["Area"] == "Austria"]
    df_grouped = df_austria.groupby("Item")["Crop_Values"].sum().reset_index().sort_values(by="Crop_Values", ascending=False).head(10)
    df_grouped.to_csv("gold/top_items_austria.csv", index=False)
    return df_grouped


def regression_analysis_linear(df_bee, df_agro):
    # Aggregiere Bee_Values pro Jahr (Durchschnitt)
    df_bee_agg = df_bee.groupby('Year')['Bee_Values'].mean().reset_index()
    merged_df = pd.merge(df_bee_agg, df_agro, on='Year', how='inner')

    # Define target and feature columns
    target_column = 'Yearly_Avg_Close'  # Zielvariable
    feature_columns = ['Bee_Values']  # Einflussgröße

    y = merged_df[target_column]
    X = merged_df[feature_columns]

    # Preprocessing: Skaliere Bee_Values
    preprocessor = ColumnTransformer(
        transformers=[
            ('scaler', StandardScaler(), ['Bee_Values'])
        ]
    )

    # Pipeline: Preprocessing + Regression
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Train-Test-Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit model
    model_pipeline.fit(X_train, y_train)

    # Predict and calculate R²
    y_pred_train = model_pipeline.predict(X_train)
    y_pred_test = model_pipeline.predict(X_test)
    r_squared_train = r2_score(y_train, y_pred_train)
    r_squared_test = r2_score(y_test, y_pred_test)

    # Get feature names and coefficients
    all_feature_names = feature_columns
    coefficients = model_pipeline.named_steps['regressor'].coef_

    # Create DataFrame with feature coefficients
    results_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Coefficient': coefficients
    })

    # Add R² as separate row
    r2_row = pd.DataFrame([{'Feature': 'R_squared_Test', 'Coefficient': r_squared_test}])
    results_df = pd.concat([results_df, r2_row], ignore_index=True)

    # Save to CSV
    results_df.to_csv("gold/regression_analysis_lr.csv", index=False)

    # Print results
    print(f"R² Train: {r_squared_train}")
    print(f"R² Test: {r_squared_test}")
    print(results_df)

    X_scaled = model_pipeline.named_steps['preprocessor'].fit_transform(X)
    X_scaled = sm.add_constant(X_scaled)  # Füge Intercept hinzu
    model_sm = sm.OLS(y, X_scaled).fit()
    print(model_sm.summary())



if __name__ == '__main__':
    main()