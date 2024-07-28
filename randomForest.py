import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

dataset = pd.read_csv("./dataset.csv")
dataset = dataset.drop('index', axis=1) # Drop index column as it's not needed

x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Ensure y is a 1D array
y = y.ravel()

# Splitting the dataset into training set and test set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Applying grid search to find best performing parameters 
parameters = [{'n_estimators': [100, 700],
    'max_features': ['sqrt', 'log2'],
    'criterion': ['gini', 'entropy']}]

grid_search = GridSearchCV(RandomForestClassifier(), parameters, cv=5, n_jobs=-1)
grid_search.fit(x_train, y_train)

acc = grid_search.best_score_
print("Best Accuracy =", str(acc* 100), " %")

print("Best Accuracy =", str(acc))
print("Best parameters =", str(grid_search.best_params_))

# Fitting RandomForest regression with best params 
best_params = grid_search.best_params_
classifier = RandomForestClassifier(n_estimators=best_params['n_estimators'], 
                                    criterion=best_params['criterion'], 
                                    max_features=best_params['max_features'],  
                                    random_state=0)
classifier.fit(x_train, y_train)

# Predicting the test set results
y_pred = classifier.predict(x_test)

# Cross-validation score
from sklearn.model_selection import cross_val_score
val_score = cross_val_score(classifier, x_train, y_train, cv=3, scoring='accuracy').mean()
print(f"Cross-validation score: {val_score}")

# Confusion matrix
from sklearn.metrics import confusion_matrix, pair_confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Pickle file joblib
joblib.dump(classifier, './randomForest.pkl', protocol=4)

# _data = np.array(data, dtype=dtype, copy=copy,
# Best Accuracy = 97.23787565139813  %
# Best Accuracy = 0.9723787565139812
# Best parameters = {'criterion': 'gini', 'max_features': 'log2', 'n_estimators': 100}
# Cross-validation score: 0.9677962738614582
# [[1181   68]
#  [  19 1496]]
