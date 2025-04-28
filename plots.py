import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Read data from CSV file
def main():
    df_bee = pd.read_csv("silver/cleaned_bees.csv")
    df_beeBloom = pd.read_csv("gold/corr_beeBloom_prodArea.csv")

    plot_bee_population_growth_by_continent(df_bee)
    #plot_flags(df_bee)
    #plot_corr_heatmap(df_beeBloom)


def plot_bee_population_growth_by_continent(df):
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


    '''
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

# plt.savefig("png/bee_population_growth_by_continent_LINEPLOT.png")

def plot_bloom():
    ...

    '''TODO: Simple Linechart '''

def plot_overlying_beeBloom():
    ...
    '''TODO: Bee, Bloom in one Line chart '''


def plot_flags(df):

    total_flags = df["Flag Description"].value_counts()

    fig, ax = plt.subplots(figsize=(9,9))
    wedges, texts = ax.pie(total_flags, labels=None)

    ax.legend(wedges, total_flags.index, title="Flag Description", loc="best", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("png/flags.png")
    plt.show()



def plot_corr_heatmap(df):
    df_sorted = df.sort_values(by='bee_prod_corr', ascending=False)

    '''BAR PLOT'''
    ffig, ax = plt.subplots(1, 1, figsize=(max(14, len(df_sorted) * 0.5), 7)) # Angepasste figsize für einen einzelnen Plot

    sns.barplot(ax=ax, x='Item', y='bee_prod_corr', data=df_sorted, color='orange', label='Bee Productivity Corr')

    ax.set_title('Correlation Between Bees Population and Productivity by Crop', fontsize=16)
    ax.set_ylabel('Correlation Coefficient', fontsize=12)
    ax.legend(loc='best')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_xticklabels(df_sorted['Item'], rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('png/bee_commodity_correlation.png', dpi=300)
    plt.show()

    ''' HEATMAP'''
    plt.figure(figsize=(max(12, len(df) * 1.1), 8))

    # Neue Reihenfolge: Erst alle Bee-Spalten, dann alle Commodity-Spalten
    corr_data = df.set_index('Item')[[
        'bee_commodity_corr',
        'bee_prod_corr',
        'bee_area_corr',
        #'bee_yield_corr',
        #'commodity_prod_corr',
        #'commodity_area_corr',
        #'commodity_yield_corr',
    ]].T

    # Labels entsprechend der neuen Reihenfolge
    corr_data.index = [
        'Bee-Commodity',
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
    plt.title('Correlation Coefficients: Bee Population and Commodity Prices', fontsize=16)
    plt.tight_layout()
    plt.savefig('png/correlation_heatmap.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    main()