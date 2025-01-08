from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import pandas as pd

"""
Trains and returns a random forest model
(assumes time series data being used)

The model has the following properties:
-random_state is 1
-class_weight is balanced
-n_estimators, max_depth, min_samples_split determined with GridSearchCV

GridSearchCV is used with a time series split, as we assume time series data
"""
def train_random_forest_model(predictors, train):

    # Original model (parameters will be updated based on GridSearchCV results)
    model = RandomForestClassifier(random_state=1, class_weight='balanced')

    # Create TimeSeriesSplit object for cross-validation
    tscv = TimeSeriesSplit(n_splits=5)

    # Define the parameter grid for hyperparameter tuning
    param_grid = {
        'n_estimators': [100, 200, 300],  # Searching over different number of trees
        'max_depth': [2, 3, 5, 10],   # Searching over different depths of trees
        'min_samples_split': [2, 5, 10, 100]  # Searching over different values for splitting nodes
    }

    # Initialize GridSearchCV with TimeSeriesSplit
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=tscv, n_jobs=-1, verbose=1)

    # Fit grid search
    grid_search.fit(train[predictors], train['label'])
    print(f"Best parameters found in train_random_forest_model: {grid_search.best_params_}")

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

    return best_model

"""
Prints model statistics
Returns nothing
"""
def print_model_statistics(model_name, predictions, train, test):

    train_label = train['label']
    test_label = test['label']

    print("------------------------")
    print(f"{model_name} MODEL STATS")

    # print distribution of labels in training and test set
    print("Distribution of actual labels in train and test sets:")
    print("train distribution: \n", train_label.value_counts())
    print("test distribution: \n", test_label.value_counts())
    print("")

    print("Model predicted labels for test set:")
    print(predictions)
    print("")

    # Calculate precision, recall, accuracy, and f1-score
    precision = precision_score(test_label, predictions)
    accuracy = accuracy_score(test_label, predictions)
    recall = recall_score(test_label, predictions)
    f1 = f1_score(test_label, predictions)

    # Calculate True Positives, True Negatives, False Positives, False Negatives
    true_positives = ((predictions == 1) & (test_label == 1)).sum()
    true_negatives = ((predictions == 0) & (test_label == 0)).sum()
    false_positives = ((predictions == 1) & (test_label == 0)).sum()
    false_negatives = ((predictions == 0) & (test_label == 1)).sum()

    # Print the results
    print(f"Precision: {precision}")
    print(f"Accuracy: {accuracy}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1}")
    print(f"True Positives: {true_positives}")
    print(f"True Negatives: {true_negatives}")
    print(f"False Positives: {false_positives}")
    print(f"False Negatives: {false_negatives}")
    print("------------------------")

"""
Uses a model to predict whether the next day will see gain or loss
This function assumes that the most recent date is the first entry in the
JSON file passed in, also assumes there is a `date` column

Returns nothing, prints the info to console
"""
def predict_next_day(file_name, predictors, model):
    
    # Predict the label for the next day using the trained model
    df = pd.read_csv(file_name)
    next_day_data = df.iloc[0]
    date = next_day_data["date"]

    # Prepare the features for prediction (same as predictors)
    next_day_features = pd.DataFrame(
        next_day_data[predictors].values.reshape(1, -1),
        columns=predictors
    )

    print("------------------------")
    print(f"Running model on the current day ({date}):")
    print(next_day_features)

    # Predict the label for the next day
    next_day_label = model.predict(next_day_features)

    # Print the predicted label for the next day
    print(f"Predicted Label for {date}: {next_day_label[0]}")
    print("If 1, then the next day after the date is projected to be bullish")
    print("If 0, then the next day after the date is projected to be bearish")
    print("------------------------")