# Reconstruction of the 3D position from two camera views.

import numpy as np


def main():
    # Camera Model Matrices
    K = np.array([[100, 0, 60], [0, 100, 45], [0, 0, 1]])
    D1 = np.eye(3)
    c1 = np.full((3,), 2)
    b1 = np.array([113, 10, 1])
    D2 = np.array(
        [
            [np.cos(-np.pi / 3), 0, np.sin(-np.pi / 3)],
            [0, 1, 0],
            [-np.sin(-np.pi / 3), 0, np.cos(-np.pi / 3)],
        ]
    )
    c2 = 100 * np.array([-1, -1, 1])
    b2 = np.array([86, 73, 1])

    # directional vectors
    r1 = np.matmul(np.linalg.inv(np.matmul(K, D1)), b1)
    r2 = np.matmul(np.linalg.inv(np.matmul(K, D2)), b2)

    # Equation System
    A = np.zeros((6, 5))
    A[:3, :3] = np.eye(3)
    A[3:, :3] = np.eye(3)
    A[:3, 3] = -r1
    A[3:, 4] = -r2
    c = np.zeros((6,))
    c[:3] = c1
    c[3:] = c2

    # Calculation of the solution
    x = np.matmul(np.matmul(np.linalg.inv(np.matmul(A.T, A)), A.T), c)

    q = np.empty((3, 2))
    q[:, 0] = c1 + x[3] * r1
    q[:, 1] = c2 + x[4] * r2

    # Calculate the error
    e = np.sqrt(np.mean(np.sum((q.T - x[:3]) ** 2, axis=1)))

    # Print solution
    print("3D-Position:", x[:3])
    print("RMSE:", e)


if __name__ == "__main__":
    main()
