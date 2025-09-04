import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import joblib

# Load the dataset using a raw string for the path
# NOTE: The CSV file is likely named 'crop_recomendation.csv' from our previous work.
# I have used that name here. Change it if your file is different.
df = pd.read_csv(r"csv/crop_recomendation.csv")

# --- CORRECTION 1: Fix target column name ---
# The column is likely 'label', not 'Crop'.
X = df.drop("label", axis=1)
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
rf = RandomForestClassifier().fit(X_train, y_train)
mlp = MLPClassifier(max_iter=500, random_state=42).fit(X_train, y_train) # Added random_state for reproducibility
dt = DecisionTreeClassifier().fit(X_train, y_train)
nb = GaussianNB().fit(X_train, y_train)

# --- CORRECTION 2 & 3: Use raw strings for paths and fix filenames ---
# Save models with the correct .pkl extension
joblib.dump(rf, r"C:\Projects\Cropify\CROPIFY_ML-main\random_forest.pkl")
joblib.dump(mlp, r"C:\Projects\Cropify\CROPIFY_ML-main\MLP.pkl")
joblib.dump(dt, r"C:\Projects\Cropify\CROPIFY_ML-main\random_tree.pkl")
joblib.dump(nb, r"C:\Projects\Cropify\CROPIFY_ML-main\naive_bayes.pkl")

print("✅ Models trained and saved successfully.")