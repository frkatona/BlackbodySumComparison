import numpy as np
import matplotlib.pyplot as plt

# Parameters for the Gaussian temperature distribution
size = 64  # Grid size (64x64 pixels)
center_temperature = 2000  # Temperature at the center (in K)
sigma = 10  # Standard deviation of the Gaussian (controls the spread)

# Create a grid of x, y coordinates
x = np.linspace(-size//2, size//2, size)
y = np.linspace(-size//2, size//2, size)
x, y = np.meshgrid(x, y)

# Calculate the Gaussian distribution
temperature_distribution = center_temperature * np.exp(-(x**2 + y**2) / (2 * sigma**2))

# Plot the temperature distribution
plt.figure(figsize=(6, 6))
plt.imshow(temperature_distribution, cmap='hot', origin='lower')
plt.colorbar(label='Temperature (K)')
plt.title('64x64 Pixel Gaussian Temperature Distribution')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.show()
