import pandas as pd
import os
from openai import OpenAI

# Paths to check
files_to_check = [
    "ml_predictions_with_hotspots.csv",
]

# Wait until all CSV files are present
for f in files_to_check:
    if not os.path.exists(f):
        raise FileNotFoundError(f"Missing file: {f}")

# Load the CSVs
part_df = pd.read_csv("ml_predictions_with_hotspots.csv")

# Convert to text for LLM (truncate to top rows)
def df_to_text(df, label):
    return f"\n--- {label} ---\n" + df.head(10).to_string(index=False)

combined_data = (
    df_to_text(part_df, "suggest optimization strategies of Machine Learning predictions with emission hotspots") 
)

# Prompt to DeepSeek
prompt = f"""
You are a sustainability expert AI assistant.

Below is emissions data from a manufacturing process in three CSVs:

{combined_data}

Tasks:
1. Summarize key insights from CSV File.
2. Detect any emission spikes or outliers.
3. Provide optimization strategies to reduce emissions at a granular level.
4. Suggest how this factory can better track toward Net Zero.

refer to this project description and answer occording to it :

Sakthi Auto Component Limited is committed to achieving Carbon Net Zero by 2040 across its operations. However, existing systems lack the ability to measure, analyze, and reduce emissions at a granular level. There is an urgent need for a digital solution that can monitor real-time carbon footprints across different departments (melting, machining, dispatch, etc.), recommend actionable emission reduction strategies, and track the effectiveness of interventions over time. The system should also support carbon offset integration and reporting aligned with global sustainability frameworks.
Expected Outcomes:
A comprehensive digital platform that:
1) Calculates Scope 1, 2, and 3 emissions at process and part level

2) Uses AI/ML to identify emission hotspots and suggest optimization strategies

3) Tracks progress toward Net Zero milestones (2028, 2032, 2040)

4) Integrates carbon offset and afforestation project data

5) Generates audit-ready reports

6) Provides dashboards for internal ESG reporting
Requirements:
1) Must support multi-department emission tracking

2) Real-time data ingestion from logs

3) Emission factor library for fuels, materials, and transport

4) Role-based access and audit logs

5) Scalability for enterprise-wide rollout

"""

# OpenRouter DeepSeek setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # Replace this
)

completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "https://your-website.com",  # Optional
        "X-Title": "NetZeroCarbonAI"
    },
    model="deepseek/deepseek-r1:free",
    messages=[{"role": "user", "content": prompt}]
)

# Output result
output = completion.choices[0].message.content
print("\n🔍 DeepSeek Analysis:\n")
print(output)

# Optional: Save to file
with open("deepseek_analysis.txt", "w") as f:
    f.write(output)
