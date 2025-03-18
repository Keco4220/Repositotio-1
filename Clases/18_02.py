for i in range (10, 1, -1):
    print(i)

tiempo = 0
velocidad = float(input("Ingrese la velocidad inicial:"))
aceleración = -9.8
    
while velocidad > 0:
    velocidad += aceleración*tiempo
    tiempo += 0.00001

print(f"el tiempo  buscado es {tiempo}")

for i in range (1,10):
    print("#"*10)

for i in (17, 12, 16, 2, 3):
    print(i)
for i in ("Maneskin", "Imagine Dragons", "Daniel, me Estás Matando", "Hozier", "Laufey"):
    print (i)
for i,j in enumerate(("Maneskin", "Imagine Dragons", "Daniel, me Estás Matando", "Hozier", "Laufey")):
    print (i+1,j)

    suma=0
for i,j,k in zip(["Maneskin", "Imagine Dragons", "Daniel, me Estás Matando", "Hozier", "Laufey"],[120, 250, 320, 159, 45],["Colombia", "Colombia", "Mexico", "USA", "Canadá"]):
    print(i,j,k)
    suma += j
    
    if suma >=1000:
        break

else:
    print(f"Costo total de los artistas:{suma}" )
    print("Exito!")
print("Bye")