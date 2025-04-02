import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import integrate
import time
from matplotlib.animation import FuncAnimation

def riemann_sum(f, a, b, n, method='midpoint'):
    """
    Calcula la suma de Riemann para una función f en el intervalo [a, b]
    utilizando n subintervalos.
    
    Parámetros:
    f: función a integrar
    a: límite inferior del intervalo
    b: límite superior del intervalo
    n: número de subintervalos
    method: método de aproximación ('left', 'right', 'midpoint', 'trapezoid')
    
    Retorna:
    La aproximación de la integral definida
    """
    if n <= 0:
        raise ValueError("El número de subintervalos debe ser positivo")
    
    # Ancho de cada subintervalo
    delta_x = (b - a) / n
    
    # Inicializar la suma
    suma = 0
    
    for i in range(n):
        # Calcular los puntos de evaluación según el método
        if method == 'left':
            # Punto extremo izquierdo
            x = a + i * delta_x
        elif method == 'right':
            # Punto extremo derecho
            x = a + (i + 1) * delta_x
        elif method == 'midpoint':
            # Punto medio
            x = a + (i + 0.5) * delta_x
        elif method == 'trapezoid':
            # Método del trapecio (promedio de los extremos)
            x_left = a + i * delta_x
            x_right = a + (i + 1) * delta_x
            suma += (f(x_left) + f(x_right)) / 2 * delta_x
            continue
        else:
            raise ValueError("Método no reconocido. Use 'left', 'right', 'midpoint' o 'trapezoid'")
        
        # Sumar el área del rectángulo
        suma += f(x) * delta_x
    
    return suma

def verificar_dominio(f, a, b, tolerancia=1e-6):
    """
    Verifica si el intervalo [a, b] está dentro del dominio de la función.
    
    Parámetros:
    f: función a verificar
    a, b: límites del intervalo
    tolerancia: distancia mínima para verificar alrededor de puntos potencialmente problemáticos
    
    Retorna:
    True si el intervalo parece estar en el dominio, False en caso contrario
    """
    # 1. Verificar los extremos del intervalo
    try:
        resultado_a = f(a)
        resultado_b = f(b)
        if (resultado_a is None or np.isnan(resultado_a) or np.isinf(resultado_a) or
            resultado_b is None or np.isnan(resultado_b) or np.isinf(resultado_b)):
            return False
    except Exception:
        return False
    
    # 2. Verificar puntos uniformemente distribuidos (mayor densidad)
    n_verificacion = 1000000  # Verificar 1000 puntos en lugar de 10
    puntos_uniformes = np.linspace(a, b, n_verificacion)
    
    try:
        for x in puntos_uniformes:
            resultado = f(x)
            if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                return False
    except Exception:
        return False
    
    # 3. Búsqueda adaptativa de puntos problemáticos
    # Intentar identificar regiones de cambio rápido donde pueden existir problemas
    valores = [f(x) for x in puntos_uniformes]
    diferencias = np.abs(np.diff(valores))
    
    # Si hay cambios muy grandes, verificar con más detalle esas regiones
    umbral_cambio = np.mean(diferencias) + 3 * np.std(diferencias)  # Umbral estadístico
    indices_sospechosos = np.where(diferencias > umbral_cambio)[0]
    
    for i in indices_sospechosos:
        # Verificar con mayor detalle alrededor de los puntos sospechosos
        x_izq = puntos_uniformes[i]
        x_der = puntos_uniformes[i + 1]
        puntos_detallados = np.linspace(x_izq, x_der, 100)  # 100 puntos en el intervalo sospechoso
        
        try:
            for x in puntos_detallados:
                resultado = f(x)
                if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                    return False
        except Exception:
            return False
    
    # 4. Verificar específicamente puntos "redondos" donde pueden haber singularidades
    # (Ejemplo: si tenemos log(x-2), habrá problema en x=2)
    puntos_especiales = []
    # Añadir enteros en el intervalo
    puntos_especiales.extend([i for i in range(int(a), int(b)+1) if a <= i <= b])
    # Añadir fracciones comunes
    for i in range(1, 21):  # Denominadores hasta 20
        for j in range(i):  # Numeradores
            punto = j/i
            if a <= punto <= b:
                puntos_especiales.append(punto)
    # Añadir valores especiales (π, e, etc.)
    valores_especiales = [math.pi, math.e, math.sqrt(2), math.sqrt(3)]
    puntos_especiales.extend([v for v in valores_especiales if a <= v <= b])
    
    # Verificar los puntos especiales y sus alrededores
    for punto in set(puntos_especiales):  # Usar set para eliminar duplicados
        # Verificar el punto exacto
        try:
            resultado = f(punto)
            if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                return False
        except Exception:
            return False
        
        # Verificar alrededor del punto (para detectar discontinuidades)
        if punto > a + tolerancia:
            try:
                resultado = f(punto - tolerancia)
                if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                    return False
            except Exception:
                return False
        
        if punto < b - tolerancia:
            try:
                resultado = f(punto + tolerancia)
                if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                    return False
            except Exception:
                return False
    
    return True  # Si pasó todas las verificaciones, parece estar en el dominio

