semestre=eval(input("¿Que semestre cursa actualmente?"))
if semestre == 1:
    print("No pasa nada")
elif 2 <= semestre <= 5:
    materias = input("¿Ha perdido Usted alguna materia? (Y o N)")
    if materias == "N":
        print("Recuerde que debe estar nivelado con el pensum para poder pasar al 6to semestre")
    elif materias == "Y":
        pre = input("¿Alguna de dichas materias es prerrequisitos? (Y o N)")
        if pre == "Y":
            print("Tenga en cuenta que va atrasado con los requisitos para avanzar en el programa, pongase al día")
        elif pre == "N":
            print("Recuerde ponerse al día con las materias perdidas para avanzar")
        else:
            print("ERROR: Opcion inalida")
elif 6 <= semestre <= 8:
    GI = input("¿Pertenece a algún grupo de investigación? (Y o N)")


