import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read data from CSV file
def main():
    df_beeBloom = pd.read_csv("gold/corr_beeBloom_prodArea.csv")

    plot_corr_heatmap(df_beeBloom)


def plot_corr_heatmap(df):
    df_sorted = df.sort_values(by='bee_prod_corr', ascending=False)

    # --- Barplots ---
    fig, axes = plt.subplots(2, 1, figsize=(max(14, len(df) * 1.2), 12))

    # Plot 1: Productivity Correlations
    sns.barplot(ax=axes[0], x='Item', y='bee_prod_corr', data=df_sorted, color='gold', label='Bee Productivity Corr')
    sns.barplot(ax=axes[0], x='Item', y='commodity_prod_corr', data=df_sorted, color='lightblue', alpha=0.7,
                label='Commodity Productivity Corr')
    axes[0].set_title('Correlation Between Bees/Commodity Prices and Productivity by Crop', fontsize=16)
    axes[0].set_ylabel('Correlation Coefficient', fontsize=12)
    axes[0].legend(loc='best')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)
    axes[0].set_xticklabels(df_sorted['Item'], rotation=45, ha='right')

    # Plot 2: Area Correlations
    sns.barplot(ax=axes[1], x='Item', y='bee_area_corr', data=df_sorted, color='orange', label='Bee Area Corr')
    sns.barplot(ax=axes[1], x='Item', y='commodity_area_corr', data=df_sorted, color='skyblue', alpha=0.7,
                label='Commodity Area Corr')
    axes[1].set_title('Correlation Between Bees/Commodity Prices and Cultivation Area by Crop', fontsize=16)
    axes[1].set_ylabel('Correlation Coefficient', fontsize=12)
    axes[1].set_xlabel('Crop Type', fontsize=12)
    axes[1].legend(loc='best')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)
    axes[1].set_xticklabels(df_sorted['Item'], rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('png/bee_commodity_correlation.png', dpi=300)
    plt.show()

    # --- Heatmap ---
    plt.figure(figsize=(max(12, len(df) * 1.1), 8))

    # Neue Reihenfolge: Erst alle Bee-Spalten, dann alle Commodity-Spalten
    corr_data = df.set_index('Item')[[
        'bee_commodity_corr',
        'bee_prod_corr',
        'bee_area_corr',
        'bee_yield_corr',
        'commodity_prod_corr',
        'commodity_area_corr',
        'commodity_yield_corr',
    ]].T

    # Labels entsprechend der neuen Reihenfolge
    corr_data.index = [
        'Bee-Commodity',
        'Bee-Productivity',
        'Bee-Area',
        'Bee-Yield',
        'Commodity-Productivity',
        'Commodity-Area',
        'Commodity-Yield',
    ]

    cmap = sns.diverging_palette(20, 260, as_cmap=True)
    vmin = min(corr_data.min().min(), 0)
    vmax = max(corr_data.max().max(), 1)

    sns.heatmap(corr_data, annot=True, cmap=cmap, vmin=vmin, vmax=vmax, fmt=".2f", linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Coefficients: Bee Population and Commodity Prices', fontsize=16)
    plt.tight_layout()
    plt.savefig('png/correlation_heatmap.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    main()