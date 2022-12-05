# TODOS 
# - AGREGAR UNA ANIMACION CUANDO SE INCREMENTA DE NIVEL
# - AGREGAR UNA ANIMACION CON LOS PUNTOS GANADOS CUANDO SE ELIMINA UNA FILA 
# - AGREGAR UNA ANIMACION CUANDO SE CONSIGUE UN TETRIS
# - CAMBIAR EL SISTEMA DE PUNTOS PARA GANAR MAS PUNTOS ENTRE MAS FILAS ELIMINES A LA VEZ
# - HACER UN ARRAY 'PIEZAS_RECT_PREV' QUE CONTENGA LOS MISMOS RECTANGULOS QUE
#       'PIEZAS_RECT' PERO COLOCADOS LO MAS BAJO POSIBLE, EVITANDO COLISIONES
# - DIBUJAR ESOS RECTANGULOS CON UN BORDE DEL COLOR DE LA PIEZA 
# - IMPLEMENTAR UNA FUNCION 'AUTO_BLOQUEAR' QUE AL PRESIONAR LA TECLA ESPACIO
#       COLOQUE LOS RECTANGULOS DE 'PIEZAS_RECT' EN LA POSICION DE LOS RECTANGULOS
#       DE 'PIEZA_RECT_PREV' 
# - HACER QUE LAS FUNCIONES 'GENERAR_PIEZA', 'GENERAR_PIEZA_RECT', 'BLOQUEAR_PIEZA'
#       'GIRAR_PIEZA', Y 'ACTUALIZAR_PIEZA_RECT' APLIQUEN TAMBIEN PARA EL ARREGLO
#        'PIEZAS_RECT_PREV'
# - IMPLEMENTAR UN MENU

import pygame, sys, random
pygame.init()

# CONFIG INICIAL
pygame.display.set_caption('Tetris')
screen = pygame.display.set_mode((630, 650))
screen.fill('white')
clock = pygame.time.Clock()
game_over = False
FPS = 60

# MUSICA DE FONDO
pygame.mixer.music.load('./audio/music/tetris-ost.mp3')
pygame.mixer.music.play(-1)

# SONIDOS
line_clear = pygame.mixer.Sound('./audio/sound-effects/line-clear.mp3')

# AREA DE JUEGO
game_surf = pygame.Surface((360, 648))
game_surf.fill('grey')

# AREA DE INFO
info_surf = pygame.Surface((270, 650))
info_surf.fill('black')

# LOGO (DIMENSIONES ORIGINALES: 300x209 REESCALADO: 231x140)
logo_surf = pygame.image.load('./assets/img/logo.png').convert_alpha()
logo_surf = pygame.transform.scale(logo_surf, (231,140))

# FUENTE Y TEXTOS
font = pygame.font.Font('./font/Tetris.ttf', 20)
score_text = font.render('Score: 0', True, ('white'))
level_text = font.render('Level: 1', True, ('white'))
lines_text = font.render('Lines: 0', True, ('white'))
next_text = font.render('Next:', True, ('white'))
hold_text = font.render('Hold:', True, ('white'))
 
# SE DEFINE LA PUNTUACION, NIVEL Y FILAS ELIMINADAS
score = 0
lines = 0
level = 1

# AREA DONDE ESTARA LA PIEZA GUARDADA Y LA SIGUIENTE PIEZA
next_surf = pygame.Surface((145,145))
next_surf.fill('black')
hold_surf = pygame.Surface((145,145))
hold_surf.fill('black')

# MATRIZ FONDO 10x18 QUE CONTIENE LOS 'SURFACES' DEL FONDO
matriz_fondo = []
for f in range(18):
    matriz_fondo.append([])
    for c in range(10):
        matriz_fondo[f].append(pygame.Surface((35, 35)))
        matriz_fondo[f][c].fill('black')

# SE DEFINE LA VELOCIDAD DE LA GRAVEDAD
gravedad = 0
v_facil = 25
v_intermedia = 20
v_dificil = 15
v_extrema = 10
velocidad_gravedad = v_facil
aumentar_velocidad = False

# LISTA CON LOS 'RECTANGLES' DE LAS PIEZAS BLOQUEADAS
piezas_bloqueadas = []

# MATRIZ DONDE SE GUARDA LA PIEZA GUARDADA
piezas_guardadas = []

# LISTA DONDE SE GUARDAN LOS 'RECTANGLES' DE LAS PIEZAS GUARDADAS
piezas_guardadas_rect = []

# LISTA DONDE SE GUARDARAN LOS RECTANGULOS DE LAS PIEZAS
piezas_rect = []