def get_polygon_coordinates(f, a, b, i, n, method):
    """
    Obtiene las coordenadas para dibujar un polígono (rectángulo o trapecio)
    
    Parámetros:
    f: función a integrar
    a, b: límites del intervalo
    i: índice del subintervalo
    n: número total de subintervalos
    method: método de aproximación
    
    Retorna:
    xs, ys: listas con las coordenadas x e y del polígono
    """
    delta_x = (b - a) / n
    x_left = a + i * delta_x
    x_right = a + (i + 1) * delta_x
    
    if method == 'left':
        y_height = f(x_left)
        xs = [x_left, x_right, x_right, x_left]
        ys = [0, 0, y_height, y_height]
    elif method == 'right':
        y_height = f(x_right)
        xs = [x_left, x_right, x_right, x_left]
        ys = [0, 0, y_height, y_height]
    elif method == 'midpoint':
        x_mid = (x_left + x_right) / 2
        y_height = f(x_mid)
        xs = [x_left, x_right, x_right, x_left]
        ys = [0, 0, y_height, y_height]
    elif method == 'trapezoid':
        y_left = f(x_left)
        y_right = f(x_right)
        xs = [x_left, x_right, x_right, x_left]
        ys = [0, 0, y_right, y_left]
    else:
        raise ValueError("Método no reconocido")
    
    return xs, ys

