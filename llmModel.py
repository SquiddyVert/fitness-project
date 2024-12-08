import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Sample workout log data
# Features: avg_sets, avg_reps, avg_calories_burned, etc.
data = {
    'avg_sets': [5, 6, 4, 7, 3],
    'avg_reps': [10, 12, 9, 11, 8],
    'avg_calories_burned': [300, 350, 280, 400, 250],
    'avg_heart_rate': [120, 130, 115, 125, 110],
    'weight_change_per_month': [-1, -2, 0, -3, -1.5],  # in kg
    'Goal_Achievement': [1, 1, 0, 1, 0]  # 1 if goal was achieved, 0 if not
}

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Define features (X) and target (y)
X = df.drop(columns='Goal_Achievement')
y = df['Goal_Achievement']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Example: Predict whether a new user's goal will be achieved
new_user_data = pd.DataFrame({
    'avg_sets': [6],
    'avg_reps': [11],
    'avg_calories_burned': [320],
    'avg_heart_rate': [125],
    'weight_change_per_month': [-2]
})

# Make prediction
prediction = model.predict(new_user_data)
print(f"Will the user achieve their goal? {'Yes' if prediction[0] == 1 else 'No'}")