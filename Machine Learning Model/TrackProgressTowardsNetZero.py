# STEP 1: Import dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# STEP 2: Simulate historical emissions
data = {
    'year': np.arange(2015, 2025),
    'emissions': [5000, 4950, 4800, 4700, 4600, 4500, 4350, 4300, 4200, 4100]
}
df = pd.DataFrame(data)

# STEP 3: Prepare data for Linear Regression
X = df['year'].values.reshape(-1, 1)
y = df['emissions'].values

model = LinearRegression()
model.fit(X, y)

# STEP 4: Predict future values till 2040
future_years = np.arange(2025, 2041).reshape(-1, 1)
predicted_emissions = model.predict(future_years)

# STEP 5: Plot actual, predicted, and targets
targets = {2028: 3000, 2032: 1800, 2040: 0}
target_df = pd.DataFrame({'year': list(targets.keys()), 'target': list(targets.values())})

plt.figure(figsize=(12, 6))
plt.plot(df['year'], df['emissions'], label='Actual Emissions', marker='o')
plt.plot(future_years, predicted_emissions, label='Linear Regression Forecast', linestyle='--')
plt.scatter(target_df['year'], target_df['target'], color='red', label='Net Zero Targets', zorder=5)

plt.title('📉 Linear Regression: Emissions vs Net Zero Targets (2015–2040)')
plt.xlabel('Year')
plt.ylabel('Total Emissions (Tonnes CO₂)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
