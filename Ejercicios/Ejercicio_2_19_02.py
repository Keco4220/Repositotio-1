numero = int(input("Inserte un número real y entero: " ))
if numero < 0:
    print("El factorial no está definido para números negativos")
elif numero == 0:
    print("El factorial definido para 0 es 1")
elif numero >= 1:
    resultado = 1
    for i in range(1, numero+1):
        resultado *= i
    print(f"El Factorial de {numero} es igual a {resultado}") 