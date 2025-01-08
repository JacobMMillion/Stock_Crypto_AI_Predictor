from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import pandas as pd

# Load data
df = pd.read_csv('labeled_stock_data.csv')

# Train-test split (same as your original code)
train = df.iloc[:-400]  # Train on all data except the last 400
test = df.iloc[-400:]   # Test on the last 400 rows

# Define the predictors
predictors = ["open", "high", "low", "close", "volume"]

# Initialize the model, `balanced` gives higher priority to underrepresented class
model = RandomForestClassifier(random_state=1, class_weight='balanced')

# Parameter grid for GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10, 100],
}

# Create TimeSeriesSplit object
tscv = TimeSeriesSplit(n_splits=5)

# Initialize GridSearchCV with TimeSeriesSplit
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=tscv, n_jobs=-1, verbose=1)

# Fit grid search to the training data
grid_search.fit(train[predictors], train['label'])

# Print best parameters from grid search
print(f"Best parameters found: {grid_search.best_params_}")

# Now use the best parameters found in the grid search to fit the final model
best_model = grid_search.best_estimator_

# Fit the model using the best found parameters
best_model.fit(train[predictors], train['label'])

# Predict on the test set
predictions = best_model.predict(test[predictors])

# Print model statistics
print("------------------------")
print("STOCK MODEL STATS")
print("Predictions:")
print(predictions)

# Calculate precision
score = precision_score(test['label'], predictions)

# Calculate other metrics
accuracy = accuracy_score(test['label'], predictions)
recall = recall_score(test['label'], predictions)
f1 = f1_score(test['label'], predictions)
conf_matrix = confusion_matrix(test['label'], predictions)

# Print the results
print(f"Precision: {score}")
print(f"Accuracy: {accuracy}")
print(f"Recall: {recall}")
print(f"F1-Score: {f1}")
print(f"Confusion Matrix:\n{conf_matrix}")
true_positives = ((predictions == 1) & (test['label'] == 1)).sum()
print(f"True Positives (Predicted 1 and Actual 1): {true_positives}")
true_negatives = ((predictions == 0) & (test['label'] == 0)).sum()
print(f"True Negatives (Predicted 0 and Actual 0): {true_negatives}")
false_positives = ((predictions == 1) & (test['label'] == 0)).sum()
print(f"False Positives (Predicted 1 and Actual 0): {false_positives}")
false_negatives = ((predictions == 0) & (test['label'] == 1)).sum()
print(f"False Negatives (Predicted 0 and Actual 1): {false_negatives}")
print("------------------------")

# Predict the label for the next day using the trained model
df = pd.read_csv('cleaned_stock_data.csv')
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