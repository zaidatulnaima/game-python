import pygame
from pygame.locals import *
from OpenGL.GL import *

# Inisialisasi Pygame
pygame.init()

# Dimensi jendela
window_width = 600
window_height = 600

# Inisialisasi jendela Pygame
pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
glOrtho(0, window_width, window_height, 0, -1, 1)

# Posisi persimpangan garis kotak persegi
# Posisi persimpangan garis untuk papan Bagchal ukuran 5x5
intersection_points = [(100 * i, 100 * j) for i in range(1, 6) for j in range(1, 6)]

# Indeks pemain yang sedang bermain (0 atau 1)
current_player = 0

# Array untuk menyimpan posisi bidak masing-masing pemain
player_positions = [[], []]

# Fungsi untuk menggambar papan Bagchal
def draw_board():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLineWidth(2)

    # Garis-garis yang membentuk kotak persegi panjang
    glBegin(GL_LINES)
    for i in range(1, 6):
        # Garis-garis horizontal
        glVertex2f(100, 100 * i)
        glVertex2f(500, 100 * i)

        # Garis-garis miring
        glVertex2f(100, 500)
        glVertex2f(500, 100)
        
        # Garis-garis miring
        glVertex2f(300, 500)
        glVertex2f(500, 300)
        
        # Garis-garis miring
        glVertex2f(100, 300)
        glVertex2f(300, 100)
        
        # Garis-garis miring
        glVertex2f(100, 100)
        glVertex2f(500, 500)
        
        # Garis-garis miring
        glVertex2f(100, 300)
        glVertex2f(300, 500)
        
        # Garis-garis miring
        glVertex2f(300, 100)
        glVertex2f(500, 300)
        
        # Garis-garis vertikal
        glVertex2f(100 * i, 100)
        glVertex2f(100 * i, 500)
    glEnd()

    # Titik-titik di persimpangan garis
    glPointSize(10)
    glBegin(GL_POINTS)
    for point in intersection_points:
        glVertex2fv(point)
    glEnd()

#     # Gambar bidak pemain
    glPointSize(20)
    glBegin(GL_POINTS)
    for i in range(2):
        glColor3f(1.0, 0.0, 0.0) if i == 0 else glColor3f(0.0, 0.0, 1.0)
        for pos in player_positions[i]:
            glVertex2fv(pos)
    glEnd()

    # Gambar tombol reset
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex2f(520, 520)
    glVertex2f(580, 520)
    glVertex2f(580, 580)
    glVertex2f(520, 580)
    glEnd()

    # Tampilkan tulisan "Reset"
    font = pygame.font.Font(None, 24)
    text = font.render("Reset", True, (0, 0, 0))
    text_rect = text.get_rect(center=(550, 550))
    pygame.display.get_surface().blit(text, text_rect)

    pygame.display.flip()

# Fungsi untuk mengecek apakah suatu posisi sudah diisi oleh pemain tertentu
def is_position_occupied(position):
    return position in player_positions[0] or position in player_positions[1]

# Fungsi untuk menentukan pemenang
def check_winner():
    for i in range(2):
        for win_condition in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
            if all(position in player_positions[i] for position in win_condition):
                return i
    return None

# Fungsi untuk menampilkan pesan kemenangan
def display_winner_message(winning_player):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Selamat, Pemain {winning_player + 1} berhasil!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
    pygame.display.get_surface().blit(text, text_rect)
    pygame.display.flip()

# Main loop
while True:
    game_won = False  # Menandai apakah permainan telah dimenangkan

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Jika klik di persimpangan garis kotak
            nearest_point = min(intersection_points, key=lambda point: ((point[0] - x) ** 2 + (point[1] - y) ** 2))
            if not is_position_occupied(nearest_point) and not game_won:
                player_positions[current_player].append(nearest_point)
                winner = check_winner()
                if winner is not None:
                    display_winner_message(winner)  # Menampilkan pesan kemenangan
                    game_won = True
                current_player = 1 - current_player  # Ganti giliran pemain

    draw_board()