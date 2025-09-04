import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, classification_report

# Load dataset using a raw string (r"...") to handle the file path correctly.
df = pd.read_csv(r"csv/crop_recomendation.csv")

# --- CORRECTION ---
# The target column (the one you want to predict) is most likely named 'label'.
# The previous errors happened because neither 'Crop' nor 'crop' were correct.
X = df.drop('label', axis=1)
y = df['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Tree Classifier (using random splits)
random_tree = DecisionTreeClassifier(splitter='random', random_state=42)
random_tree.fit(X_train, y_train)

# Make predictions
y_pred = random_tree.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Display results
print("Random Tree Model Accuracy:", accuracy)
print("\nClassification Report:\n", report)

# Optional: Print tree decision rules
print("\nDecision Tree Rules:\n")
tree_rules = export_text(random_tree, feature_names=list(X.columns))
print(tree_rules)