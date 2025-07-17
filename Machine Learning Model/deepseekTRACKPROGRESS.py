import pandas as pd
import os
from openai import OpenAI

# Paths to check
files_to_check = [
    "track_progress_output.csv",
]

# Wait until all CSV files are present
for f in files_to_check:
    if not os.path.exists(f):
        raise FileNotFoundError(f"Missing file: {f}")

# Load the CSVs
part_df = pd.read_csv("track_progress_output.csv")

# Convert to text for LLM (truncate to top rows)
def df_to_text(df, label):
    return f"\n--- {label} ---\n" + df.head(10).to_string(index=False)

combined_data = (
    df_to_text(part_df, "Emissions per Part") 
)

# Prompt to DeepSeek
prompt = f"""
You are a sustainability and emissions forecasting expert AI assistant.

Below is emissions data from a manufacturing facility, including actual yearly emissions, predicted future emissions, and declared Net Zero targets.

{combined_data}

Tasks:
1. Identify patterns or anomalies in the actual vs predicted emissions.
2. Compare the forecasted emissions against Net Zero targets — where are the biggest gaps?
3. Suggest short-term and long-term strategies to reduce Scope 1, 2, and 3 emissions effectively.
4. Recommend data-driven actions to help this facility stay on track for Net Zero by 2040.
5. If the predicted path fails to meet targets, explain why and how it can be corrected.
Be precise, practical, and insights-driven.
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
