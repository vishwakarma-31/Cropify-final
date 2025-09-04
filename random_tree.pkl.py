import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("csv/crop_prediction_dataset.csv")

# Split features and target
X = df.drop('Crop', axis=1)
y = df['Crop']

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