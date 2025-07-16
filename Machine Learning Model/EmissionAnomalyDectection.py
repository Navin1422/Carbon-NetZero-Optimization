import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, IsolationForest
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer


# STEP 1: Load the unified emission + anomaly data
file_path = "unified_emission_anomaly_data.csv"
df = pd.read_csv(file_path)

# STEP 2: Define features for anomaly detection
required_columns = [
    'energy_consumed_kwh', 'material_weight_kg', 'machine_hours',
    'transport_distance_km', 'supplier_emission_rating', 'packaging_weight_kg',
    'waste_kg', 'efficiency_score'
]

missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in input data: {missing_cols}")

# STEP 3: Prepare Features with Imputation
X = df[required_columns].copy()

# Fill missing values using median strategy
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

# Scale after imputation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)


# STEP 4: Train regression model if actual total emission is available
if {'scope1_emissions_kg', 'scope2_emissions_kg', 'scope3_emissions_kg'}.issubset(df.columns):
    df['total_emissions_kg'] = df[['scope1_emissions_kg', 'scope2_emissions_kg', 'scope3_emissions_kg']].sum(axis=1)
    target = df['total_emissions_kg']

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, target, test_size=0.2, random_state=42)

    gbr = GradientBoostingRegressor(random_state=42)
    grid = GridSearchCV(gbr, {
        'n_estimators': [100],
        'learning_rate': [0.1],
        'max_depth': [3]
    }, cv=3, scoring='r2')

    grid.fit(X_train, y_train)
    model = grid.best_estimator_

    y_pred = model.predict(X_test)

    print("✅ Emission Model Evaluation:")
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"MSE: {mean_squared_error(y_test, y_pred):.2f}")
    print(f"R² Score: {r2_score(y_test, y_pred):.4f}")

    # Plot feature importance
    importances = model.feature_importances_
    feat_imp_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(8, 5))
    sns.barplot(x='Importance', y='Feature', data=feat_imp_df, palette='mako')
    plt.title("Feature Importance - Gradient Boosting")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    raise ValueError("Missing total emissions columns for model training")

# STEP 5: Predict emissions on full dataset
df['Predicted_Emissions'] = model.predict(X_scaled)

# STEP 6: Clustering & Anomaly Detection
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

iso = IsolationForest(contamination=0.05, random_state=42)
df['anomaly'] = iso.fit_predict(X_scaled)
df['anomaly'] = df['anomaly'].map({1: 'normal', -1: 'hotspot'})

# STEP 7: Visualization
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

cluster_palette = {0: "red", 1: "blue", 2: "green"}
anomaly_styles = {'normal': 'o', 'hotspot': 'X'}

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='energy_consumed_kwh',
    y='Predicted_Emissions',
    hue='cluster',
    style='anomaly',
    data=df,
    palette=cluster_palette,
    markers=anomaly_styles,
    s=70,
    edgecolor='black'
)

plt.title("Emission Hotspots via Clustering & Anomaly Detection")
plt.xlabel("Energy Consumed (kWh)")
plt.ylabel("Predicted Emissions (kg CO₂)")
plt.grid(True)

# Custom legend
cluster_patches = [
    mpatches.Patch(color='red', label='cluster 0'),
    mpatches.Patch(color='blue', label='cluster 1'),
    mpatches.Patch(color='green', label='cluster 2')
]
anomaly_markers = [
    mlines.Line2D([], [], color='black', marker='o', linestyle='None', markersize=8, label='normal'),
    mlines.Line2D([], [], color='black', marker='X', linestyle='None', markersize=8, label='hotspot')
]

plt.legend(
    handles=cluster_patches + anomaly_markers,
    title='Legend',
    bbox_to_anchor=(1.05, 1),
    loc='upper left'
)

plt.tight_layout()
plt.show()

# STEP 8: Export
df.to_csv("ml_predictions_with_hotspots.csv", index=False)
print("📁 Saved: ml_predictions_with_hotspots.csv")


import subprocess
subprocess.run(["python3", "deepseekANOMALY.py"])