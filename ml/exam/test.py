import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

# Data
X = np.array([[-1, -1], [1, -1], [-1, 1], [1, 1], [0, -2], [0, 2], [-2, -2], [2, -2], [-2, 2], [2, 2]])
y = np.array([1, 1, -1, -1, 1, -1, 1, 1, -1, -1])  # 1 for B and -1 for A

clf = SVC(kernel='linear', C=0.5)
clf.fit(X, y)

# Plotting
plt.scatter(X[:, 0], X[:, 1], c=y, s=100, cmap='bwr')
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Create grid to evaluate model
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

# Plot decision boundary and margins
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])

# Plot support vectors
ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=200, facecolors='none', edgecolors='k')
plt.xlabel('X1')
plt.ylabel('X2')
plt.show()