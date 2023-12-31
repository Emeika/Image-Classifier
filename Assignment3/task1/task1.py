import numpy as np
from sklearn.linear_model import SGDRegressor, RidgeCV, ElasticNetCV, LassoCV
from sklearn.linear_model import Ridge, ElasticNet, Lasso
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import GridSearchCV, KFold
import pickle
from sklearn.exceptions import ConvergenceWarning
import warnings
from flatten import *
from A2_task2 import *

# Extract features and labels for training and testing
X_train = np.vstack(strat_train_set['Image_Features'].values)
y_train = strat_train_set['Age'] 

X_test = np.vstack(strat_test_set['Image_Features'].values)
y_test = strat_test_set['Age'] 

# Step 1: GridSearchCV for SGDRegressor
param_grid_sgd = {'penalty': ["l2", "l1", "elasticnet", None],
                'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10]} 

sgd_reg = SGDRegressor()

# Create a 5-fold cross-validation object
kf = KFold(n_splits=5, shuffle=True, random_state=42)

grid_search_sgd = GridSearchCV(sgd_reg, param_grid_sgd, cv=kf, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_sgd.fit(X_train, y_train)

best_params_sgd = grid_search_sgd.best_params_
best_score_sgd = grid_search_sgd.best_score_
print("Best Parameters for SGDRegressor:", best_params_sgd)
print("Best Score for SGDRegressor: ", best_score_sgd)

# Train the SGDRegressor with the optimal parameters
sgd_model_optimal = SGDRegressor(**best_params_sgd, random_state=42)
sgd_model_optimal.fit(X_train, y_train)

# Get predictions using the trained model for the testing split
y_pred_sgd_optimal = sgd_model_optimal.predict(X_test)

# Calculate R-squared and MSE for SGD Linear Regression with optimal parameters
r2_sgd_optimal = r2_score(y_test, y_pred_sgd_optimal)
mse_sgd_optimal = mean_squared_error(y_test, y_pred_sgd_optimal)

print("\nSGD Linear Regressor with Optimal Parameters:")
print("R-squared:", r2_sgd_optimal)
print("Mean Squared Error:", mse_sgd_optimal)

print("\nComparison with previous SGD model:")
print("R-squared (Optimal vs Previous):", r2_sgd_optimal, "vs", r2_sgd)
print("Mean Squared Error (Optimal vs Previous):", mse_sgd_optimal, "vs", mse_sgd)

# Save the best model as pickle dump
with open('Assignment3\\task1\\sgd_regression_optimal_model.pkl', 'wb') as model_file:
    pickle.dump(sgd_model_optimal, model_file)

# Step 3: Cross-Validation for RidgeCV, ElasticNetCV, and LassoCV

# Ignore convergence warnings
warnings.simplefilter("ignore", ConvergenceWarning)
alpha_values = [0.0001, 0.001, 0.01, 0.1, 1, 10]

# RidgeCV
ridge_cv = RidgeCV(alphas=alpha_values, store_cv_values=True)
ridge_cv.fit(X_train, y_train)
best_alpha_ridge = ridge_cv.alpha_

# ElasticNetCV
elastic_net_cv = ElasticNetCV(alphas=alpha_values,l1_ratio=[0.1, 0.5, 0.7, 0.9, 0.95, 0.99, 1.0], cv=kf)
elastic_net_cv.fit(X_train, y_train)
best_alpha_elastic_net = elastic_net_cv.alpha_

# LassoCV
lasso_cv = LassoCV(alphas=alpha_values, cv=kf)
lasso_cv.fit(X_train, y_train)
best_alpha_lasso = lasso_cv.alpha_

print("\nBest Alpha values:")
print("Ridge:", best_alpha_ridge)
print("ElasticNet:", best_alpha_elastic_net)
print("Lasso:", best_alpha_lasso)

# Step 4: Train and Test Ridge, ElasticNet, and Lasso Models
ridge_model = Ridge(alpha=best_alpha_ridge)
elastic_net_model = ElasticNet(alpha=best_alpha_elastic_net, l1_ratio=0.5)
lasso_model = Lasso(alpha=best_alpha_lasso)

ridge_model.fit(X_train, y_train)
elastic_net_model.fit(X_train, y_train)
lasso_model.fit(X_train, y_train)

# Test the trained models on the testing split
y_pred_ridge = ridge_model.predict(X_test)
y_pred_elastic_net = elastic_net_model.predict(X_test)
y_pred_lasso = lasso_model.predict(X_test)

# Calculate R-squared and MSE for each model
r2_ridge = r2_score(y_test, y_pred_ridge)
mse_ridge = mean_squared_error(y_test, y_pred_ridge)

r2_elastic_net = r2_score(y_test, y_pred_elastic_net)
mse_elastic_net = mean_squared_error(y_test, y_pred_elastic_net)

r2_lasso = r2_score(y_test, y_pred_lasso)
mse_lasso = mean_squared_error(y_test, y_pred_lasso)

print("\nPerformance Metrics for Ridge:")
print("R-squared:", r2_ridge)
print("Mean Squared Error:", mse_ridge)

print("\nPerformance Metrics for ElasticNet:")
print("R-squared:", r2_elastic_net)
print("Mean Squared Error:", mse_elastic_net)

print("\nPerformance Metrics for Lasso:")
print("R-squared:", r2_lasso)
print("Mean Squared Error:", mse_lasso)

print("\nPerformance Metrics for SGD Linear Regressor:")
print("R-squared:", r2_sgd)
print("Mean Squared Error:", mse_sgd)

print("\nPerformance Metrics for Optimal SGD Linear Regressor:")
print("R-squared:", r2_sgd_optimal)
print("Mean Squared Error:", mse_sgd_optimal)

print("\nPerformance Metrics for OLS Linear Regression:")
print("R-squared:", r2_ols)
print("Mean Squared Error:", mse_ols)


# Step 5: Save the best model as pickle dump
with open('Assignment3\\task1\\ridge_model.pkl', 'wb') as model_file:
    pickle.dump(ridge_model, model_file)

with open('Assignment3\\task1\\elastic_net_model.pkl', 'wb') as model_file:
    pickle.dump(elastic_net_model, model_file)

with open('Assignment3\\task1\\lasso_model.pkl', 'wb') as model_file:
    pickle.dump(lasso_model, model_file)

with open('Assignment3\\task1\\sgd_regression_model.pkl', 'wb') as model_file:
    pickle.dump(sgd_model, model_file)

with open('Assignment3\\task1\\sgd_regression_optimal_model.pkl', 'wb') as model_file:
    pickle.dump(sgd_model_optimal, model_file)

with open('Assignment2\\linear_regression_optimal_model.pkl', 'wb') as model_file:
    pickle.dump(ols_model, model_file)

# Select the best model based on the evaluation metric
models = [
    ('Ridge', ridge_model, mse_ridge),
    ('ElasticNet', elastic_net_model, mse_elastic_net),
    ('Lasso', lasso_model, mse_lasso),
    ('SGD', sgd_model, mse_sgd),
    ('SGD Optimal', sgd_model_optimal, mse_sgd),
    ('OLS', ols_model, mse_ols)
]

best_model = min(models, key=lambda x: x[2])[1]

# Train the best model on the full training set
best_model.fit(X_train, y_train)

# Test the best model on the testing set
y_pred_best_model = best_model.predict(X_test)

# Calculate R-squared and MSE for the best model
r2_best_model = r2_score(y_test, y_pred_best_model)
mse_best_model = mean_squared_error(y_test, y_pred_best_model)

print("\nBest Model:")
print(f"Type: {type(best_model).__name__}")
print("R-squared:", r2_best_model)
print("Mean Squared Error:", mse_best_model)

# Save the best model as a pickle dump
with open('Assignment3\\task1\\best_model.pkl', 'wb') as model_file:
    pickle.dump(best_model, model_file)