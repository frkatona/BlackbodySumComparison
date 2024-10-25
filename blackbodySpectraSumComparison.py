#%%
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from scipy.optimize import curve_fit
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

summedPeakPositions = []

# Generate a Gaussian temperature distribution
length = 300 # pixels
sigma = 50
x = np.linspace(-length // 2, length // 2, length)
y = np.linspace(-length // 2, length // 2, length)
x, y = np.meshgrid(x, y)

# show a sample of the distribution with normalized temperature
plt.figure(figsize=(8, 8))
plt.imshow(np.exp(-(x**2 + y**2) / (2 * sigma**2)), cmap='hot', interpolation='nearest')
plt.colorbar(label='temperature (arb)')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
# plt.title(f'{length}x{length} px normal temperature distribution at sigma = {sigma}', fontsize=12)

#%%
# Plot each summed blackbody spectrum
plt.figure(figsize=(16, 10))

for idx, temp in enumerate(temperatures):

    temperature_distribution = temp * np.exp(-(x**2 + y**2) / (2 * sigma**2))

    # Sum the blackbody spectra for the distribution
    summed_spectrum = np.zeros_like(wavelengths)
    for row in temperature_distribution:
        for pixel_temp in row:
            if pixel_temp > 0:
                summed_spectrum += planck_law(wavelengths, pixel_temp)

    # store peak positions for wein's displacement law
    summedPeakPositions.append(wavelengths[np.argmax(summed_spectrum)])

    # Normalize
    summed_spectrum /= np.max(summed_spectrum)  

    plt.plot(wavelengths * 1e9, summed_spectrum, color=reds[idx], label=f'Summed T = {temp} K')

# use the peak positions and the wein displacement law to make an array of temperatures
b = 2.898e-3 # Wien's displacement constant in m*K
weinTemps = [b // peak for peak in summedPeakPositions]

# Plot individual blackbody spectra for each temperature
for idx, temp in enumerate(weinTemps):
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

#%%
# make a graph to compare the original temperatures to the wein temperatures

# Define a linear function for fitting
def linear_fit(x, a, b):
    return a * x + b

# Fit the data
params, _ = curve_fit(linear_fit, temperatures, weinTemps)

# Generate fit line data
fit_line = linear_fit(np.array(temperatures), *params)

plt.figure(figsize=(16, 10))
plt.scatter(temperatures, weinTemps, color='red', label='Data')
plt.plot(temperatures, fit_line, color='blue', linestyle='-', label=f'Fit: y = {params[0]:.2f}x + {params[1]:.2f}')
plt.plot(temperatures, temperatures, color='green', linestyle='--', label='y = x')
plt.xlabel('Gaussian Temperature (K)', fontsize=20)
plt.ylabel('Matching WDL Temperature (K)', fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title('uniform temperatures with matching peak positions to summed blackbody temperatures', fontsize=20)
plt.xlim(0, 3200)
plt.ylim(0, 3200)
plt.grid(True)
plt.legend(fontsize=12)

# %%