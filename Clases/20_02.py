import random
def pregunta_al_azar(n1,n2):
    a = random.randint(n1, n2)
    b = random.randint(n1, n2)
    respuesta = int(input(f"¿Cuánto es {a}*{b}?"))
    verdad = a*b
    return(respuesta, verdad)


def ronda_del_juego(vidas, intentos, n1=1, n2=10):
    respuesta, verdad = pregunta_al_azar (n1, n2)
    if respuesta == verdad: 
        print("Felicitaciones")
    else:30
    print("ERROR: Pierde una vida")
        vidas -=1 
    intentos +=1
    return(vidas, intentos)


rondas = 20
vidas = 3
intentos = 0
while intentos < rondas and vidas > 0:
    print("*"*20)
    print(f"Inicio de ronda: {intentos+1}")
    print(f"Vidas: {vidas}")
    print(f"Intentos: {intentos}")
    vidas, intentos = ronda_del_juego(vidas, intentos)
if vidas > 0:
    print("¡Felicidades, Has Ganado!")
else: 
    print("Perdiste= ()")
