import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Crear una función para calcular log(z)
def complex_log(r, theta):
    # log(z) = log|z| + i*arg(z)
    return np.log(r), theta

# Definir el rango para r y theta (coordenadas polares)
r = np.linspace(0.01, 3, 100)  # Evitar r=0 porque log(0) no está definido
theta = np.linspace(-2*np.pi, 2*np.pi, 100)  # Mostrar múltiples hojas
r_grid, theta_grid = np.meshgrid(r, theta)

# Calcular partes real e imaginaria
real_part, imag_part = complex_log(r_grid, theta_grid)

# Convertir a coordenadas cartesianas para la visualización
x = r_grid * np.cos(theta_grid)
y = r_grid * np.sin(theta_grid)

# Crear figura con dos subplots (uno para parte real, otro para parte imaginaria)
fig = plt.figure(figsize=(14, 7))

# Gráfica para la parte real
ax1 = fig.add_subplot(121, projection='3d')
surface1 = ax1.plot_surface(x, y, real_part, cmap=cm.viridis, alpha=0.8, 
                            linewidth=0, antialiased=True)
ax1.set_title('Parte Real de log(z)')
ax1.set_xlabel('Re(z)')
ax1.set_ylabel('Im(z)')
ax1.set_zlabel('Re(log(z))')
fig.colorbar(surface1, ax=ax1, shrink=0.5, aspect=10)

# Gráfica para la parte imaginaria
ax2 = fig.add_subplot(122, projection='3d')
surface2 = ax2.plot_surface(x, y, imag_part, cmap=cm.plasma, alpha=0.8, 
                           linewidth=0, antialiased=True)
ax2.set_title('Parte Imaginaria de log(z)')
ax2.set_xlabel('Re(z)')
ax2.set_ylabel('Im(z)')
ax2.set_zlabel('Im(log(z))')
fig.colorbar(surface2, ax=ax2, shrink=0.5, aspect=10)

plt.tight_layout()
plt.show()

# Otra visualización: superficie de Riemann helicoidal
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Parámetros para la visualización helicoidal
r_helix = np.linspace(0.1, 2, 50)
theta_helix = np.linspace(-4*np.pi, 4*np.pi, 200)
r_grid_helix, theta_grid_helix = np.meshgrid(r_helix, theta_helix)

# Coordenadas para la superficie helicoidal
x_helix = r_grid_helix * np.cos(theta_grid_helix)
y_helix = r_grid_helix * np.sin(theta_grid_helix)
z_helix = theta_grid_helix  # La parte imaginaria forma la hélice

# Crear la superficie helicoidal
helix_surface = ax.plot_surface(x_helix, y_helix, z_helix, 
                               cmap=cm.coolwarm, alpha=0.8,
                               linewidth=0, antialiased=True)

ax.set_title('Superficie de Riemann para log(z)')
ax.set_xlabel('Re(z)')
ax.set_ylabel('Im(z)')
ax.set_zlabel('arg(z)')
fig.colorbar(helix_surface, ax=ax, shrink=0.5, aspect=10)

plt.tight_layout()
plt.show()                      