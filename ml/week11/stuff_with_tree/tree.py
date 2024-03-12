"""
Week11: test with decision trees

19.11.2019 / Sascha Jecklin

"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


df = pd.read_csv('Data/Hitters.csv').dropna()
df = df.drop('Unnamed: 0', axis=1)
df = pd.get_dummies(df)
df.info()
target = np.log(df.Salary.values)
predictors = df.drop(['Salary'], axis=1)

best_mse_overall = np.inf
best_predictor = []
for col in predictors.columns:
    current_pred = predictors[col].values.reshape(-1, 1)
    stacked  = np.hstack((current_pred, target.reshape(-1, 1)))
    stacked_sorted = stacked[stacked[:,0].argsort()]
    current_pred_sorted = stacked_sorted[:,0]
    current_target_sorted = stacked_sorted[:,1]
    best_mse = np.inf
    mse_list = []
    if col == "Years":
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        print("test")
    for i, value in enumerate(current_pred_sorted):
        left = np.mean(current_pred_sorted[:i+1])
        right = np.mean(current_pred_sorted[i:])
        prediction = np.zeros(current_target_sorted.shape)
        prediction[current_pred_sorted <= value] = left
        prediction[current_pred_sorted > value] = right
        mse = mean_squared_error(prediction, current_target_sorted)
        mse_list.append(mse)
        if mse < best_mse:
            best_mse = mse
            best_i = i
            best_value = value
            if value == 4:
                print("test2")
    if col =="Years":
        print(mse_list)
    if best_mse < best_mse_overall:
        best_mse_overall = best_mse
        best_i_overall = best_i
        best_value_overall = best_value
        best_col = col
    print(col, best_i, best_value, best_mse)
    mdl = LinearRegression().fit(predictors[col].values.reshape(-1, 1), target)
    best_predictor.append(mdl.score(predictors[col].values.reshape(-1, 1),
                                    target))

print(best_col, best_i_overall, best_value_overall, best_mse_overall)
best = np.argmax(best_predictor)
print (best)
