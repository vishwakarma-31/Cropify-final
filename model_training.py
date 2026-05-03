import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

df = pd.read_csv(r"csv/Crop_recommendation.csv")

X = df.drop("label", axis=1)
y = df["label"]

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Train models
rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
mlp = MLPClassifier(hidden_layer_sizes=(100,50), max_iter=1000, random_state=42).fit(X_train, y_train)
dt = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
nb = GaussianNB().fit(X_train, y_train)

# Print results
for name, model in [("Random Forest", rf), ("MLP", mlp), ("Decision Tree", dt), ("Naive Bayes", nb)]:
    preds = model.predict(X_test)
    print(f"{name}: {accuracy_score(y_test, preds)*100:.2f}%")
    print(classification_report(y_test, preds, target_names=le.classes_))
    print("---")

# Save models
joblib.dump(rf, r"random_forest.pkl")
joblib.dump(mlp, r"MLP.pkl")
joblib.dump(dt, r"random_tree.pkl")
joblib.dump(nb, r"naive_bayes.pkl")
joblib.dump(le, r"label_encoder.pkl")

print("Done")