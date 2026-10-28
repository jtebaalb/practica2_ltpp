import random

LISTA_LETRAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
MAP_LETRAS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

def crear_tabla(filas, columnas):
    tablero = []
    for i in range(filas):
        fila = ["-"] * columnas
        tablero.append(fila)
    return tablero

def mostrar_tabla(tablero):
    print("   ABCDEFGHIJ")
    for i in range(10):
        linea = str(i + 1) + ":"
        for j in range(10):
            linea = linea + tablero[i][j]
        print(linea)

def coord_a_pos(coord):
    letra = coord[0]
    numero = int(coord[1:])
    fila = numero - 1
    columna = MAP_LETRAS[letra]
    return (fila, columna)

def pos_a_coord(i, j):
    letra = LISTA_LETRAS[j]
    numero = str(i + 1)
    return letra + numero

def celda_libre(tablero, fila, col):
    for f in range(fila - 1, fila + 2):
        for c in range(col - 1, col + 2):
            if f >= 0 and f <= 9 and c >= 0 and c <= 9:
                if tablero[f][c] != "-":
                    return False
    return True

def situar_barco(tablero, i, j, tamano, orientacion, colocar):
    for paso in range(tamano):
        if orientacion == 0:
            f = i
            c = j + paso
        else:
            f = i + paso
            c = j
            
        if colocar == False:
            if celda_libre(tablero, f, c) == False:
                return False
        else:
            tablero[f][c] = "O"
            
    return True

def colocar_flota(tablero):
    flota = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    
    for tamano in flota:
        colocado = False
        while colocado == False:
            orientacion = random.randint(0, 1)
            
            if orientacion == 0:
                i = random.randint(0, 9)
                j = random.randint(0, 10 - tamano)
            else:
                i = random.randint(0, 10 - tamano)
                j = random.randint(0, 9)
                
            if situar_barco(tablero, i, j, tamano, orientacion, False) == True:
                situar_barco(tablero, i, j, tamano, orientacion, True)
                colocado = True

print("Bienvenido a Hundir la Flota!!!")
print("Voy a distribuir mis barcos")

tablero_ordenador = crear_tabla(10, 10)
colocar_flota(tablero_ordenador)

print("Ya está. Podemos empezar:")
mostrar_tabla(tablero_ordenador)