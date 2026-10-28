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
    letra = coord[0].upper()
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
            if 0 <= f <= 9 and 0 <= c <= 9:
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
            
        if not colocar:
            if not celda_libre(tablero, f, c):
                return False
        else:
            tablero[f][c] = "O"
            
    return True


def colocar_flota(tablero):
    flota = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for tamano in flota:
        colocado = False
        while not colocado:
            orientacion = random.randint(0, 1)
            if orientacion == 0:
                i = random.randint(0, 9)
                j = random.randint(0, 10 - tamano)
            else:
                i = random.randint(0, 10 - tamano)
                j = random.randint(0, 9)
                
            if situar_barco(tablero, i, j, tamano, orientacion, False):
                situar_barco(tablero, i, j, tamano, orientacion, True)
                colocado = True


def es_coordenada_valida(coord):
    if len(coord) < 2 or len(coord) > 3:
        return False
    letra = coord[0].upper()
    numero_str = coord[1:]
    if letra not in MAP_LETRAS:
        return False
    if not numero_str.isdigit():
        return False
    numero = int(numero_str)
    if numero < 1 or numero > 10:
        return False
    return True


def crear_lista_pdt():
    pdt = []
    for i in range(10):
        for j in range(10):
            pdt.append((i, j))
    return pdt


def eliminar_perimetro(barco_tocado, pdt):
    for (f_b, c_b) in barco_tocado:
        for f in range(f_b - 1, f_b + 2):
            for c in range(c_b - 1, c_b + 2):
                if (f, c) in pdt:
                    pdt.remove((f, c))


def jugar():
    print("Bienvenido a Hundir la Flota!!!")
    print("Voy a distribuir mis barcos")
    
    tablero_ordenador = crear_tabla(10, 10)
    colocar_flota(tablero_ordenador)
    
    tablero_disparos_usuario = crear_tabla(10, 10)
    
    print("Ya está. Podemos empezar:")
    mostrar_tabla(tablero_ordenador)
    mostrar_tabla(tablero_disparos_usuario)
    
    pdt = crear_lista_pdt()
    candidatos_ia = []
    barco_actual_ia = []
    
    aciertos_usuario = 0
    aciertos_ia = 0
    
    while aciertos_usuario < 20 and aciertos_ia < 20:
        # --- TURNO DEL USUARIO ---
        jugada_valida = False
        while not jugada_valida:
            coord_str = input("Introduce tu jugada (ej. A5): ").strip().upper()
            if not es_coordenada_valida(coord_str):
                print("Coordenada inválida. Debe ser una letra (A-J) y un número (1-10).")
                continue
                
            f_u, c_u = coord_a_pos(coord_str)
            if tablero_disparos_usuario[f_u][c_u] != "-":
                print("Ya has disparado en esa posición. Elige otra.")
            else:
                jugada_valida = True
                
        if tablero_ordenador[f_u][c_u] == "O":
            print("Tocado!")
            tablero_disparos_usuario[f_u][c_u] = "X"
            aciertos_usuario += 1
        else:
            print("Agua. Has fallado.")
            tablero_disparos_usuario[f_u][c_u] = "+"
            
        print("\nTu mapa de disparos:")
        mostrar_tabla(tablero_disparos_usuario)
        
        if aciertos_usuario == 20:
            print("¡Felicidades! Has hundido toda mi flota. ¡Has ganado!")
            break
            
        # --- TURNO DEL ORDENADOR ---
        disparo_ia = None
        while len(candidatos_ia) > 0:
            candidato = candidatos_ia.pop(0)
            if candidato in pdt:
                disparo_ia = candidato
                pdt.remove(disparo_ia)
                break
                
        if disparo_ia is None:
            idx = random.randint(0, len(pdt) - 1)
            disparo_ia = pdt.pop(idx)
            
        f_ia, c_ia = disparo_ia
        print(f"\nAhora tiro yo: {pos_a_coord(f_ia, c_ia)}")
        
        resp_valida = False
        while not resp_valida:
            resp = input("¿Cómo ha resultado mi disparo (A: agua, T: tocado, H: hundido)?: ").strip().upper()
            if resp in ['A', 'T', 'H']:
                resp_valida = True
            else:
                print("Respuesta no válida. Debe ser A, T o H.")
                
        if resp == "A":
            pass
        elif resp == "T":
            print("Jaja, voy a por ti")
            aciertos_ia += 1
            barco_actual_ia.append((f_ia, c_ia))
            
            vecinos = [(f_ia - 1, c_ia), (f_ia + 1, c_ia), (f_ia, c_ia - 1), (f_ia, c_ia + 1)]
            for vf, vc in vecinos:
                if 0 <= vf <= 9 and 0 <= vc <= 9:
                    if (vf, vc) in pdt and (vf, vc) not in candidatos_ia:
                        candidatos_ia.append((vf, vc))
        elif resp == "H":
            print("¡Barco hundido!")
            aciertos_ia += 1
            barco_actual_ia.append((f_ia, c_ia))
            eliminar_perimetro(barco_actual_ia, pdt)
            barco_actual_ia = []
            candidatos_ia = []
            
        if aciertos_ia == 20:
            print("¡He hundido todos tus barcos! He ganado la partida.")
            break


jugar()