# Install if needed
# !pip install pandas scikit-learn matplotlib

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor
import matplotlib.pyplot as plt

# STEP 1: Load data (already uploaded or created)
file_path = "part_process_emission_data.csv"  # Replace if needed
df = pd.read_csv(file_path)

# STEP 2: Preprocess
X = df.drop(columns=['scope1_emissions_kg', 'scope2_emissions_kg', 'scope3_emissions_kg'])
y = df[['scope1_emissions_kg', 'scope2_emissions_kg', 'scope3_emissions_kg']]

# Keep IDs for grouping later
ids = X[['part_id', 'process_type']]
X_features = X.drop(columns=['part_id', 'process_type'])

# STEP 3: Encode categorical `process_type`
categorical_features = ['process_type']
categorical_transformer = OneHotEncoder(drop='first')

# Combine transformer in pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough'
)

# Final pipeline with regression
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42)))
])

# STEP 4: Train/Test split
X_trans = pd.concat([X[['process_type']], X_features], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X_trans, y, test_size=0.2, random_state=42)

# STEP 5: Train the model
pipeline.fit(X_train, y_train)

# STEP 6: Evaluate
y_pred = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("✅ Evaluation Results:")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"R² Score: {r2:.4f}")

# STEP 7: Predict on full data
X_full = pd.concat([X[['process_type']], X_features], axis=1)
y_pred_full = pipeline.predict(X_full)

df[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']] = y_pred_full

# STEP 8: Grouping logic for reporting

# 🔧 Total emissions per part
part_level = df.groupby('part_id')[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']].sum().reset_index()
part_level['Total_CO2_per_part'] = part_level[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']].sum(axis=1)

# 🔧 Total emissions per process
process_level = df.groupby('process_type')[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']].sum().reset_index()
process_level['Total_CO2_per_process'] = process_level[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']].sum(axis=1)

# STEP 9: Plotting results (optional)
plt.figure(figsize=(10, 6))
process_level.plot(x='process_type', y=['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3'], kind='bar', stacked=True)
plt.title("Emissions by Process Type")
plt.ylabel("kg CO2")
plt.tight_layout()
plt.grid(True)
plt.show()

# STEP 10: Export results
df.to_csv("full_predictions_per_row.csv", index=False)
part_level.to_csv("emissions_per_part.csv", index=False)
process_level.to_csv("emissions_per_process.csv", index=False)

print("📁 Saved:")
print("- full_predictions_per_row.csv")
print("- emissions_per_part.csv")
print("- emissions_per_process.csv")
