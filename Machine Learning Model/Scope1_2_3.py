import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

np.random.seed(42)
n_samples = 100

# Simulate manufacturing + scope 3 features
data = pd.DataFrame({
    'energy_consumed_kwh': np.random.uniform(100, 1000, n_samples),
    'fuel_consumed_liters': np.random.uniform(10, 100, n_samples),
    'production_volume_units': np.random.randint(50, 500, n_samples),
    'machine_hours': np.random.uniform(10, 50, n_samples),
    'temperature_c': np.random.uniform(20, 40, n_samples),
    'material_weight_kg': np.random.uniform(100, 1000, n_samples),
    'transport_distance_km': np.random.uniform(10, 500, n_samples),
    'supplier_emission_rating': np.random.uniform(0.5, 2.0, n_samples),  # normalized score
    'packaging_weight_kg': np.random.uniform(5, 50, n_samples),
    'waste_kg': np.random.uniform(10, 200, n_samples)
})

# Emissions calculations (approx. emission factors)
data['scope1_emissions_kg'] = data['fuel_consumed_liters'] * 2.68  # Diesel
data['scope2_emissions_kg'] = data['energy_consumed_kwh'] * 0.92   # Grid
data['scope3_emissions_kg'] = (
    data['material_weight_kg'] * 1.9 +                   # Steel or composite
    (data['transport_distance_km'] * data['material_weight_kg'] / 1000) * 0.15 +  # Trucking
    data['supplier_emission_rating'] * 50 +              # Normalized factor
    data['packaging_weight_kg'] * 2.5 +                  # Plastic packaging
    data['waste_kg'] * 1.8                               # Mixed waste
)

# Features & targets
X = data.drop(['scope1_emissions_kg', 'scope2_emissions_kg', 'scope3_emissions_kg'], axis=1)
y = data[['scope1_emissions_kg', 'scope2_emissions_kg', 'scope3_emissions_kg']]
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

# Visualize predictions vs actuals
plt.figure(figsize=(12, 6))
plt.scatter(y_test['scope1_emissions_kg'], y_pred[:, 0], label='Scope 1', alpha=0.7)
plt.scatter(y_test['scope2_emissions_kg'], y_pred[:, 1], label='Scope 2', alpha=0.7)
plt.scatter(y_test['scope3_emissions_kg'], y_pred[:, 2], label='Scope 3', alpha=0.7)
plt.plot([0, max(y_test.max())], [0, max(y_test.max())], 'r--')
plt.xlabel("Actual Emissions (kg CO2)")
plt.ylabel("Predicted Emissions (kg CO2)")
plt.title("Actual vs Predicted Emissions (All Scopes)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
