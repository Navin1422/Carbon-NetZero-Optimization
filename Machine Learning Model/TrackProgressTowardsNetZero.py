import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import warnings

# Suppress sklearn warning
warnings.filterwarnings("ignore", category=UserWarning)

# Step 1: Load and preprocess the data
df = pd.read_csv("unified_emission_anomaly_data.csv")
df['record_date'] = pd.to_datetime(df['record_date'])

# Step 2: Compute total emissions and add year column
df['total_emissions_kg'] = df[['scope1_emissions_kg', 'scope2_emissions_kg', 'scope3_emissions_kg']].sum(axis=1)
df['year'] = df['record_date'].dt.year

# Step 3: Aggregate emissions per year
yearly_emissions = df.groupby('year')['total_emissions_kg'].sum().reset_index()
yearly_emissions['actual_emissions_tonnes'] = yearly_emissions['total_emissions_kg'] / 1000

# Show current emissions
latest_year = yearly_emissions['year'].max()
latest_emission = yearly_emissions.loc[yearly_emissions['year'] == latest_year, 'actual_emissions_tonnes'].values[0]
print(f"📌 Current Emissions ({latest_year}): {latest_emission:.2f} tonnes CO₂")

# Step 4: Train model
X = yearly_emissions[['year']]
y = yearly_emissions['actual_emissions_tonnes']
model = LinearRegression()
model.fit(X, y)

# Step 5: Forecast
future_years = np.arange(X['year'].min(), 2041).reshape(-1, 1)
forecast = model.predict(future_years)

# Step 6: Define Net Zero targets
targets = {
    2028: 3000,
    2032: 1800,
    2040: 0
}
target_df = pd.DataFrame(list(targets.items()), columns=['year', 'net_zero_target'])

# Step 7: Merge actual, forecast, and targets
output_df = pd.DataFrame({
    'year': future_years.flatten(),
    'predicted_emissions_tonnes': forecast
})
output_df = pd.merge(output_df, yearly_emissions[['year', 'actual_emissions_tonnes']], on='year', how='left')
output_df = pd.merge(output_df, target_df, on='year', how='left')

# Step 8: Merge back into original full data CSV by year (many-to-one join)
df = pd.merge(df, output_df, on='year', how='left')

# Save full unified CSV with added fields
df.to_csv("unified_emission_anomaly_data.csv", index=False)

# Also save track_progress_output.csv
output_df.to_csv("track_progress_output.csv", index=False)
print("✅ File updated: unified_emission_anomaly_data.csv")
print("📁 File generated: track_progress_output.csv")

# Step 9: Plot
plt.figure(figsize=(12, 6))
plt.plot(yearly_emissions['year'], yearly_emissions['actual_emissions_tonnes'],
         label="Actual Emissions", marker='o', color='navy')
plt.plot(future_years.flatten(), forecast, '--', label="Forecasted Emissions", color='orange')
plt.scatter(target_df['year'], target_df['net_zero_target'], color='red',
            s=70, label="Net Zero Targets", zorder=5)
plt.title("📉 Emissions Forecast vs Net Zero Targets (2015–2040)")
plt.xlabel("Year")
plt.ylabel("Total Emissions (Tonnes CO₂)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Step 10: Optional call to DeepSeek
import subprocess
subprocess.run(["python3", "deepseekTRACKPROGRESS.py"])
