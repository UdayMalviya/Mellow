import pandas as pd
import ollama
import json
import tempfile

def clean_with_ai(df: pd.DataFrame) -> pd.DataFrame:
    # Convert the DataFrame to a CSV string for input
    csv_data = df.to_csv(index=False)

    prompt = f"""
You are a data cleaning assistant. Given a CSV, your job is to clean it by:
- Handling missing values (drop or impute),
- Removing duplicates,
- Converting datatypes if needed,
- Fixing obvious anomalies or typos,
- Making sure the data is ready for analysis.

Respond only with a cleaned CSV, no explanations.

CSV input:
{csv_data}
"""

    # Call Ollama locally using the Mistral model
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    cleaned_csv = response["message"]["content"]

    # Write cleaned CSV to a temp file and read back into DataFrame
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.csv') as tmp:
        tmp.write(cleaned_csv)
        tmp.seek(0)
        cleaned_df = pd.read_csv(tmp.name)

    return cleaned_df
