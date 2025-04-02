# Calculadora de Integrales

Una aplicación interactiva para visualizar y calcular integrales mediante diferentes métodos numéricos.

## Descripción

Esta calculadora de integrales proporciona una interfaz de usuario para calcular integrales definidas utilizando diferentes métodos:
- Integración exacta (mediante SciPy)
- Aproximación por sumas de Riemann con cuatro variantes:
  - Punto izquierdo
  - Punto derecho
  - Punto medio
  - Método del trapecio

La aplicación no solo calcula los valores, sino que también visualiza gráficamente el proceso de integración, lo que resulta útil para propósitos educativos y de comprensión conceptual.

## Características

- Definición y evaluación de funciones matemáticas
- Verificación automática del dominio de las funciones
- Cálculo de integrales definidas exactas
- Aproximación por sumas de Riemann con número variable de subintervalos
- Visualización animada del proceso de integración
- Comparación entre el valor exacto y la aproximación numérica
- Cálculo de errores absolutos y relativos

## Requisitos

```
numpy
matplotlib
scipy
```

## Uso

1. Ejecuta el script: `python calculadora_integrales.py`
2. Sigue las instrucciones en consola:
   - Ingresa la función a integrar utilizando sintaxis de Python
   - Define los límites de integración
   - Selecciona el método de integración deseado
   - Para aproximaciones de Riemann, elige el método específico y el número de subintervalos

## Ejemplo de uso

```python
# Al ejecutar la aplicación:
# 1. Ingresa la función, por ejemplo: x**2 + sin(x)
# 2. Define los límites, por ejemplo: 0 y 3
# 3. Selecciona el método de integración
# 4. Para método de Riemann, selecciona la variante y número de subintervalos
```

## Estructura del código

- `Funcion`: Clase abstracta base para representar funciones matemáticas
- `FuncionExpresion`: Implementación concreta para funciones definidas mediante expresiones
- `Integrador`: Clase abstracta para los métodos de integración
- `RiemannIntegrator`: Implementa integración por sumas de Riemann con diferentes variantes
- `ExactIntegrator`: Implementa integración exacta mediante scipy.integrate
- `CalculadoraIntegrales`: Interfaz de usuario para el sistema

## Implementación técnica

La calculadora utiliza programación orientada a objetos con herencia y polimorfismo para representar diferentes tipos de funciones y métodos de integración. La visualización se realiza con matplotlib, incluyendo animaciones del proceso de aproximación.

## Nota de uso

Para funciones con comportamiento especial (asíntotas, discontinuidades, etc.), la herramienta incluye detección automática de dominio para evitar cálculos erróneos.
