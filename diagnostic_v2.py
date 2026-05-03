import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv(r"csv/crop_recomendation.csv")

# Check for duplicates
print("Duplicates:", df.duplicated().sum())

# Check feature ranges
print("\nFeature stats:")
print(df.describe())

# Check if labels are clean
print("\nUnique labels:")
print(df['label'].unique())

# Check correlation of features with label
le = LabelEncoder()
df['label_enc'] = le.fit_transform(df['label'])
print("\nCorrelation with label:")
# Dropping non-numeric columns for correlation if any, but here only label is non-numeric
numeric_df = df.select_dtypes(include=['number'])
print(numeric_df.corr()['label_enc'].sort_values())
