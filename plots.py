import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Rectangle
import seaborn as sns

from helpers import continents

# Read data from CSV file
def main():
    df_bee = pd.read_csv("silver/cleaned_bees.csv")
    df_bloom = pd.read_csv("bronze/Bloomberg_Commodity_Historical_Data.csv")
    df_crops = pd.read_csv("silver/cleaned_crops.csv")
    df_top_items = pd.read_csv("gold/top_10_items_per_continent.csv")
    df_beeBloom = pd.read_csv("gold/corr_beeBloom_prodArea_Global.csv")


    #plot_bee_population_growth_by_continent(df_bee)
    #plot_bloom(df_bloom)
    #plot_flags(df_bee)

    #plot_corr_barplot(df_beeBloom, "Global")
    #plot_corr_heatmap(df_beeBloom,"Gobal")

    for continent in continents:
        df_continent = pd.read_csv(f"gold/corr_beeBloom_prodArea_{continent}.csv")
        #plot_corr_heatmap(df_continent, continent)
        plot_top_items_by_continent_pie(df_top_items, continent)



def plot_bee_population_growth_by_continent_barplot(df):
    continent_bees = df.groupby(["Year", "Continent"])["Bee_Values"].sum().unstack()

    plt.figure(figsize=(16, 8))

    continent_bees.plot(kind='bar', stacked=True, ax=plt.gca(), figsize=(16, 8))

    plt.xlabel("Year")
    plt.ylabel("Total Bee Population")
    plt.title("Total Bee Population by Continent Over Time")
    plt.legend(title="Continent")
    plt.tight_layout()
    plt.savefig("png/bee_population_growth_by_continent_BARPLOT.png")
    plt.show()


    ''' LINEPLOT
    continent_bees = df.groupby(["Year", "Continent"])["Bee_Values"].sum().unstack()
    global_bees = df.groupby("Year")["Bee_Values"].sum()

    plt.figure(figsize=(16, 8))

    for continent in continent_bees.columns:
        plt.plot(continent_bees[continent], label=continent)

    plt.plot(global_bees.index, global_bees.values, label="Global", color='black', linestyle='--', )

    plt.xlabel("Year")
    plt.ylabel("Total Bee Population")
    plt.title("Total Bee Population by Continent Over Time")
    plt.legend(title="Continent")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("png/bee_population_growth_by_continent_LINEPLOT.png")
    plt.show()
    '''

def plot_bloom_candlestick(df):
    # convert date
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['Year'] = df['Date'].dt.year
    df = df.sort_values('Date')

    fig, ax = plt.subplots(figsize=(16, 8))

    # widh candles
    width = 0.6

    # draw candles with color
    for i, (idx, row) in enumerate(df.iterrows()):
        if row['Open'] < row['Price']:  # up
            color = 'darkgreen'
        else:  # down
            color = 'red'

        body_bottom = min(row['Open'], row['Price'])
        body_height = abs(row['Price'] - row['Open'])

        rect = Rectangle(
            xy=(i - width / 2, body_bottom),
            width=width,
            height=body_height,
            facecolor=color,
            edgecolor=color,
            alpha=1
        )
        ax.add_patch(rect)

        # draw wicks
        ax.plot([i, i], [row['Low'], row['High']], color='black', linewidth=1)

    # x on 5 year intervall
    unique_years = sorted(df['Year'].unique())
    five_year_ticks = [year for year in unique_years if year % 5 == 0]

    # posisitons for the years
    tick_positions = []
    for year in five_year_ticks:
        year_data = df[df['Year'] == year]
        if not year_data.empty:
            first_idx_in_year = list(df[df['Year'] == year].index)[0]
            position = df.index.get_loc(first_idx_in_year)
            tick_positions.append(position)

    plt.xticks(tick_positions, five_year_ticks)
    plt.title('Bloomberg Candlestick Chart')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.grid(True, alpha=0.3)

    # MA
    df['MA10'] = df['Price'].rolling(window=10).mean()

    x_values = range(len(df))
    plt.plot(x_values, df['MA10'].values, color='gray', linewidth=1, label='10-Day MA')
    plt.legend()
    plt.tight_layout()
    plt.savefig('png/bloomberg_candlestick.png', dpi=300)
    plt.show()


def plot_flags_pie(df):
    total_flags = df["Flag Description"].value_counts()

    fig, ax = plt.subplots(figsize=(9,9))
    wedges, texts = ax.pie(total_flags, labels=None)

    ax.legend(wedges, total_flags.index, title="Flag Description", loc="best", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("png/flags.png")
    plt.show()

def plot_top_items_by_continent_pie(df, continent):
    total_continents = df[df["Continent"] == continent]
    item_totals = total_continents.groupby("Item")["Crop_Values"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 9))
    wedges, texts = ax.pie(item_totals, labels=None)

    ax.legend(wedges, item_totals.index, title="Items", loc="best", bbox_to_anchor=(1, 0.5))
    ax.set_title(f'Top Items by Crop Value in {continent}')
    plt.tight_layout()
    plt.savefig(f"png/top_items_pie_{continent}.png")


def plot_corr_barplot(df, continent):
    df_sorted = df.sort_values(by='bee_prod_corr', ascending=False)

    ffig, ax = plt.subplots(1, 1, figsize=(max(14, len(df_sorted) * 0.5), 7))  # Angepasste figsize für einen einzelnen Plot

    sns.barplot(ax=ax, x='Item', y='bee_prod_corr', data=df_sorted, color='orange', label='Bee Productivity Corr')

    ax.set_title(f'{continent} - Correlation Between Bees Population and Productivity by Crop', fontsize=16)
    ax.set_ylabel('Correlation Coefficient', fontsize=12)
    ax.legend(loc='best')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_xticklabels(df_sorted['Item'], rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(f'png/correlation_barplot_{continent}.png', dpi=300)
    plt.show()

def plot_corr_heatmap(df, continent):
    plt.figure(figsize=(max(12, len(df) * 1.1), 8))

    # Neue Reihenfolge: Erst alle Bee-Spalten, dann alle Commodity-Spalten
    corr_data = df.set_index('Item')[[
        #'bee_commodity_corr',
        'bee_prod_corr',
        'bee_area_corr',
        #'bee_yield_corr',
        #'commodity_prod_corr',
        #'commodity_area_corr',
        #'commodity_yield_corr',
    ]].T

    # Labels entsprechend der neuen Reihenfolge
    corr_data.index = [
        #'Bee-Commodity',
        'Bee-Productivity',
        'Bee-Area Harvested',
        #'Bee-Yield',
        #'Commodity-Productivity',
        #'Commodity-Area',
        #'Commodity-Yield',
    ]

    cmap = sns.diverging_palette(20, 260, as_cmap=True)
    vmin = min(corr_data.min().min(), 0)
    vmax = max(corr_data.max().max(), 1)

    sns.heatmap(corr_data, annot=True, cmap=cmap, vmin=vmin, vmax=vmax, fmt=".2f", linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title(f'{continent} - Correlation Coefficients ', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'png/correlation_heatmap_{continent}.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    main()