import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read data from CSV file
df = pd.read_csv("gold/corr_beeBloom_prodArea.csv")

# Prepare data for visualization
df_sorted = df.sort_values(by='bee_prod_corr', ascending=False)

# Create figure
plt.figure(figsize=(14, 10))

# Main plot: Bee correlation vs. Commodity Price correlation for productivity
plt.subplot(2, 1, 1)
sns.barplot(x='Item', y='bee_prod_corr', data=df_sorted, color='gold', label='Bee Productivity Correlation')
sns.barplot(x='Item', y='commodity_prod_corr', data=df_sorted, color='lightblue', alpha=0.7, label='Commodity Price Productivity Correlation')

plt.title('Correlation Between Bees/Commodity Prices and Productivity by Crop', fontsize=16)
plt.ylabel('Correlation Coefficient', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(loc='best')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Second plot: Bee correlation vs. Commodity Price correlation for cultivation area
plt.subplot(2, 1, 2)
sns.barplot(x='Item', y='bee_area_corr', data=df_sorted, color='orange', label='Bee Area Correlation')
sns.barplot(x='Item', y='commodity_area_corr', data=df_sorted, color='skyblue', alpha=0.7, label='Commodity Price Area Correlation')

plt.title('Correlation Between Bees/Commodity Prices and Cultivation Area by Crop', fontsize=16)
plt.ylabel('Correlation Coefficient', fontsize=12)
plt.xlabel('Crop Type', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(loc='best')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('png/bee_commodity_correlation.png', dpi=300)
plt.show()

# Heatmap with custom color scheme
plt.figure(figsize=(12, 8))
corr_data = df.set_index('Item')[['bee_prod_corr', 'commodity_prod_corr', 'bee_area_corr', 'commodity_area_corr']].T
# Rename the index for clarity in the heatmap
corr_data.index = ['Bee-Productivity Corr', 'Commodity-Productivity Corr',
                   'Bee-Area Corr', 'Commodity-Area Corr']

# Color parameter - change these values to modify colors
# First number (10) is for values near 0 (currently red)
# Second number (220) is for values near 1 (currently blue)
cmap = sns.diverging_palette(20, 260, as_cmap=True)

# Scale parameters
vmin = min(corr_data.min().min(), 0)
vmax = max(corr_data.max().max(), 1)

sns.heatmap(corr_data, annot=True, cmap=cmap, vmin=vmin, vmax=vmax, fmt=".2f")
plt.title('Correlation Coefficients: Bee Activity vs. Commodity Prices', fontsize=16)
plt.tight_layout()
plt.savefig('png/correlation_heatmap.png', dpi=300)
plt.show()