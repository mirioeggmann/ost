import matplotlib.pyplot as plt
import numpy as np

def U(t):
    return 1 if abs(t) < 0.5 else 0

def kernel(x, x_prime, gamma=1):
    return U(np.exp(-gamma * (x - x_prime)**2))

# Generate a range of x values
x_values = np.linspace(-3, 3, 500)
x_prime = 0
gamma = 1

# Calculate the kernel values
k_values = [kernel(x, x_prime, gamma) for x in x_values]

# Create the plot
plt.plot(x_values, k_values)
plt.xlabel('x')
plt.ylabel('Kernel value')
plt.title('Custom Kernel: U(exp(-gamma * (x - x\')^2))')
plt.grid(True)
plt.show()