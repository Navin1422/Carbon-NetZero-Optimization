import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Simulated manufacturing dataset
np.random.seed(42)
n_samples = 100
data = pd.DataFrame({
    'energy_consumed_kwh': np.random.uniform(100, 1000, n_samples),
    'fuel_consumed_liters': np.random.uniform(10, 100, n_samples),
    'production_volume_units': np.random.randint(50, 500, n_samples),
    'machine_hours': np.random.uniform(10, 50, n_samples),
    'temperature_c': np.random.uniform(20, 40, n_samples)
})

# Emissions formula (simplified with emission factors)
data['scope1_emissions_kg'] = data['fuel_consumed_liters'] * 2.68  # Diesel ~2.68 kg CO₂/liter
data['scope2_emissions_kg'] = data['energy_consumed_kwh'] * 0.92   # Grid intensity ~0.92 kg CO₂/kWh

# Split
X = data.drop(['scope1_emissions_kg', 'scope2_emissions_kg'], axis=1)
y = data[['scope1_emissions_kg', 'scope2_emissions_kg']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)

# Plot actual vs predicted
plt.figure(figsize=(10, 5))
plt.scatter(y_test['scope1_emissions_kg'], y_pred[:, 0], label='Scope 1', alpha=0.7)
plt.scatter(y_test['scope2_emissions_kg'], y_pred[:, 1], label='Scope 2', alpha=0.7)
plt.plot([0, max(y_test.max())], [0, max(y_test.max())], 'r--')
plt.xlabel("Actual Emissions (kg CO2)")
plt.ylabel("Predicted Emissions (kg CO2)")
plt.title("Actual vs Predicted Emissions")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