def graficar_riemann_dinamico(f, a, b, n, method='midpoint', title=None, variable='x'):
    """
    Crea una animación de la aproximación de Riemann.
    
    Parámetros:
    f: función a integrar
    a: límite inferior del intervalo
    b: límite superior del intervalo
    n: número de subintervalos
    method: método de aproximación ('left', 'right', 'midpoint', 'trapezoid')
    title: título opcional para la gráfica
    variable: nombre de la variable de integración
    """
    # Verificar que los límites estén en el dominio de la función
    if not verificar_dominio(f, a, b):
        print(f"Error: Los límites [{a}, {b}] no están completamente dentro del dominio de la función.")
        return None
    
    # Calcular la velocidad de la animación para que dure máximo 5 segundos
    velocidad = 5 / (n + 1)  # +1 para incluir el frame final
    
    # Crear puntos para graficar la función original
    x_func = np.linspace(a, b, 1000)
    y_func = [f(x) for x in x_func]
    
    # Determinar el rango de y para la gráfica
    y_min = min(0, min(y_func))
    y_max = max(y_func) * 1.1
    
    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Graficar la función original
    ax.plot(x_func, y_func, 'b-', linewidth=2, label=f'Función f({variable})')
    
    # Agregar título y etiquetas
    method_names = {
        'left': 'Punto Izquierdo',
        'right': 'Punto Derecho',
        'midpoint': 'Punto Medio',
        'trapezoid': 'Trapecio'
    }
    
    if title is None:
        title = f"Aproximación de Riemann: Método del {method_names[method]} con {n} subintervalos"
    
    ax.set_title(title)
    ax.set_xlabel(variable)
    ax.set_ylabel(f'f({variable})')
    ax.grid(True)
    ax.legend()
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.set_xlim(a, b)
    ax.set_ylim(y_min, y_max)
    
    # Crear texto para mostrar la aproximación
    aprox_text = ax.text(0.05, 0.95, '', transform=ax.transAxes,
                         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    # Crear texto para mostrar la notación de la integral
    integral_text = ax.text(0.05, 0.89, '', transform=ax.transAxes,
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    # Lista para almacenar los polígonos (ahora global)
    poligonos = []
    
    # Inicializar suma
    suma_actual = 0
    delta_x = (b - a) / n
    
    def init():
        # Limpiar los polígonos anteriores
        for p in poligonos:
            p.remove()
        poligonos.clear()
        
        aprox_text.set_text('')
        integral_text.set_text('')
        return aprox_text, integral_text
    
    def animate(i):
        nonlocal suma_actual
        
        # Si es el primer frame, reiniciar la animación
        if i == 0:
            for p in poligonos:
                p.remove()
            poligonos.clear()
            suma_actual = 0
        
        # Si hay más subintervalos por agregar
        if i < n:
            # Calcular las coordenadas del polígono
            xs, ys = get_polygon_coordinates(f, a, b, i, n, method)
            
            # Crear el polígono y agregarlo al gráfico
            poligono = plt.Polygon(list(zip(xs, ys)), fill=True, alpha=0.3, edgecolor='r', facecolor='r')
            ax.add_patch(poligono)
            poligonos.append(poligono)
            
            # Actualizar la suma
            if method == 'left':
                suma_actual += f(a + i * delta_x) * delta_x
            elif method == 'right':
                suma_actual += f(a + (i + 1) * delta_x) * delta_x
            elif method == 'midpoint':
                suma_actual += f(a + (i + 0.5) * delta_x) * delta_x
            elif method == 'trapezoid':
                suma_actual += (f(a + i * delta_x) + f(a + (i + 1) * delta_x)) / 2 * delta_x
            
            # Actualizar el texto de la aproximación
            aprox_text.set_text(f'Aproximación parcial ({i+1}/{n}): {suma_actual:.6f}')
            integral_text.set_text(f'∫({a})^({b}) f({variable}) d{variable} ≈ {suma_actual:.6f}')
        
        # Si es el último frame, mostrar la aproximación final
        elif i == n:
            aprox_text.set_text(f'Aproximación final: {suma_actual:.6f}')
            integral_text.set_text(f'∫({a})^({b}) f({variable}) d{variable} ≈ {suma_actual:.6f}')
        
        # Se debe devolver todos los objetos actualizados
        return [aprox_text, integral_text] + poligonos
    
    # Crear la animación
    frames = n + 1  # Número de subintervalos + 1 para el mensaje final
    ani = FuncAnimation(fig, animate, frames=frames, init_func=init, blit=True, interval=velocidad*1000)
    
    plt.tight_layout()
    plt.show()
    
    # Calcular y devolver la aproximación final
    return riemann_sum(f, a, b, n, method)

def evaluar_expresion(expresion, valor, variable='x'):
    """
    Evalúa una expresión matemática en un valor dado.
    
    Parámetros:
    expresion: string con la expresión matemática
    valor: valor en el que evaluar la expresión
    variable: nombre de la variable a reemplazar
    
    Retorna:
    El resultado de evaluar la expresión
    """
    # Crear un espacio de nombres con las funciones matemáticas
    namespace = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'sqrt': math.sqrt,
        'pi': math.pi,
        'e': math.e,
        'abs': abs,
        'pow': pow
    }
    
    # Asignar el valor a la variable
    namespace[variable] = valor
    
    try:
        # Evaluar la expresión
        return eval(expresion, {"__builtins__": {}}, namespace)
    except Exception as e:
        print(f"Error al evaluar la expresión: {e}")
        return None
def resolver_integral_exacta(f, a, b, expresion, variable='x'):
    """
    Resuelve la integral de forma exacta y muestra su gráfica.
    
    Parámetros:
    f: función a integrar
    a: límite inferior del intervalo
    b: límite superior del intervalo
    expresion: expresión matemática de la función
    variable: nombre de la variable de integración
    
    Retorna:
    El resultado exacto de la integral
    """
    try:
        # Calcular el resultado exacto
        resultado, error = integrate.quad(f, a, b)
        
        # Crear puntos para graficar la función original
        x_func = np.linspace(a, b, 100000)
        y_func = [f(x) for x in x_func]
        
        # Determinar el rango de y para la gráfica
        y_min = min(0, min(y_func))
        y_max = max(y_func) * 1.1
        
        # Crear la figura y los ejes
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Graficar la función original
        ax.plot(x_func, y_func, 'b-', linewidth=2, label=f'Función f({variable})')
        
        # Rellenar el área bajo la curva
        ax.fill_between(x_func, y_func, alpha=0.3, color='green')
        
        # Agregar título y etiquetas
        ax.set_title(f"Integral exacta de f({variable}) = {expresion}")
        ax.set_xlabel(variable)
        ax.set_ylabel(f'f({variable})')
        ax.grid(True)
        ax.legend()
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.set_xlim(a, b)
        ax.set_ylim(y_min, y_max)
        
        # Agregar texto con el resultado
        ax.text(0.05, 0.95, 
                f'Integral exacta: {resultado:.6f}', 
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        ax.text(0.05, 0.89, 
                f'∫({a})^({b}) f({variable}) d{variable} = {resultado:.6f}', 
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return resultado
        
    except Exception as e:
        print(f"Error al calcular la integral exacta: {e}")
        print("Se procederá con la aproximación numérica.")
        return None


import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import integrate
import time
from matplotlib.animation import FuncAnimation

def riemann_sum(f, a, b, n, method='midpoint'):
    """
    Calcula la suma de Riemann para una función f en el intervalo [a, b]
    utilizando n subintervalos.
    
    Parámetros:
    f: función a integrar
    a: límite inferior del intervalo
    b: límite superior del intervalo
    n: número de subintervalos
    method: método de aproximación ('left', 'right', 'midpoint', 'trapezoid')
    
    Retorna:
    La aproximación de la integral definida
    """
    if n <= 0:
        raise ValueError("El número de subintervalos debe ser positivo")
    
    # Ancho de cada subintervalo
    delta_x = (b - a) / n
    
    # Inicializar la suma
    suma = 0
    
    for i in range(n):
        # Calcular los puntos de evaluación según el método
        if method == 'left':
            # Punto extremo izquierdo
            x = a + i * delta_x
        elif method == 'right':
            # Punto extremo derecho
            x = a + (i + 1) * delta_x
        elif method == 'midpoint':
            # Punto medio
            x = a + (i + 0.5) * delta_x
        elif method == 'trapezoid':
            # Método del trapecio (promedio de los extremos)
            x_left = a + i * delta_x
            x_right = a + (i + 1) * delta_x
            suma += (f(x_left) + f(x_right)) / 2 * delta_x
            continue
        else:
            raise ValueError("Método no reconocido. Use 'left', 'right', 'midpoint' o 'trapezoid'")
        
        # Sumar el área del rectángulo
        suma += f(x) * delta_x
    
    return suma

def verificar_dominio(f, a, b, tolerancia=1e-6):
    """
    Verifica si el intervalo [a, b] está dentro del dominio de la función de manera más exhaustiva.
    
    Parámetros:
    f: función a verificar
    a, b: límites del intervalo
    tolerancia: distancia mínima para verificar alrededor de puntos potencialmente problemáticos
    
    Retorna:
    True si el intervalo parece estar en el dominio, False en caso contrario
    """
    # 1. Verificar los extremos del intervalo
    try:
        resultado_a = f(a)
        resultado_b = f(b)
        if (resultado_a is None or np.isnan(resultado_a) or np.isinf(resultado_a) or
            resultado_b is None or np.isnan(resultado_b) or np.isinf(resultado_b)):
            return False
    except Exception:
        return False
    
    # 2. Verificar puntos uniformemente distribuidos (mayor densidad)
    n_verificacion = 1000  # Verificar 1000 puntos en lugar de 10
    puntos_uniformes = np.linspace(a, b, n_verificacion)
    
    try:
        for x in puntos_uniformes:
            resultado = f(x)
            if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                return False
    except Exception:
        return False
    
    # 3. Búsqueda adaptativa de puntos problemáticos
    # Intentar identificar regiones de cambio rápido donde pueden existir problemas
    valores = [f(x) for x in puntos_uniformes]
    diferencias = np.abs(np.diff(valores))
    
    # Si hay cambios muy grandes, verificar con más detalle esas regiones
    umbral_cambio = np.mean(diferencias) + 3 * np.std(diferencias)  # Umbral estadístico
    indices_sospechosos = np.where(diferencias > umbral_cambio)[0]
    
    for i in indices_sospechosos:
        # Verificar con mayor detalle alrededor de los puntos sospechosos
        x_izq = puntos_uniformes[i]
        x_der = puntos_uniformes[i + 1]
        puntos_detallados = np.linspace(x_izq, x_der, 100)  # 100 puntos en el intervalo sospechoso
        
        try:
            for x in puntos_detallados:
                resultado = f(x)
                if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                    return False
        except Exception:
            return False
    
    # 4. Verificar específicamente puntos "redondos" donde pueden haber singularidades
    # (Ejemplo: si tenemos log(x-2), habrá problema en x=2)
    puntos_especiales = []
    # Añadir enteros en el intervalo
    puntos_especiales.extend([i for i in range(int(a), int(b)+1) if a <= i <= b])
    # Añadir fracciones comunes
    for i in range(1, 21):  # Denominadores hasta 20
        for j in range(i):  # Numeradores
            punto = j/i
            if a <= punto <= b:
                puntos_especiales.append(punto)
    # Añadir valores especiales (π, e, etc.)
    valores_especiales = [math.pi, math.e, math.sqrt(2), math.sqrt(3)]
    puntos_especiales.extend([v for v in valores_especiales if a <= v <= b])
    
    # Verificar los puntos especiales y sus alrededores
    for punto in set(puntos_especiales):  # Usar set para eliminar duplicados
        # Verificar el punto exacto
        try:
            resultado = f(punto)
            if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                return False
        except Exception:
            return False
        
        # Verificar alrededor del punto (para detectar discontinuidades)
        if punto > a + tolerancia:
            try:
                resultado = f(punto - tolerancia)
                if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                    return False
            except Exception:
                return False
        
        if punto < b - tolerancia:
            try:
                resultado = f(punto + tolerancia)
                if resultado is None or np.isnan(resultado) or np.isinf(resultado):
                    return False
            except Exception:
                return False
    
    return True  # Si pasó todas las verificaciones, parece estar en el dominio

def get_polygon_coordinates(f, a, b, i, n, method):
    """
    Obtiene las coordenadas para dibujar un polígono (rectángulo o trapecio)
    
    Parámetros:
    f: función a integrar
    a, b: límites del intervalo
    i: índice del subintervalo
    n: número total de subintervalos
    method: método de aproximación
    
    Retorna:
    xs, ys: listas con las coordenadas x e y del polígono
    """
    delta_x = (b - a) / n
    x_left = a + i * delta_x
    x_right = a + (i + 1) * delta_x
    
    if method == 'left':
        y_height = f(x_left)
        xs = [x_left, x_right, x_right, x_left]
        ys = [0, 0, y_height, y_height]
    elif method == 'right':
        y_height = f(x_right)
        xs = [x_left, x_right, x_right, x_left]
        ys = [0, 0, y_height, y_height]
    elif method == 'midpoint':
        x_mid = (x_left + x_right) / 2
        y_height = f(x_mid)
        xs = [x_left, x_right, x_right, x_left]
        ys = [0, 0, y_height, y_height]
    elif method == 'trapezoid':
        y_left = f(x_left)
        y_right = f(x_right)
        xs = [x_left, x_right, x_right, x_left]
        ys = [0, 0, y_right, y_left]
    else:
        raise ValueError("Método no reconocido")
    
    return xs, ys

def graficar_riemann_dinamico(f, a, b, n, method='midpoint', title=None, variable='x'):
    """
    Crea una animación de la aproximación de Riemann.
    
    Parámetros:
    f: función a integrar
    a: límite inferior del intervalo
    b: límite superior del intervalo
    n: número de subintervalos
    method: método de aproximación ('left', 'right', 'midpoint', 'trapezoid')
    title: título opcional para la gráfica
    variable: nombre de la variable de integración
    """
    # Verificar que los límites estén en el dominio de la función
    if not verificar_dominio(f, a, b):
        print(f"Error: Los límites [{a}, {b}] no están completamente dentro del dominio de la función.")
        return None
    
    # Calcular la velocidad de la animación para que dure máximo 5 segundos
    velocidad = 5 / (n + 1)  # +1 para incluir el frame final
    
    # Crear puntos para graficar la función original
    x_func = np.linspace(a, b, 1000)
    y_func = [f(x) for x in x_func]
    
    # Determinar el rango de y para la gráfica
    y_min = min(0, min(y_func))
    y_max = max(y_func) * 1.1
    
    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Graficar la función original
    ax.plot(x_func, y_func, 'b-', linewidth=2, label=f'Función f({variable})')
    
    # Agregar título y etiquetas
    method_names = {
        'left': 'Punto Izquierdo',
        'right': 'Punto Derecho',
        'midpoint': 'Punto Medio',
        'trapezoid': 'Trapecio'
    }
    
    if title is None:
        title = f"Aproximación de Riemann: Método del {method_names[method]} con {n} subintervalos"
    
    ax.set_title(title)
    ax.set_xlabel(variable)
    ax.set_ylabel(f'f({variable})')
    ax.grid(True)
    ax.legend()
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.set_xlim(a, b)
    ax.set_ylim(y_min, y_max)
    
    # Crear texto para mostrar la aproximación
    aprox_text = ax.text(0.05, 0.95, '', transform=ax.transAxes,
                         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    # Crear texto para mostrar la notación de la integral
    integral_text = ax.text(0.05, 0.89, '', transform=ax.transAxes,
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    # Lista para almacenar los polígonos (ahora global)
    poligonos = []
    
    # Inicializar suma
    suma_actual = 0
    delta_x = (b - a) / n
    
    def init():
        # Limpiar los polígonos anteriores
        for p in poligonos:
            p.remove()
        poligonos.clear()
        
        aprox_text.set_text('')
        integral_text.set_text('')
        return aprox_text, integral_text
    
    def animate(i):
        nonlocal suma_actual
        
        # Si es el primer frame, reiniciar la animación
        if i == 0:
            for p in poligonos:
                p.remove()
            poligonos.clear()
            suma_actual = 0
        
        # Si hay más subintervalos por agregar
        if i < n:
            # Calcular las coordenadas del polígono
            xs, ys = get_polygon_coordinates(f, a, b, i, n, method)
            
            # Crear el polígono y agregarlo al gráfico
            poligono = plt.Polygon(list(zip(xs, ys)), fill=True, alpha=0.3, edgecolor='r', facecolor='r')
            ax.add_patch(poligono)
            poligonos.append(poligono)
            
            # Actualizar la suma
            if method == 'left':
                suma_actual += f(a + i * delta_x) * delta_x
            elif method == 'right':
                suma_actual += f(a + (i + 1) * delta_x) * delta_x
            elif method == 'midpoint':
                suma_actual += f(a + (i + 0.5) * delta_x) * delta_x
            elif method == 'trapezoid':
                suma_actual += (f(a + i * delta_x) + f(a + (i + 1) * delta_x)) / 2 * delta_x
            
            # Actualizar el texto de la aproximación
            aprox_text.set_text(f'Aproximación parcial ({i+1}/{n}): {suma_actual:.6f}')
            integral_text.set_text(f'∫({a})^({b}) f({variable}) d{variable} ≈ {suma_actual:.6f}')
        
        # Si es el último frame, mostrar la aproximación final
        elif i == n:
            aprox_text.set_text(f'Aproximación final: {suma_actual:.6f}')
            integral_text.set_text(f'∫({a})^({b}) f({variable}) d{variable} ≈ {suma_actual:.6f}')
        
        # Se debe devolver todos los objetos actualizados
        return [aprox_text, integral_text] + poligonos
    
    # Crear la animación
    frames = n + 1  # Número de subintervalos + 1 para el mensaje final
    ani = FuncAnimation(fig, animate, frames=frames, init_func=init, blit=True, interval=velocidad*1000)
    
    plt.tight_layout()
    plt.show()
    
    # Calcular y devolver la aproximación final
    return riemann_sum(f, a, b, n, method)

def evaluar_expresion(expresion, valor, variable='x'):
    """
    Evalúa una expresión matemática en un valor dado.
    
    Parámetros:
    expresion: string con la expresión matemática
    valor: valor en el que evaluar la expresión
    variable: nombre de la variable a reemplazar
    
    Retorna:
    El resultado de evaluar la expresión
    """
    # Crear un espacio de nombres con las funciones matemáticas
    namespace = {
        'cot': math.cot,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'sqrt': math.sqrt,
        'pi': math.pi,
        'e': math.e,
        'abs': abs,
        'pow': pow,
    }
    
    # Asignar el valor a la variable
    namespace[variable] = valor
    
    try:
        # Evaluar la expresión
        return eval(expresion, {"__builtins__": {}}, namespace)
    except Exception as e:
        print(f"Error al evaluar la expresión: {e}")
        return None
def resolver_integral_exacta(f, a, b, expresion, variable='x'):
    """
    Resuelve la integral de forma exacta y muestra su gráfica.
    
    Parámetros:
    f: función a integrar
    a: límite inferior del intervalo
    b: límite superior del intervalo
    expresion: expresión matemática de la función
    variable: nombre de la variable de integración
    
    Retorna:
    El resultado exacto de la integral
    """
    try:
        # Calcular el resultado exacto
        resultado, error = integrate.quad(f, a, b)
        
        # Crear puntos para graficar la función original
        x_func = np.linspace(a, b, 1000)
        y_func = [f(x) for x in x_func]
        
        # Determinar el rango de y para la gráfica
        y_min = min(0, min(y_func))
        y_max = max(y_func) * 1.1
        
        # Crear la figura y los ejes
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Graficar la función original
        ax.plot(x_func, y_func, 'b-', linewidth=2, label=f'Función f({variable})')
        
        # Rellenar el área bajo la curva
        ax.fill_between(x_func, y_func, alpha=0.3, color='green')
        
        # Agregar título y etiquetas
        ax.set_title(f"Integral exacta de f({variable}) = {expresion}")
        ax.set_xlabel(variable)
        ax.set_ylabel(f'f({variable})')
        ax.grid(True)
        ax.legend()
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.set_xlim(a, b)
        ax.set_ylim(y_min, y_max)
        
        # Agregar texto con el resultado
        ax.text(0.05, 0.95, 
                f'Integral exacta: {resultado:.6f}', 
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        ax.text(0.05, 0.89, 
                f'∫({a})^({b}) f({variable}) d{variable} = {resultado:.6f}', 
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return resultado
        
    except Exception as e:
        print(f"Error al calcular la integral exacta: {e}")
        print("Se procederá con la aproximación numérica.")
        return None

def interfaz_usuario():
    """
    Interfaz para que el usuario defina su propia función y parámetros.
    """
    print("=" * 50)
    print("CALCULADORA DE INTEGRALES Y SUMAS DE RIEMANN")
    print("=" * 50)
    
    # Obtener la expresión matemática
    print("\nIngrese la función a integrar.")
    print("Puede usar funciones matemáticas como sin, cos, tan, exp, log, sqrt, etc.")
    print("Ejemplo: x**2 + sin(x)")
    expresion = input("f(x) = ")
    
    # Permitir al usuario cambiar la variable de integración
    variable = input("\nIngrese la variable de integración (por defecto 'x'): ").strip() or 'x'
    
    # Crear la función
    def funcion_usuario(valor):
        return evaluar_expresion(expresion, valor, variable)
    
    # Comprobar si la función es válida
    try:
        test_value = funcion_usuario(1.0)
        if test_value is None:
            print("La función no es válida. Se usará f(x) = x^2 como ejemplo.")
            funcion_usuario = lambda x: x**2
            expresion = "x**2"
    except Exception as e:
        print(f"Error al crear la función: {e}")
        print("Se usará f(x) = x^2 como ejemplo.")
        funcion_usuario = lambda x: x**2
        expresion = "x**2"
    
    # Obtener límites de integración
    try:
        a = float(input("\nIngrese el límite inferior de integración: "))
        b = float(input("Ingrese el límite superior de integración: "))
        if a >= b:
            print("El límite inferior debe ser menor que el superior. Se usarán 0 y 1.")
            a, b = 0, 1
    except ValueError:
        print("Valores no válidos. Se usarán 0 y 1 como límites.")
        a, b = 0, 1
    
    # Verificar que los límites estén en el dominio de la función
    if not verificar_dominio(funcion_usuario, a, b):
        print(f"Los límites [{a}, {b}] no están completamente dentro del dominio de la función.")
        print("No es posible realizar la integral en este intervalo.")
        respuesta = input("\n¿Desea intentar con otra función o límites? (s/n): ").lower()
        if respuesta == 's':
            interfaz_usuario()
        else:
            print("\n¡Gracias por usar la calculadora de integrales!")
        return
    
    # Preguntar si desea resolución exacta o aproximación por Riemann
    print("\n¿Cómo desea resolver la integral?")
    print("1. Resolución exacta (cuando sea posible)")
    print("2. Aproximación por suma de Riemann")
    
    try:
        opcion = int(input("Seleccione (1-2): "))
        if opcion != 1 and opcion != 2:
            print("Opción no válida. Se usará la resolución exacta.")
            opcion = 1
    except ValueError:
        print("Opción no válida. Se usará la resolución exacta.")
        opcion = 1
    
    # Resolución exacta
    if opcion == 1:
        print("\nCalculando la integral exacta...")
        resultado = resolver_integral_exacta(funcion_usuario, a, b, expresion, variable)
        
        if resultado is not None:
            print(f"\nEl valor exacto de ∫({a})^({b}) {expresion} d{variable} es: {resultado:.6f}")
    
    # Aproximación por suma de Riemann
    else:
        # Obtener número de subintervalos
        try:
            n = int(input("\nIngrese el número de subintervalos: "))
            if n <= 0:
                print("El número de subintervalos debe ser positivo. Se usarán 10.")
                n = 10
        except ValueError:
            print("Valor no válido. Se usarán 10 subintervalos.")
            n = 10
        
        # Obtener método de aproximación
        print("\nSeleccione el método de aproximación:")
        print("1. Punto izquierdo")
        print("2. Punto derecho")
        print("3. Punto medio")
        print("4. Trapecio")
        
        try:
            metodo_num = int(input("Seleccione (1-4): "))
            metodos = ['left', 'right', 'midpoint', 'trapezoid']
            if metodo_num < 1 or metodo_num > 4:
                print("Opción no válida. Se usará el método del punto medio.")
                metodo = 'midpoint'
            else:
                metodo = metodos[metodo_num - 1]
        except ValueError:
            print("Opción no válida. Se usará el método del punto medio.")
            metodo = 'midpoint'
        
        # Graficar la suma de Riemann de forma dinámica
        print("\nCalculando y graficando la suma de Riemann de forma dinámica...")
        print("(La visualización completa se generará en un máximo de 5 segundos)")
        titulo = f"Suma de Riemann para f({variable}) = {expresion}"
        resultado = graficar_riemann_dinamico(funcion_usuario, a, b, n, metodo, titulo, variable)
        
        if resultado is not None:
            print(f"\nLa aproximación de ∫({a})^({b}) {expresion} d{variable} es: {resultado:.6f}")
            
            # Calcular también el valor exacto para comparar
            resultado_exacto = resolver_integral_exacta(funcion_usuario, a, b, expresion, variable)
            if resultado_exacto is not None:
                error = abs(resultado_exacto - resultado)
                print(f"El valor exacto es: {resultado_exacto:.6f}")
                print(f"Error absoluto: {error:.6f}")
                print(f"Error relativo: {(error/abs(resultado_exacto))*100:.4f}%")
    
    # Preguntar si quiere calcular otra integral
    respuesta = input("\n¿Desea calcular otra integral? (s/n): ").lower()
    if respuesta == 's':
        interfaz_usuario()
    else:
        print("\n¡Gracias por usar la calculadora de integrales!")

# Ejecutar la interfaz de usuario
if __name__ == "__main__":
    interfaz_usuario()