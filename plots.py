import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from matplotlib.patches import Rectangle
import seaborn as sns

color_palette = [
        '#7286B7',
        '#9BADE6',
        '#D9E2FD',
        '#7DBAEF',
        '#344F6A'
    ]

def main():
    df_bee = pd.read_csv("silver/cleaned_bees_global.csv")
    #df_agro = pd.read_csv("silver/cleaned_agro.csv")
    #df_crops = pd.read_csv("silver/cleaned_crops_europe.csv.csv")
    #df_lr = pd.read_csv("gold/regression_analysis_lr.csv")
    #df_bloom = pd.read_csv("bronze/Bloomberg_Commodity_Historical_Data.csv")
    #df_corr = pd.read_csv("gold/corr_Crops_Bees_europe.csv")

    #plot_bee_population_growth_by_continent_line(df_bee)
    #plot_legend_only(df_bee)

    #plot_flags_pie(df_bee)
    #visualize_data_with_fstat()
    #plot_three_quarter_pie()

    #plot_corr_heatmap(df_corr,"Europe")


def plot_bee_population_growth_by_continent_line(df):
    continent_bees = df.groupby(["Year", "Continent"])["Bee_Values"].sum().unstack()

    plt.figure(figsize=(16, 8))

    for i, continent in enumerate(continent_bees.columns):
        plt.plot(continent_bees[continent],
                 color=color_palette[i % len(color_palette)],
                 linewidth=2.5)

    plt.axis('off')
    plt.grid(False)
    plt.gca().set_facecolor('none')
    plt.gcf().patch.set_alpha(0.0)

    plt.tight_layout()
    plt.savefig("png/01_bee_population_growth_by_continent_LINEPLOT.png", dpi=300, bbox_inches='tight',
                transparent=True)
    plt.show()

def plot_legend_only(df):
    continent_bees = df.groupby(["Year", "Continent"])["Bee_Values"].sum().unstack()

    plt.figure(figsize=(4, 2))


    handles = []
    labels = []
    for i, continent in enumerate(continent_bees.columns):
        handle, = plt.plot([], [],
                           color=color_palette[i % len(color_palette)],
                           linewidth=2.5,
                           label=continent)
        handles.append(handle)
        labels.append(continent)


    legend = plt.legend(handles=handles,
                        labels=labels,
                        title="Continent",
                        title_fontsize=12,
                        fontsize=10,
                        framealpha=1,
                        facecolor='white',
                        loc='center')

    plt.axis('off')
    plt.gca().set_facecolor('none')
    plt.gcf().patch.set_alpha(0.0)

    plt.tight_layout()
    plt.savefig("png/legend_only.png", dpi=300, bbox_inches='tight', transparent=True)
    plt.show()


def plot_flags_pie(df):
    total_flags = df["Flag Description"].value_counts().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 9))

    wedges, texts = ax.pie(total_flags,
                           labels=None,
                           colors=color_palette[:len(total_flags)],
                           startangle=90,
                           wedgeprops={'linewidth': 1, 'edgecolor': 'white'})

    ax.legend(wedges,
              total_flags.index,
              title="Flag Description",
              loc="best",
              bbox_to_anchor=(1, 0.5),
              fontsize=10,
              title_fontsize=12)

    plt.title("Distribution of Flag Descriptions",
              fontsize=14,
              pad=20)

    plt.setp(texts, size=10, weight="bold")

    plt.tight_layout()
    plt.savefig("png/01_flags.png", dpi=300, bbox_inches='tight')
    plt.show()


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

    corr_data = df.set_index('Item')[[
        'bee_prod_corr',
        'bee_area_corr',
    ]].T

    corr_data.index = [
        'Bee-Productivity',
        'Bee-Area Harvested',
    ]

    cmap = sns.diverging_palette(20, 260, as_cmap=True)
    vmin = min(corr_data.min().min(), 0)
    vmax = max(corr_data.max().max(), 1)

    sns.heatmap(corr_data, annot=True, cmap=cmap, vmin=vmin, vmax=vmax, fmt=".2f", linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title(f'{continent} - Correlation Coefficients ', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'png/correlation_heatmap_{continent}.png', dpi=300)
    plt.show()


def visualize_data_with_fstat():
    mu = 0
    sigma = 1
    t_stat = 1.420
    critical_value = 1.645

    x = np.linspace(-4, 4, 1000)
    y = norm.pdf(x, mu, sigma)

    # Erstelle den Plot
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, color='#7286B7', label='Normal distribution (H₀)')
    plt.fill_between(x, 0, y, where=(x >= critical_value), color='red', alpha=0.5,
                     label='Significant Area (p < 0.05)')

    plt.axvline(x=0, color='#7286B7', linestyle='--')
    plt.axvline(x=t_stat, color='white', linestyle='--', label='T-Statistics (1.420)')

    plt.xlabel('')
    plt.ylabel('')
    plt.title('Normalverteilung mit Signifikanzniveau (α = 0.05)')
    #plt.legend()
    plt.tight_layout()
    plt.grid(False)
    plt.savefig("png/03_linear_regression.png", transparent=True, dpi=300)
    plt.show()


def plot_three_quarter_pie():
    sizes = [75,25]

    fig, ax = plt.subplots(figsize=(9, 9))

    wedges, texts = ax.pie(sizes,
                           labels=None,
                           colors=color_palette[:len(sizes)],
                           startangle=90,
                           wedgeprops={'linewidth': 1, 'edgecolor': 'white'})

    plt.tight_layout()
    plt.savefig("png/01_three_quarter.png", dpi=300, bbox_inches='tight', transparent=True,)
    plt.show()



if __name__ == '__main__':
    main()