from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import pandas as pd

# Load data
df = pd.read_csv('labeled_crypto_data.csv')

# Train-test split
train = df.iloc[:-50]  # Train on all data except the last 50
test = df.iloc[-50:]   # Test on the last 50 rows

# Define the predictors
predictors = ["current_price", "market_cap", "total_volume"]

# Original model (parameters will be updated based on GridSearchCV results)
model = RandomForestClassifier(random_state=1, class_weight='balanced')

# Define the parameter grid for hyperparameter tuning
param_grid = {
    'n_estimators': [100, 200, 300],  # Example: Searching over different number of trees
    'max_depth': [10, 20, 30, None],   # Example: Searching over different depths of trees
    'min_samples_split': [2, 5, 10, 100]  # Example: Searching over different values for splitting nodes
}

# Create TimeSeriesSplit object for cross-validation
tscv = TimeSeriesSplit(n_splits=5)

# Initialize GridSearchCV with TimeSeriesSplit
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=tscv, n_jobs=-1, verbose=1)

# Fit grid search
grid_search.fit(train[predictors], train['label'])

# Print the best parameters found by GridSearchCV
print(f"Best parameters found: {grid_search.best_params_}")

# Reinitialize the model with the best parameters found from GridSearchCV
best_model = RandomForestClassifier(
    n_estimators=grid_search.best_params_['n_estimators'],
    max_depth=grid_search.best_params_['max_depth'],
    min_samples_split=grid_search.best_params_['min_samples_split'],
    random_state=1,
    class_weight='balanced'
)

# Fit the best model on the training data
best_model.fit(train[predictors], train["label"])

# Predict on the test set
predictions = best_model.predict(test[predictors])

# Print model stats
print("------------------------")
print("CRYPTO MODEL STATS")
print("Predictions:")
print(predictions)

# Calculate precision, recall, accuracy, and f1-score
precision = precision_score(test['label'], predictions)
accuracy = accuracy_score(test['label'], predictions)
recall = recall_score(test['label'], predictions)
f1 = f1_score(test['label'], predictions)
conf_matrix = confusion_matrix(test['label'], predictions)

# Print the results
print(f"Precision: {precision}")
print(f"Accuracy: {accuracy}")
print(f"Recall: {recall}")
print(f"F1-Score: {f1}")
print(f"Confusion Matrix:\n{conf_matrix}")

# Calculate True Positives, True Negatives, False Positives, False Negatives
true_positives = ((predictions == 1) & (test['label'] == 1)).sum()
true_negatives = ((predictions == 0) & (test['label'] == 0)).sum()
false_positives = ((predictions == 1) & (test['label'] == 0)).sum()
false_negatives = ((predictions == 0) & (test['label'] == 1)).sum()

print(f"True Positives: {true_positives}")
print(f"True Negatives: {true_negatives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")
print("------------------------")

# Predict on the next day's data
df = pd.read_csv('cleaned_crypto_data.csv')
next_day_data = df.iloc[0]
date = next_day_data["date"]

# Prepare the features for prediction (same as predictors)
next_day_features = pd.DataFrame(
    next_day_data[predictors].values.reshape(1, -1),
    columns=predictors
)

print(f"Running model on the current day ({date}):")
print(next_day_features)

# Predict the label for the next day
next_day_label = best_model.predict(next_day_features)

# Print the predicted label for the next day
print(f"Predicted Label for {date}: {next_day_label[0]}")
print("------------------------")