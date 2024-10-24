import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import csv
import matplotlib.cm as cm

# Define a function to calculate blackbody spectral radiance using Planck's law
def planck_law(wavelength, temperature):
    # Wavelength in meters, temperature in Kelvin
    return (2 * const.h * const.c**2) / (wavelength**5) * (1 / (np.exp((const.h * const.c) / (wavelength * const.k * temperature)) - 1))

# Wavelength range (in meters)
wavelengths = np.linspace(100e-9, 10000e-9, 1000)  # 300 nm to 2500 nm

# Temperatures to consider (in K)
temperatures = [273, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000]

# Prepare to store summed spectra
summed_spectra = []

# Colors for plotting
reds = cm.Reds(np.linspace(0.2, 1.0, len(temperatures)))
blues = cm.Blues(np.linspace(0.2, 1.0, len(temperatures)))

# Plot each summed blackbody spectrum
plt.figure(figsize=(16, 10))

for idx, temp in enumerate(temperatures):
    # Generate a Gaussian temperature distribution centered at `temp`
    size = 64
    sigma = 10
    x = np.linspace(-size // 2, size // 2, size)
    y = np.linspace(-size // 2, size // 2, size)
    x, y = np.meshgrid(x, y)
    temperature_distribution = temp * np.exp(-(x**2 + y**2) / (2 * sigma**2))

    # Sum the blackbody spectra for the distribution
    summed_spectrum = np.zeros_like(wavelengths)
    for row in temperature_distribution:
        for pixel_temp in row:
            if pixel_temp > 0:
                summed_spectrum += planck_law(wavelengths, pixel_temp)

    summed_spectrum /= np.max(summed_spectrum)  # Normalize to peak value

    summed_spectra.append(summed_spectrum)
    plt.plot(wavelengths * 1e9, summed_spectrum, color=reds[idx], label=f'Summed T = {temp} K')

# Plot individual blackbody spectra for each temperature
for idx, temp in enumerate(temperatures):
    blackbody_spectrum = planck_law(wavelengths, temp)
    blackbody_spectrum /= np.max(blackbody_spectrum)  # Normalize to peak value
    plt.plot(wavelengths * 1e9, blackbody_spectrum, color=blues[idx], linestyle='--', label=f'Blackbody T = {temp} K')

# Configure plot properties
plt.xlabel('Wavelength (nm)', fontsize=20)
plt.ylabel('Spectral Radiance (arbitrary units)', fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tick_params(axis='both', which='both', direction='out', length=6)
plt.xlim(300, 10000)

# Add secondary x-axis for wavenumbers
ax = plt.gca()
ax2 = ax.secondary_xaxis('top', functions=(lambda x: 1e7 / x, lambda x: 1e7 / x))  # Convert nm to cm^-1
ax2.set_xlabel('Wavenumber (cm$^{-1}$)', fontsize=20)
ax2.tick_params(axis='x', labelsize=16)

plt.grid(True)
plt.legend(fontsize=12)
plt.show()