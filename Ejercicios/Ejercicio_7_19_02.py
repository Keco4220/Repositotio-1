import math
def factorial(n):
    fact = 1
    for i in range(1, n + 1):
        fact *= i
    return fact 

def taylor_sin(x, tol=1e-10):
    term = x
    sum_sin = term
    n = 1

    while abs(term) > tol:
        term = (-1) ** n * (x ** (2 * n + 1))/factorial(2 * n + 1)
        sum_sin += term
        n += 1
    return sum_sin

x = float(input("Ingresa el valor de x en radianes: "))
resultado = taylor_sin(x)
print(f"La aproximación de Sen(x) con series de Taylor es: {resultado}")
print(f"Valor real usado math.sin: {math.sin(x)}")