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

# STEP 1: Load the unified data file
file_path = "unified_emission_anomaly_data.csv"
df = pd.read_csv(file_path)

# STEP 2: Define target and features
target_cols = ['scope1_emissions_kg', 'scope2_emissions_kg', 'scope3_emissions_kg']
feature_cols = [col for col in df.columns if col not in target_cols]

# Prepare X and y
X = df[feature_cols].copy()
y = df[target_cols].copy()

# Save identifiers separately (optional, useful for grouping/reporting)
ids = X[['part_id', 'process_type', 'record_date']] if 'record_date' in X.columns else X[['part_id', 'process_type']]

# Drop identifiers that shouldn't be used as features
X_features = X.drop(columns=['part_id', 'record_date'] if 'record_date' in X.columns else ['part_id'])

# STEP 3: Encode categorical `process_type`
categorical_features = ['process_type']
categorical_transformer = OneHotEncoder(drop='first', handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[('cat', categorical_transformer, categorical_features)],
    remainder='passthrough'
)

# STEP 4: Pipeline with RandomForest for Multi-Output Regression
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42)))
])

# STEP 5: Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_features, y, test_size=0.2, random_state=42)

# STEP 6: Train
pipeline.fit(X_train, y_train)

# STEP 7: Evaluate
y_pred = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("✅ Evaluation Results:")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"R² Score: {r2:.4f}")

# STEP 8: Predict on full data
y_pred_full = pipeline.predict(X_features)
df[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']] = y_pred_full

# STEP 9: Grouped Reporting

# Emissions per part
part_level = df.groupby('part_id')[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']].sum().reset_index()
part_level['Total_CO2_per_part'] = part_level[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']].sum(axis=1)

# Emissions per process
process_level = df.groupby('process_type')[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']].sum().reset_index()
process_level['Total_CO2_per_process'] = process_level[['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3']].sum(axis=1)

# STEP 10: Plotting
plt.figure(figsize=(10, 6))
process_level.plot(x='process_type', y=['Pred_Scope1', 'Pred_Scope2', 'Pred_Scope3'], kind='bar', stacked=True)
plt.title("Emissions by Process Type")
plt.ylabel("kg CO2")
plt.tight_layout()
plt.grid(True)
plt.show()

# STEP 11: Export
df.to_csv("full_predictions_per_row.csv", index=False)
part_level.to_csv("emissions_per_part.csv", index=False)
process_level.to_csv("emissions_per_process.csv", index=False)

print("📁 Files Saved:")
print("- full_predictions_per_row.csv")
print("- emissions_per_part.csv")
print("- emissions_per_process.csv")



import subprocess
subprocess.run(["python3", "deepseekSCOPE.py"])
subprocess.run(["python3" , "EmissionAnomalyDectection.py"])
subprocess.run(["python3" , "TrackProgressTowardsNetZero.py"])
