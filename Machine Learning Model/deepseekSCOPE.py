import pandas as pd
import os
from openai import OpenAI

# Paths to check
files_to_check = [
    "emissions_per_part.csv",
    "emissions_per_process.csv",
    "full_predictions_per_row.csv"
]

# Wait until all CSV files are present
for f in files_to_check:
    if not os.path.exists(f):
        raise FileNotFoundError(f"Missing file: {f}")

# Load the CSVs
part_df = pd.read_csv("emissions_per_part.csv")
process_df = pd.read_csv("emissions_per_process.csv")
row_df = pd.read_csv("full_predictions_per_row.csv")

# Convert to text for LLM (truncate to top rows)
def df_to_text(df, label):
    return f"\n--- {label} ---\n" + df.head(10).to_string(index=False)

combined_data = (
    df_to_text(part_df, "Emissions per Part") +
    df_to_text(process_df, "Emissions per Process") +
    df_to_text(row_df, "Full Predictions per Row")
)

# Prompt to DeepSeek
prompt = f"""
You are a sustainability expert AI assistant.

Below is emissions data from a manufacturing process in three CSVs:

{combined_data}

Tasks:
1. Summarize key insights from each CSV.
2. Detect any emission spikes or outliers.
3. Provide optimization strategies to reduce Scope 1, 2, and 3 emissions.
4. Suggest how this factory can better track toward Net Zero.
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
