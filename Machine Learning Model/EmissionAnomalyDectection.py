# Install required packages if needed
# !pip install pandas scikit-learn matplotlib seaborn

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, IsolationForest
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 1: Load Manufacturing Data
file_path = "incoming_manufacturing_data.csv"  # Replace with the path or API input
df = pd.read_csv(file_path)

# 🔍 Expected Columns:
# ['energy_kwh', 'material_used_kg', 'operating_hours', 
#  'temperature_c', 'production_volume', 'efficiency_score', 'emissions_kg_co2' (optional for training)]

# STEP 2: Basic Validation
required_columns = ['energy_kwh', 'material_used_kg', 'operating_hours',
                    'temperature_c', 'production_volume', 'efficiency_score']

missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in input data: {missing_cols}")

# STEP 3: Preprocess
features = df[required_columns]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# STEP 4: Train Model (Only if 'emissions_kg_co2' is available)
if 'emissions_kg_co2' in df.columns:
    target = df['emissions_kg_co2']
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, target, test_size=0.2, random_state=42)

    gbr = GradientBoostingRegressor(random_state=42)
    grid = GridSearchCV(gbr, {
        'n_estimators': [100],
        'learning_rate': [0.1],
        'max_depth': [3]
    }, cv=3, scoring='r2')
    grid.fit(X_train, y_train)
    model = grid.best_estimator_

   # Evaluate
    y_pred = model.predict(X_test)
    print("✅ Model Evaluation:")
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"MSE: {mean_squared_error(y_test, y_pred):.2f}")
    print(f"R² Score: {r2_score(y_test, y_pred):.4f}")

    # 🔍 Feature Importance Plot
    importances = model.feature_importances_
    feat_imp_df = pd.DataFrame({
        'Feature': features.columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(8, 5))
    sns.barplot(x='Importance', y='Feature', data=feat_imp_df, palette='mako')
    plt.title("Feature Importance - Gradient Boosting")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    # Use pretrained model if training data is not available
    print("⚠️ No emissions_kg_co2 found — loading pretrained model instead.")
    # Example: model = joblib.load("trained_emission_model.pkl")
    raise ValueError("Pretrained model loading not implemented in this script.")

# STEP 5: Predict Emissions on All Data
df['Predicted_Emissions'] = model.predict(X_scaled)

# STEP 6: Emission Hotspot Detection
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

iso = IsolationForest(contamination=0.05, random_state=42)
df['anomaly'] = iso.fit_predict(X_scaled)
df['anomaly'] = df['anomaly'].map({1: 'normal', -1: 'hotspot'})
'''
# STEP 7: Visualization (Advanced Version — like first code)
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    x='energy_kwh', y='Predicted_Emissions',
    hue='cluster',
    style='anomaly',
    data=df,
    palette='Set1',
    s=70,
    linewidth=0.5,
    edgecolor='white'
)

# Title and labels
plt.title("Emission Hotspots via Clustering & Anomaly Detection")
plt.xlabel("Energy Consumed (kWh)")
plt.ylabel("Predicted Emissions (kg CO₂)")
'''
# STEP 7: Visualization (Static Color–Cluster Mapping)

# Define static cluster–color mapping
cluster_palette = {
    0: "red",
    1: "blue",
    2: "green"
}

# Define anomaly–style mapping
anomaly_styles = {
    'normal': 'o',
    'hotspot': 'X'
}

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# Define fixed color mapping
cluster_palette = {0: "red", 1: "blue", 2: "green"}
anomaly_styles = {'normal': 'o', 'hotspot': 'X'}

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='energy_kwh',
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

# Custom fixed legend
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


'''
# Fixing legend so it shows clearly
handles, labels = scatter.get_legend_handles_labels()
plt.legend(handles=handles, labels=labels, title='Legend', bbox_to_anchor=(1.05, 1), loc='upper left')
'''
plt.grid(True)
plt.tight_layout()
plt.show()


# STEP 8: Export or Return
df.to_csv("ml_predictions_with_hotspots.csv", index=False)
print("📁 Saved: ml_predictions_with_hotspots.csv")