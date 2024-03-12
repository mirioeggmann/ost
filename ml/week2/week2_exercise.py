"""
Statistical Machine Learning - Chapter 3 - python

By N. Tobler
"""

import numpy as np
import matplotlib.pyplot as plt

from KNN_ import KNN_

# Loading Data
train_data = np.genfromtxt('KNN_Train.csv', delimiter=',', skip_header=1)
test_data  = np.genfromtxt('KNN_Test.csv', delimiter=',', skip_header=1)

X_train = train_data[:, :2]
y_train = train_data[:, 2].astype(int)

X_test = test_data[:, :2]
y_test = test_data[:, 2].astype(int)

# Call KNN function
k = 3
predicted_labels, nn_index, accuracy = KNN_(k, X_train, y_train, X_test, y_test)

print(f'Accuracy: {accuracy:1.4f}')

plt.figure()
plt.scatter(X_train[:, 0], X_train[:,1], 20, y_train)
plt.scatter(X_test[:, 0], X_test[:, 1], 20, predicted_labels, edgecolors="red")
plt.xlabel('1. Predictor')
plt.ylabel('2. Predictor')
plt.title('kNN classifier')
plt.grid()

## Run KNN classifier with different k and display decision surface

# Prepare predictor data for decision surface
x1range = np.arange(np.min([X_train[:, 0], X_test[:, 0]]), np.max([X_train[:, 0], X_test[:, 0]]), 0.5)
x2range = np.arange(np.min([X_train[:, 1], X_test[:, 1]]), np.max([X_train[:, 1], X_test[:, 1]]), 0.5)
[xx1, xx2] = np.meshgrid(x1range,x2range)
XGrid = np.stack((xx1.flatten(), xx2.flatten()), axis=-1)

_, axs = plt.subplots(2, 2, tight_layout=True)
axs = axs.flatten()
for i in range(4):
    k = i * 4 + 1
    
    # Call KNN_ with different k
    predicted_labels_1, _, _ = KNN_(k, X_train, y_train, X_test)
    predicted_labels_2, _, _ = KNN_(k, X_train, y_train, XGrid)
    
    # Display decision surface
    
    e = axs[i].pcolor(xx1, xx2, np.reshape(predicted_labels_2, xx1.shape), alpha=0.2)
    # set(e,'facealpha',0.2)
    # set(e, 'EdgeColor', 'none')
    
    # Display test samples
    axs[i].scatter(X_test[:,0], X_test[:,1], 20, predicted_labels_1)
    axs[i].set_title(f'kNN classifier k={k}')


## Plot error rate

# TODO: Plot training error rate and test error rate as a function of
# 1 / K (flexibility of KNN)


# show all plots
plt.show()