# LISTA DONDE SE GUARDARAN LOS RECTANGLUS DE LA SIGUIENTE PIEZA
sig_piezas_rect = []

# LISTA DONDE SE GUARDA EL NUMERO DE FILAS LLENAS
filas_llenas = []

# SURFACES DE LAS CUALES SE VAN A GENERARAR LOS RECTANGULOS DE LAS PIEZAS
O_surf = pygame.image.load('./assets/textures/O.png').convert_alpha()
I_surf = pygame.image.load('./assets/textures/I.png').convert_alpha()
S_surf = pygame.image.load('./assets/textures/S.png').convert_alpha()
J_surf = pygame.image.load('./assets/textures/J.png').convert_alpha()
L_surf = pygame.image.load('./assets/textures/L.png').convert_alpha()
Z_surf = pygame.image.load('./assets/textures/Z.png').convert_alpha()
T_surf = pygame.image.load('./assets/textures/T.png').convert_alpha()

# MATRICES 4x4 DE LAS PIEZAS, INDICANDO CON UN 1 LAS POSICIONES DE LA PIEZA
sig_pieza = []
pieza = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]
I = [
    [
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0]
    ],
    [
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
]
O = [
    [
        [1,1,0,0],
        [1,1,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
]
S = [
    [
        [0,1,1,0],
        [1,1,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,0,0,0]
    ]
]
J = [
    [
        [0,1,0,0],
        [0,1,0,0],
        [1,1,0,0],
        [0,0,0,0]
    ],
    [
        [1,0,0,0],
        [1,1,1,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [1,1,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [0,0,0,0]
    ],
    [
        [1,1,1,0],
        [0,0,1,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
]
L = [
    [
        [1,0,0,0],
        [1,0,0,0],
        [1,1,0,0],
        [0,0,0,0]
    ],
    [
        [1,1,1,0],
        [1,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [1,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
        [0,0,0,0]
    ],
    [
        [0,0,1,0],
        [1,1,1,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
]
Z = [
    [
        [1,1,0,0],
        [0,1,1,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0],
        [0,0,0,0]
    ]
]
T = [
    [
        [0,1,0,0],
        [1,1,1,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [1,0,0,0],
        [1,1,0,0],
        [1,0,0,0],
        [0,0,0,0]
    ],
    [
        [1,1,1,0],
        [0,1,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [0,1,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,0,0,0]
    ]
]

# BOLSA DE LAS MATRICES DE LAS PIEZAS
bolsa_piezas = [I,O,S,J,L,Z,T]

# FUNCIONES
def cambiar_dificultad(nueva_velocidad):
    global velocidad_gravedad
    global level
    velocidad_gravedad = nueva_velocidad
    if nueva_velocidad == v_facil: level = 1
    if nueva_velocidad == v_intermedia: 
        pygame.mixer.music.load('./audio/music/tetris-ost-intermedio.mp3')
        pygame.mixer.music.play(-1)
        level = 2
    if nueva_velocidad == v_dificil: 
        pygame.mixer.music.load('./audio/music/tetris-ost-dificil.mp3')
        pygame.mixer.music.play(-1)
        level = 3
    if nueva_velocidad == v_extrema: 
        pygame.mixer.music.load('./audio/music/tetris-ost-extremo.mp3')
        pygame.mixer.music.play(-1)
        level = 4

    actualizar_info(score, level, lines)
    
def actualizar_info(score, level, lines):
    global score_text
    global level_text
    global lines_text
    info_surf.fill('black')

    score_text = font.render('Score: %s'%str(score), True, ('white'))
    level_text = font.render('Level: %s'%str(level), True, ('white'))
    lines_text = font.render('Lines: %s'%str(lines), True, ('white'))
    info_surf.blit(score_text, (80, 180))
    info_surf.blit(level_text, (80, 210))
    info_surf.blit(lines_text, (80, 240))

def pieza_aleatoria():
    global bolsa_piezas
    if bolsa_piezas == []: bolsa_piezas = [I,O,S,J,L,Z,T]
    pieza_aleatoria = random.choice(bolsa_piezas)
    bolsa_piezas.remove(pieza_aleatoria)
    return pieza_aleatoria

def generar_pieza():
    global pieza
    global sig_pieza 
    global sig_pieza_color_surf 

    if sig_pieza:
        pieza = sig_pieza
        generar_pieza_rect()
        sig_pieza = pieza_aleatoria()[0]
        sig_pieza_color_surf = get_color_pieza(sig_pieza)
        generar_sig_pieza_rect()
    else:
        sig_pieza = pieza_aleatoria()[0]
        sig_pieza_color_surf = get_color_pieza(sig_pieza)
        generar_sig_pieza_rect()
        pieza = pieza_aleatoria()[0]
        generar_pieza_rect()

def generar_pieza_guardada(pieza_guardada):
    global pieza 
    pieza = pieza_guardada
    generar_pieza_rect()

def generar_pieza_rect():
    global piezas_rect
    global game_over
    piezas_rect = []
    for f in range(pieza.__len__()):
        if f == 0: y_coord = 0
        else: y_coord = f * 36
        for c in range(pieza[f].__len__()):
            if c == 0: x_coord = 144
            else: x_coord = 144 + (c * 36)
            if pieza[f][c] == 1: 
                piezas_rect.append(I_surf.get_rect(topleft = (x_coord, y_coord)))
    for i in piezas_rect:
        for j in piezas_bloqueadas:
            if(i.colliderect(j)):
                game_over = True

def generar_pieza_guardada_rect(pieza_guardada):
    global piezas_guardadas_rect
    global game_over
    piezas_guardadas_rect = []
    for f in range(pieza_guardada.__len__()):
        if f == 0: y_coord = 500
        else: y_coord = 500 + (f * 36)
        for c in range(pieza_guardada[f].__len__()):
            if c == 0: x_coord = 100
            else: x_coord = 100 + (c * 36)
            if pieza_guardada[f][c] == 1: 
                piezas_guardadas_rect.append(I_surf.get_rect(topleft = (x_coord, y_coord)))

def generar_sig_pieza_rect():
    global sig_piezas_rect   
    sig_piezas_rect = [] 
    for f in range(sig_pieza.__len__()):
        if f == 0: y_coord = 320
        else: y_coord = 320 + (f * 36)
        for c in range(sig_pieza[f].__len__()):
            if c == 0: x_coord = 100
            else: x_coord = 100 + (c * 36)
            if sig_pieza[f][c] == 1: 
                sig_piezas_rect.append(I_surf.get_rect(topleft = (x_coord, y_coord)))

def actualizar_pieza_rect():
    global piezas_rect
    top = piezas_rect[0].top
    left = piezas_rect[0].left
    piezas_rect = []
    for f in range(pieza.__len__()):
            if f == 0: y_coord = top
            else: y_coord = top + (f * 36)
            for c in range(pieza[f].__len__()):
                if c == 0: x_coord = left 
                else: x_coord = left + (c * 36)
                if pieza[f][c] == 1: 
                    piezas_rect.append(I_surf.get_rect(topleft = (x_coord, y_coord)))
    
    for i in range(piezas_rect.__len__()):
        if piezas_rect[i].right > 359: 
            for i2 in range(piezas_rect.__len__()):
                piezas_rect[i2].right -= 36

    for i in range(piezas_rect.__len__()):
        if piezas_rect[i].left < 0: 
            for i2 in range(piezas_rect.__len__()):
                piezas_rect[i2].left += 36

def get_pieza():
    for i in range(I.__len__()):
        if pieza == I[i]: return(I)
    for i in range(O.__len__()):
        if pieza == O[i]: return(O)
    for i in range(S.__len__()):    
        if pieza == S[i]: return(S)
    for i in range(J.__len__()):
        if pieza == J[i]: return(J)
    for i in range(L.__len__()):    
        if pieza == L[i]: return(L)
    for i in range(Z.__len__()):
        if pieza == Z[i]: return(Z)
    for i in range(T.__len__()):
        if pieza == T[i]: return(T)

def get_color_pieza(pieza):
    for i in range(I.__len__()):
        if pieza == I[i]: return(I_surf)
    for i in range(O.__len__()):
        if pieza == O[i]: return(O_surf)
    for i in range(S.__len__()):    
        if pieza == S[i]: return(S_surf)
    for i in range(J.__len__()):
        if pieza == J[i]: return(J_surf)
    for i in range(L.__len__()):    
        if pieza == L[i]: return(L_surf)
    for i in range(Z.__len__()):
        if pieza == Z[i]: return(Z_surf)
    for i in range(T.__len__()):
        if pieza == T[i]: return(T_surf)

def girar_pieza():
    global pieza
    pieza_activa = get_pieza()
    giros = pieza_activa.__len__()
    for i in range(giros):
        if pieza == pieza_activa[i]: giro_actual = i
    if giro_actual + 1 < giros:
        pieza = pieza_activa[giro_actual + 1]
    else: pieza = pieza_activa[0]
    actualizar_pieza_rect()

def bloquear_pieza():
    for f in range(piezas_rect.__len__()):
        piezas_bloqueadas.append(piezas_rect[f])
        x_coord = piezas_rect[f].x
        y_coord = piezas_rect[f].y
        x_pos = int(x_coord/36)
        y_pos = int(y_coord/36)
        matriz_fondo[y_pos][x_pos] = pieza_color_surf
    generar_pieza()

def guardar_pieza():
    global piezas_guardadas_color_surf
    global piezas_guardadas
    global piezas_rect
    if piezas_guardadas:
        pieza_temp = get_pieza()[0]
        generar_pieza_guardada(piezas_guardadas)
        piezas_guardadas = pieza_temp
        generar_pieza_guardada_rect(piezas_guardadas)
        piezas_guardadas_color_surf = get_color_pieza(piezas_guardadas)
    else:
        piezas_guardadas = get_pieza()[0]
        generar_pieza_guardada_rect(piezas_guardadas)
        piezas_guardadas_color_surf = get_color_pieza(piezas_guardadas)
        generar_pieza()

def checar_filas():
    for f in range(matriz_fondo.__len__()):
        colores = []
        for c in range(matriz_fondo[f].__len__()):
            colores.append(matriz_fondo[f][c].get_at((15,15))[:3])
        fila_llena = all(surf != (0,0,0) for surf in colores)
        if fila_llena: 
            filas_llenas.append(f)
            #print('Fila ', [f+1], ' llena')
        colores = []

    if filas_llenas: eliminar_fila()

def eliminar_fila():
    global piezas_bloqueadas
    global filas_llenas
    global score_text
    global level_text
    global lines_text
    global score
    global lines

    # Ciclo que por casa filla llena va a recorrer la 'matriz_fondo', pintando de negro las que esten 
    # en la fila llena y recorriendo 'piezas_bloqueadas', eliminando las que esten en la fila llena
    for i in range(filas_llenas.__len__()):
        for f in range(matriz_fondo.__len__()):
            for c in range(matriz_fondo[f].__len__()):
                fila_coords = f * 36
                if f == filas_llenas[i]:
                    # Pinta de negro las superficies de la fila eliminada
                    matriz_fondo[f][c] = pygame.Surface((35,35))
                    matriz_fondo[f][c].fill('black')
                    # Elimina los rectangulos en la fila eliminada de 'pieza_bloqueadas'
                    piezas_bloqueadas = [j for j in piezas_bloqueadas if j.top != fila_coords]
                    
    # Ciclo que por cada fila llena recorre 'matriz_fondo' de abajo para arriba, pintando hacia abajo 
    # las superficies y rectangulos que esten por encima de la fila llena 
    for i in range(filas_llenas.__len__()):
        for f in range(matriz_fondo.__len__(), 1, -1):
                fila_coords = f * 36
                if f == filas_llenas[i]:
                    # Baja los rectangulos arriba de la fila eliminada
                    for j in piezas_bloqueadas:
                        if j.top < fila_coords:
                            j.top += 36
                if f <= filas_llenas[i]:
                    for c in range(matriz_fondo[f].__len__(),):
                        matriz_fondo[f][c] = matriz_fondo[f-1][c]
                
    # Ciclo que suma los puntos y las lineas eliminadas
    for i in range(filas_llenas.__len__()):
        score += 100
        lines += 1

    pygame.mixer.Sound.play(line_clear)
    actualizar_info(score, level, lines)
    filas_llenas = []

# SE GENERA LA PIEZA INICIAL ANTES DE COMENZAR EL JUEGO
generar_pieza()
    
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN:
                touching_borders = False
                collision = False
                # Ciclo que valida si la pieza actual esta tocando los bordes
                for f in range(piezas_rect.__len__()):
                    if piezas_rect[f].bottom == 647: 
                        touching_borders = True

                # Ciclo que valida si hay una colision entre la pieza actual y las piezas bloqueadas
                for f in range(piezas_rect.__len__()):
                    for e in range(piezas_bloqueadas.__len__()):
                        if piezas_rect[f].colliderect(piezas_bloqueadas[e]): 
                            collision = True

                if not touching_borders and not collision:
                    for f in range(piezas_rect.__len__()):
                        piezas_rect[f].bottom += 36
                        aumentar_velocidad = True

                if collision:
                    for f2 in range(piezas_rect.__len__()):
                                piezas_rect[f2].bottom -= 36

            if event.key == pygame.K_RIGHT:
                touching_borders = False
                for f in range(piezas_rect.__len__()):
                    if piezas_rect[f].right == 359: touching_borders = True

                if not touching_borders:
                    for f in range(piezas_rect.__len__()):
                        piezas_rect[f].right += 36

                for f in range(piezas_rect.__len__()):
                    for e in range(piezas_bloqueadas.__len__()):
                        if piezas_rect[f].colliderect(piezas_bloqueadas[e]): 
                            for f2 in range(piezas_rect.__len__()):
                                piezas_rect[f2].right -= 36

            if event.key == pygame.K_LEFT:
                touching_borders = False
                for f in range(piezas_rect.__len__()):
                        if piezas_rect[f].left == 0: touching_borders = True 
                            
                if not touching_borders:
                    for f in range(piezas_rect.__len__()):
                        piezas_rect[f].left -= 36

                for f in range(piezas_rect.__len__()):
                    for e in range(piezas_bloqueadas.__len__()):
                        if piezas_rect[f].colliderect(piezas_bloqueadas[e]): 
                            for f2 in range(piezas_rect.__len__()):
                                piezas_rect[f2].left += 36

            if event.key == pygame.K_UP:
                girar_pieza()

            if event.key == pygame.K_c:
                guardar_pieza()
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                aumentar_velocidad = False

    # REVISA SI LA PIEZA TOCA EL FINAL Y LA BLOQUEA
    for f in range(piezas_rect.__len__()):
        if piezas_rect[f].bottom > 647: 
            for f2 in range(piezas_rect.__len__()):
                piezas_rect[f2].bottom -= 36
            bloquear_pieza()

    # SE APLICA LA LOGICA DE LA GRAVEDAD
    gravedad += 1
    if gravedad == FPS * 77 and gravedad < FPS * 147: cambiar_dificultad(v_intermedia)
    if gravedad == FPS * 147 and gravedad < FPS * 211: cambiar_dificultad(v_dificil)
    if gravedad == FPS * 211: nueva_velocidad = cambiar_dificultad(v_extrema)

    if aumentar_velocidad and velocidad_default > 5: velocidad_default -= 1
    if not aumentar_velocidad: 
        velocidad_default = velocidad_gravedad
        
    if gravedad % velocidad_default == 0:
        for f in range(piezas_rect.__len__()):
            piezas_rect[f].bottom += 36

    # REVISA SI HAY PIEZAS BLOQUEADAS Y SI HUBO UNA COLISION DE LA PIEZA ACTUAL CON LAS BLOQUEADAS
    if piezas_bloqueadas:
        for f in range(piezas_rect.__len__()):
            for e in range(piezas_bloqueadas.__len__()):
                if piezas_rect[f].colliderect(piezas_bloqueadas[e]): 
                    for f2 in range(piezas_rect.__len__()):
                        piezas_rect[f2].top -= 36
                    bloquear_pieza()                    

    checar_filas()

    pieza_color_surf = get_color_pieza(pieza)

    screen.blit(game_surf, (0,0))
    
    # COLOCA LOS 'RECTANGLES' DE LAS PIEZAS BLOQUEADAS EN LA PANTALLA
    for i in range(piezas_bloqueadas.__len__()):
        game_surf.blit(pieza_color_surf, piezas_bloqueadas[i])

    # COLOCA EL FONDO EN LA PANTALLA
    for f in range(matriz_fondo.__len__()):
        if f == 0: y_coord = 0
        else: y_coord = f * 36
        for c in range(matriz_fondo[f].__len__()):
            if c == 0: x_coord = 0 
            else: x_coord = c * 36
            game_surf.blit(matriz_fondo[f][c], (x_coord, y_coord))

    # COLOCA LA PIEZA ACTIVA EN LA PANTALLA
    for f in range(piezas_rect.__len__()):
        game_surf.blit(pieza_color_surf, piezas_rect[f])

    # COLOCA EL AREA DE INFORMACION A LA DERECHA DEL AREA DE JUEGO
    screen.blit(info_surf, (360,0))
    info_surf.blit(logo_surf, (20,20))
    info_surf.blit(score_text, (80, 180))
    info_surf.blit(level_text, (80, 210))
    info_surf.blit(lines_text, (80, 240))
    info_surf.blit(next_text, (65, 280))
    info_surf.blit(next_surf, (65, 320))
    info_surf.blit(hold_text, (65, 470))
    info_surf.blit(hold_surf, (65, 500))

    # COLOCA LA SIGUIENTE PIEZA EN LA PANTALLA
    for p in sig_piezas_rect:
        info_surf.blit(sig_pieza_color_surf, p)

    # COLOCA LA PIEZA GUARDADA EN LA PANTALLA
    for p in piezas_guardadas_rect:
        info_surf.blit(piezas_guardadas_color_surf, p)

    pygame.display.flip()
    clock.tick(FPS)

print('Tu puntuacion final fue: %s'%str(score))