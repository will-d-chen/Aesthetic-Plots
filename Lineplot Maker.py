import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

# Define the file names and colors
files = ['Isra_powered', 'Isra_noexo', 'Isra_unpowered']
colors = sns.color_palette('husl', 8)
sns.set_style("ticks")
sns.set_context("poster")

# Read the data from the Excel files and skip the first 100 rows
data = {}
for file in files:
    df = pd.read_excel(file + '.xlsx', usecols=[0, 2], header =1)
    transformed_data = df.copy()
    transformed_data.iloc[:, 1] = (transformed_data.iloc[:, 1] * 16.58 + transformed_data.iloc[:, 1] * 0.85 * 4.51) / 1000 * 16.67  # Transformation equation applied to the 12th column
    data[file] = transformed_data.values

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))
for i, file in enumerate(files):
    smooth_data = lowess(data[file][:, 1], data[file][:, 0], frac=0.12)  # Smooth the data (ignoring first 100 data points)
    x_values = smooth_data[:, 0]
    y_values = smooth_data[:, 1]
  
    # Limit x-axis range to 0-250
    valid_indices = (x_values >= 0) & (x_values <= 360)
    ax.plot(x_values[valid_indices], y_values[valid_indices], color=colors[7-i], label=file, linewidth=4, alpha=0.9)  # Plot the smoothed data

# Add labels and legend
ax.set_xlabel('Time (Seconds)')
ax.set_ylabel('Metabolics (W/kg)')
ax.set_title('2023-7-7 outdoor hiking')

ax.legend(loc='lower right', fontsize='x-small')
sns.despine(offset=1, trim=True)

plt.show()
