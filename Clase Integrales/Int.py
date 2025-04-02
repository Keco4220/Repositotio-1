import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from matplotlib.animation import FuncAnimation
from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional

class Funcion(ABC):
    """Clase abstracta base para representar funciones matemáticas"""
    
    @abstractmethod
    def evaluar(self, x: float) -> float:
        """Evalúa la función en el punto x"""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Representación en cadena de la función"""
        pass
    
    def dominio_valido(self, a: float, b: float) -> bool:
        """Verifica si el intervalo [a, b] está en el dominio de la función"""
        return verificar_dominio(self.evaluar, a, b)

class FuncionExpresion(Funcion):
    """Representa una función definida por una expresión matemática"""
    
    def __init__(self, expresion: str, variable: str = 'x'):
        self.expresion = expresion
        self.variable = variable
        self._namespace = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'exp': math.exp, 'log': math.log, 'log10': math.log10,
            'sqrt': math.sqrt, 'pi': math.pi, 'e': math.e,
            'abs': abs, 'pow': pow
        }
    
    def evaluar(self, x: float) -> float:
        self._namespace[self.variable] = x
        try:
            return eval(self.expresion, {"__builtins__": {}}, self._namespace)
        except Exception:
            return float('nan')
    
    def __str__(self) -> str:
        return f"f({self.variable}) = {self.expresion}"

class Integrador(ABC):
    """Clase abstracta para métodos de integración"""
    
    def __init__(self, funcion: Funcion):
        self.funcion = funcion
    
    @abstractmethod
    def integrar(self, a: float, b: float, **kwargs) -> float:
        """Realiza la integración en el intervalo [a, b]"""
        pass
    
    @abstractmethod
    def graficar(self, a: float, b: float, **kwargs) -> None:
        """Muestra gráficamente el proceso de integración"""
        pass

class RiemannIntegrator(Integrador):
    """Implementa la integración por sumas de Riemann"""
    
    METODOS = {
        'left': 'Punto Izquierdo',
        'right': 'Punto Derecho',
        'midpoint': 'Punto Medio',
        'trapezoid': 'Trapecio'
    }
    
    def __init__(self, funcion: Funcion, metodo: str = 'midpoint'):
        super().__init__(funcion)
        if metodo not in self.METODOS:
            raise ValueError(f"Método no válido. Use uno de: {list(self.METODOS.keys())}")
        self.metodo = metodo
    
    def integrar(self, a: float, b: float, n: int = 1000) -> float:
        if n <= 0:
            raise ValueError("El número de subintervalos debe ser positivo")
        
        delta_x = (b - a) / n
        suma = 0
        
        for i in range(n):
            if self.metodo == 'left':
                x = a + i * delta_x
                suma += self.funcion.evaluar(x) * delta_x
            elif self.metodo == 'right':
                x = a + (i + 1) * delta_x
                suma += self.funcion.evaluar(x) * delta_x
            elif self.metodo == 'midpoint':
                x = a + (i + 0.5) * delta_x
                suma += self.funcion.evaluar(x) * delta_x
            elif self.metodo == 'trapezoid':
                x_left = a + i * delta_x
                x_right = a + (i + 1) * delta_x
                suma += (self.funcion.evaluar(x_left) + self.funcion.evaluar(x_right)) / 2 * delta_x
        
        return suma
    
    def graficar(self, a: float, b: float, n: int = 100, titulo: str = None) -> None:
        if not self.funcion.dominio_valido(a, b):
            print(f"Error: Los límites [{a}, {b}] no están completamente dentro del dominio de la función.")
            return
        
        velocidad = 5 / (n + 1)
        x_func = np.linspace(a, b, 1000)
        y_func = [self.funcion.evaluar(x) for x in x_func]
        y_min, y_max = min(0, min(y_func)), max(y_func) * 1.1
        
        fig, ax = plt.subplots(figsize=(12, 6))
        line, = ax.plot(x_func, y_func, 'b-', linewidth=2, label=f'Función {self.funcion}')
        
        if titulo is None:
            titulo = f"Aproximación de Riemann: Método del {self.METODOS[self.metodo]} con {n} subintervalos"
        
        ax.set_title(titulo)
        ax.set_xlabel(self.funcion.variable)
        ax.set_ylabel(f'f({self.funcion.variable})')
        ax.grid(True)
        ax.legend()
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.set_xlim(a, b)
        ax.set_ylim(y_min, y_max)
        
        aprox_text = ax.text(0.05, 0.95, '', transform=ax.transAxes,
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        integral_text = ax.text(0.05, 0.89, '', transform=ax.transAxes,
                               bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        
        # Lista para almacenar los polígonos
        rectangulos = []
        
        # Inicializar suma
        suma_actual = 0
        delta_x = (b - a) / n
        
        def init():
            # Limpiar los polígonos anteriores
            for rect in rectangulos:
                rect.remove()
            rectangulos.clear()
            
            aprox_text.set_text('')
            integral_text.set_text('')
            return [aprox_text, integral_text]
        
        def animate(i):
            nonlocal suma_actual
            
            if i == 0:
                for rect in rectangulos:
                    rect.remove()
                rectangulos.clear()
                suma_actual = 0
            
            if i < n:
                # Calcular las coordenadas del polígono
                x_left = a + i * delta_x
                x_right = a + (i + 1) * delta_x
                
                if self.metodo == 'left':
                    y_height = self.funcion.evaluar(x_left)
                    xs = [x_left, x_right, x_right, x_left]
                    ys = [0, 0, y_height, y_height]
                elif self.metodo == 'right':
                    y_height = self.funcion.evaluar(x_right)
                    xs = [x_left, x_right, x_right, x_left]
                    ys = [0, 0, y_height, y_height]
                elif self.metodo == 'midpoint':
                    x_mid = (x_left + x_right) / 2
                    y_height = self.funcion.evaluar(x_mid)
                    xs = [x_left, x_right, x_right, x_left]
                    ys = [0, 0, y_height, y_height]
                elif self.metodo == 'trapezoid':
                    y_left = self.funcion.evaluar(x_left)
                    y_right = self.funcion.evaluar(x_right)
                    xs = [x_left, x_right, x_right, x_left]
                    ys = [0, 0, y_right, y_left]
                
                # Crear y agregar el polígono
                poligono = plt.Polygon(list(zip(xs, ys)), fill=True, alpha=0.3, edgecolor='r', facecolor='r')
                ax.add_patch(poligono)
                rectangulos.append(poligono)
                
                # Actualizar la suma
                if self.metodo == 'left':
                    suma_actual += self.funcion.evaluar(x_left) * delta_x
                elif self.metodo == 'right':
                    suma_actual += self.funcion.evaluar(x_right) * delta_x
                elif self.metodo == 'midpoint':
                    suma_actual += self.funcion.evaluar((x_left + x_right)/2) * delta_x
                elif self.metodo == 'trapezoid':
                    suma_actual += (self.funcion.evaluar(x_left) + self.funcion.evaluar(x_right)) / 2 * delta_x
                
                # Actualizar los textos
                aprox_text.set_text(f'Aproximación parcial ({i+1}/{n}): {suma_actual:.6f}')
                integral_text.set_text(f'∫({a})^({b}) {self.funcion} d{self.funcion.variable} ≈ {suma_actual:.6f}')
            
            elif i == n:
                aprox_text.set_text(f'Aproximación final: {suma_actual:.6f}')
                integral_text.set_text(f'∫({a})^({b}) {self.funcion} d{self.funcion.variable} ≈ {suma_actual:.6f}')
            
            return [aprox_text, integral_text] + rectangulos
        
        # Crear la animación
        ani = FuncAnimation(fig, animate, frames=n+1, init_func=init, blit=True, interval=velocidad*1000)
        
        plt.tight_layout()
        plt.show()

class ExactIntegrator(Integrador):
    """Implementa la integración exacta cuando es posible"""
    
    def integrar(self, a: float, b: float, **kwargs) -> float:
        try:
            resultado, _ = integrate.quad(self.funcion.evaluar, a, b)
            return resultado
        except Exception as e:
            print(f"Error al calcular la integral exacta: {e}")
            return float('nan')
    
    def graficar(self, a: float, b: float, **kwargs) -> None:
        if not self.funcion.dominio_valido(a, b):
            print(f"Error: Los límites [{a}, {b}] no están completamente dentro del dominio de la función.")
            return
        
        x_func = np.linspace(a, b, 1000)
        y_func = [self.funcion.evaluar(x) for x in x_func]
        y_min, y_max = min(0, min(y_func)), max(y_func) * 1.1
        
        resultado = self.integrar(a, b)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x_func, y_func, 'b-', linewidth=2, label=f'Función {self.funcion}')
        ax.fill_between(x_func, y_func, alpha=0.3, color='green')
        
        ax.set_title(f"Integral exacta de {self.funcion}")
        ax.set_xlabel(self.funcion.variable)
        ax.set_ylabel(f'f({self.funcion.variable})')
        ax.grid(True)
        ax.legend()
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.set_xlim(a, b)
        ax.set_ylim(y_min, y_max)
        
        ax.text(0.05, 0.95, f'Integral exacta: {resultado:.6f}', 
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        ax.text(0.05, 0.89, f'∫({a})^({b}) {self.funcion} d{self.funcion.variable} = {resultado:.6f}', 
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
        
        plt.tight_layout()
        plt.show()

def verificar_dominio(f: Callable, a: float, b: float, tolerancia: float = 1e-6) -> bool:
    """Verifica si el intervalo [a, b] está dentro del dominio de la función"""
    try:
        if np.isnan(f(a)) or np.isnan(f(b)) or np.isinf(f(a)) or np.isinf(f(b)):
            return False
        
        puntos_uniformes = np.linspace(a, b, 1000)
        for x in puntos_uniformes:
            if np.isnan(f(x)) or np.isinf(f(x)):
                return False
        
        valores = [f(x) for x in puntos_uniformes]
        diferencias = np.abs(np.diff(valores))
        umbral = np.mean(diferencias) + 3 * np.std(diferencias)
        indices = np.where(diferencias > umbral)[0]
        
        for i in indices:
            x_izq, x_der = puntos_uniformes[i], puntos_uniformes[i+1]
            puntos_detallados = np.linspace(x_izq, x_der, 100)
            for x in puntos_detallados:
                if np.isnan(f(x)) or np.isinf(f(x)):
                    return False
        
        puntos_especiales = []
        puntos_especiales.extend([i for i in range(int(a), int(b)+1) if a <= i <= b])
        for i in range(1, 21):
            for j in range(i):
                punto = j/i
                if a <= punto <= b:
                    puntos_especiales.append(punto)
        
        valores_especiales = [math.pi, math.e, math.sqrt(2), math.sqrt(3)]
        puntos_especiales.extend([v for v in valores_especiales if a <= v <= b])
        
        for punto in set(puntos_especiales):
            if np.isnan(f(punto)) or np.isinf(f(punto)):
                return False
            if punto > a + tolerancia and (np.isnan(f(punto - tolerancia)) or np.isinf(f(punto - tolerancia))):
                return False
            if punto < b - tolerancia and (np.isnan(f(punto + tolerancia)) or np.isinf(f(punto + tolerancia))):
                return False
        
        return True
    except Exception:
        return False

class CalculadoraIntegrales:
    """Interfaz de usuario para el sistema de cálculo de integrales"""
    
    def __init__(self):
        self.funcion: Optional[Funcion] = None
        self.integrador: Optional[Integrador] = None
    
    def ejecutar(self):
        print("=" * 50)
        print("CALCULADORA DE INTEGRALES")
        print("=" * 50)
        
        self._definir_funcion()
        self._definir_limites()
        
        if not self.funcion.dominio_valido(self.a, self.b):
            print(f"Error: Los límites [{self.a}, {self.b}] no están en el dominio de la función.")
            return
        
        self._seleccionar_metodo()
        self._mostrar_resultados()
        
        if input("\n¿Desea calcular otra integral? (s/n): ").lower() == 's':
            self.ejecutar()
        else:
            print("\n¡Gracias por usar la calculadora de integrales!")
    
    def _definir_funcion(self):
        print("\nIngrese la función a integrar (use 'x' como variable):")
        print("Ejemplos: x**2 + sin(x), exp(-x**2), log(x+1)")
        expresion = input("f(x) = ")
        variable = input("Variable de integración (por defecto 'x'): ").strip() or 'x'
        
        self.funcion = FuncionExpresion(expresion, variable)
        
        # Verificar que la función sea válida
        try:
            test_val = self.funcion.evaluar(1.0)
            if np.isnan(test_val):
                raise ValueError
        except:
            print("Función no válida. Se usará f(x) = x^2 como ejemplo.")
            self.funcion = FuncionExpresion("x**2")
    
    def _definir_limites(self):
        try:
            self.a = float(input("\nLímite inferior de integración: "))
            self.b = float(input("Límite superior de integración: "))
            if self.a >= self.b:
                print("El límite inferior debe ser menor. Se usarán 0 y 1.")
                self.a, self.b = 0, 1
        except ValueError:
            print("Valores no válidos. Se usarán 0 y 1.")
            self.a, self.b = 0, 1
    
    def _seleccionar_metodo(self):
        print("\nMétodos de integración disponibles:")
        print("1. Resolución exacta (cuando sea posible)")
        print("2. Aproximación por suma de Riemann")
        
        try:
            opcion = int(input("Seleccione (1-2): "))
            if opcion == 1:
                self.integrador = ExactIntegrator(self.funcion)
            elif opcion == 2:
                metodo = self._seleccionar_metodo_riemann()
                n = self._obtener_subintervalos()
                self.integrador = RiemannIntegrator(self.funcion, metodo)
                self.n = n
            else:
                print("Opción no válida. Se usará resolución exacta.")
                self.integrador = ExactIntegrator(self.funcion)
        except ValueError:
            print("Opción no válida. Se usará resolución exacta.")
            self.integrador = ExactIntegrator(self.funcion)
    
    def _seleccionar_metodo_riemann(self) -> str:
        print("\nMétodos de aproximación de Riemann:")
        print("1. Punto izquierdo")
        print("2. Punto derecho")
        print("3. Punto medio")
        print("4. Trapecio")
        
        try:
            opcion = int(input("Seleccione (1-4): "))
            metodos = ['left', 'right', 'midpoint', 'trapezoid']
            return metodos[opcion - 1]
        except (ValueError, IndexError):
            print("Opción no válida. Se usará punto medio.")
            return 'midpoint'
    
    def _obtener_subintervalos(self) -> int:
        try:
            n = int(input("\nNúmero de subintervalos (recomendado >100): "))
            return max(1, n)
        except ValueError:
            print("Valor no válido. Se usarán 100 subintervalos.")
            return 100
    
    def _mostrar_resultados(self):
        print("\nCalculando...")
        
        if isinstance(self.integrador, ExactIntegrator):
            resultado = self.integrador.integrar(self.a, self.b)
            self.integrador.graficar(self.a, self.b)
            print(f"\nResultado exacto: {resultado:.6f}")
        
        elif isinstance(self.integrador, RiemannIntegrator):
            titulo = f"Aproximación de {self.funcion} entre {self.a} y {self.b}"
            resultado = self.integrador.integrar(self.a, self.b, self.n)
            self.integrador.graficar(self.a, self.b, self.n, titulo)
            print(f"\nAproximación: {resultado:.6f}")
            
            # Comparar con valor exacto si es posible
            exact_integrator = ExactIntegrator(self.funcion)
            try:
                exacto = exact_integrator.integrar(self.a, self.b)
                if not np.isnan(exacto):
                    error = abs(exacto - resultado)
                    print(f"Valor exacto: {exacto:.6f}")
                    print(f"Error absoluto: {error:.6f}")
                    print(f"Error relativo: {error/abs(exacto)*100:.4f}%")
            except:
                pass

# Ejecutar la aplicación
if __name__ == "__main__":
    app = CalculadoraIntegrales()
    app.ejecutar()