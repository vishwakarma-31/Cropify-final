import pandas as pd
df = pd.read_csv(r"csv/crop_recomendation.csv")
print(f"Shape: {df.shape}")
print("\nLabel Value Counts:")
print(df['label'].value_counts())
print("\nFirst 5 Rows:")
print(df.head())
