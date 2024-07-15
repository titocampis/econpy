# Suppress specific warning for matplotlib with WSL
import warnings

warnings.filterwarnings(
    "ignore", message="Unable to import Axes3D", category=UserWarning
)

import matplotlib.pyplot as plt
import numpy as np

# Valores de r
r = np.linspace(-0.2, 0.2, 400)


# Definición de la función
def func(ratio):
    return (1 + ratio / 12) ** 12 - (1 + ratio)


# Cálculo de los valores de la función
y = func(r)

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(r, y, label=r"$(1 + \frac{r}{12})^{12} - (1 + r)$")
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
plt.axvline(0, color="black", linewidth=0.5, linestyle="--")
plt.title("Comparación de Interés Compuesto Mensual vs. Anual")
plt.xlabel("Tasa de Interés Anual (r)")
plt.ylabel("Diferencia")
plt.legend()
plt.grid(True)
plt.show()
