import pygame
import sys
from old_maze_creator import maze_generator, maze_from_image

# --- CONFIGURACIÓN DE LA MATRIZ ---
# He puesto una versión simplificada, luego incluir el maze real.
maze_simple = [
    [1, 1, 1],
    [1, 0, 0],
    [0, 0, 1]
    ]
maze = maze_from_image()

# --- CONFIGURACIÓN VISUAL ---
# Dimensiones de la cuadrícula
FILAS = 32
COLUMNAS = 32

# Tamaño de cada "píxel" o celda del laberinto en la pantalla
TAMANO_CELDA = 20 # 20x20 píxeles por celda

# Calcular dimensiones de la ventana automáticamente
ANCHO_PANTALLA = COLUMNAS * TAMANO_CELDA
ALTO_PANTALLA = FILAS * TAMANO_CELDA

# Colores (R, G, B)
COLOR_PARED = (0, 0, 0)      # Negro para el 1
COLOR_PASILLO = (255, 255, 255) # Blanco para el 0
COLOR_FONDO = (50, 50, 50)   # Gris oscuro para el borde de ventana

# --- DRAWING GRID ---
def drawing_grid(ventana, matriz, tamano_celda):
    """
    ventana: el objeto 'pantalla' de pygame
    matriz: tu lista de listas 'maze' (32x32)
    tamano_celda: píxeles de ancho/alto para cada cuadrado
    """
    for i in range(len(maze)):        # i = índice de fila (eje Y)
        for j in range(len(maze[0])): # j = índice de columna (eje X)
            
            # 1. Calcular coordenadas de pantalla
            x = j * tamano_celda
            y = i * tamano_celda
            
            # 2. Definir el color según el valor (1=Pared, 0=Pasillo)
            color = (0, 0, 0) if maze[i][j] == 1 else (255, 255, 255)
            
            # 3. Dibujar el cuadrado
            # Rect(x, y, ancho, alto)
            pygame.draw.rect(ventana, color, (x, y, tamano_celda, tamano_celda))
            
            # 4. Opcional: Dibujar una línea de rejilla gris muy fina
            pygame.draw.rect(ventana, (200, 200, 200), (x, y, tamano_celda, tamano_celda), 1)

# --- INICIALIZAR PYGAME ---
def main():
    # 1. Inicializar todos los módulos de Pygame
    pygame.init()

    # 2. Configurar las dimensiones de la ventana
    ANCHO, ALTO = 640, 640
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    
    # 3. Título de la ventana
    pygame.display.set_caption("Mi Ventana de Laberinto")

    # 4. Reloj para controlar los FPS (Frames Per Second)
    reloj = pygame.time.Clock()

    # 5. Bucle principal del juego
    ejecutando = True
    while ejecutando:
        # A. Gestión de eventos (Input)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # B. Lógica del programa (Update)
        # Aquí es donde más adelante procesarás tu BFS/A*

        # C. Renderizado (Draw)
        pantalla.fill(COLOR_FONDO)  # Color de fondo COLOR_FONDO (R, G, B)
        drawing_grid(pantalla, maze, 20)

        # Actualizar el contenido de la ventana
        pygame.display.flip()

        # Limitar a 60 FPS para no sobrecargar la CPU
        reloj.tick(60)

    # 6. Salida limpia
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()