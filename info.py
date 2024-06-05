import pygame
from pygame.locals import *
from OpenGL.GL import *
import pygame.font
import subprocess

pygame.init()

window_width = 800
window_height = 600

# Inisialisasi Pygame
pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
glOrtho(0, window_width, window_height, 0, -1, 1)

victory_font_path = "assets/font3.otf"
victory_font_size = 72
victory_font = pygame.font.Font(victory_font_path, victory_font_size)
victory_text = ""

font_size = 36
font = pygame.font.Font(victory_font_path, font_size)

intersection_points = [(100 * i, 100 * j) for i in range(1, 6) for j in range(1, 6)]

current_player = 1
tiger_positions = [[(100, 500), (500, 100), (500, 500), (100, 100)], []]
goat_positions = [[], []]

selected_tiger = None
x, y = 0, 0

texture_id = glGenTextures(1)

def display_text(text, color, position):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    pygame.display.get_surface().blit(text_surface, text_rect)
    pygame.display.flip()

def load_texture(texture_path, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    texture_surface = pygame.image.load(texture_path)
    texture_width, texture_height = texture_surface.get_width(), texture_surface.get_height()
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_width, texture_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

# Usage example:
wood_texture_id = glGenTextures(1)
singa_texture_id = glGenTextures(1)
kambing_texture_id = glGenTextures(1)

load_texture("assets/wood.jpg", wood_texture_id)
load_texture("assets/HARI_bg.png", singa_texture_id)
load_texture("assets/GOAT_bg.png", kambing_texture_id)

# Variables for scoring
tiger_score = 0
goat_score = 0

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    light_position = (window_width / 2.0, window_height / 8.0, 100.0, 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # Set up additional properties for diffuse lighting
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 0.0, 0.0, 1.0))  # Diffuse color (white)
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))  # Specular color (white)
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))  # Specular material color (white)
    glMaterialfv(GL_FRONT, GL_SHININESS, 50.0)  # Shininess factor


def draw_lines_with_lighting():
    # Set up lighting
    setup_lighting()

    # Draw lines with lighting
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 1.0)  # Set the color of the lines (white)

    for i in range(1, 6):
        glVertex3f(100, 100 * i, 0.0)  # Specify the Z-coordinate as 0.0
        glVertex3f(500, 100 * i, 0.0)

        glVertex3f(100 * i, 100, 0.0)
        glVertex3f(100 * i, 500, 0.0)

    glVertex3f(100, 500, 0.0)
    glVertex3f(500, 100, 0.0)

    glVertex3f(300, 500, 0.0)
    glVertex3f(500, 300, 0.0)

    glVertex3f(100, 300, 0.0)
    glVertex3f(300, 100, 0.0)

    glVertex3f(100, 100, 0.0)
    glVertex3f(500, 500, 0.0)

    glVertex3f(100, 300, 0.0)
    glVertex3f(300, 500, 0.0)

    glVertex3f(300, 100, 0.0)
    glVertex3f(500, 300, 0.0)

    glEnd()

    # Disable lighting after drawing
    glDisable(GL_LIGHTING)

# Load MP3 file
pygame.mixer.init()
# pygame.mixer.music.load("assets/musik1.mp3")

# Variables for MP3 playback control
is_playing = False
play_music_flag = False

def play_music():
    pygame.mixer.music.play(-1)

def draw_board():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLineWidth(6)
    glClearColor(1.0, 0.96, 0.85, 1.0)

    glEnable(GL_TEXTURE_2D)

    # Draw the board with wood texture
    glBindTexture(GL_TEXTURE_2D, wood_texture_id)
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    glTexCoord2f(0, 1)
    glVertex2f(100, 500)
    glTexCoord2f(1, 1)
    glVertex2f(500, 500)
    glTexCoord2f(1, 0)
    glVertex2f(500, 100)
    glTexCoord2f(0, 0)
    glVertex2f(100, 100)
    glEnd()

    # Draw the lines
    draw_lines()

    # Draw the intersection points
    glPointSize(20)
    glBegin(GL_POINTS)
    for point in intersection_points:
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(point[0], point[1], 0.0)
    glEnd()

    # Draw tigers and goats with tiger texture
    glBindTexture(GL_TEXTURE_2D, singa_texture_id)
    draw_tigers_and_goats()

    pygame.display.flip()
    glDisable(GL_TEXTURE_2D)

def draw_lines():
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)
    for i in range(1, 6):
        glVertex2f(100, 100 * i)
        glVertex2f(500, 100 * i)

        glVertex2f(100 * i, 100)
        glVertex2f(100 * i, 500)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(100, 500)
    glVertex2f(500, 100)

    glVertex2f(300, 500)
    glVertex2f(500, 300)

    glVertex2f(100, 300)
    glVertex2f(300, 100)

    glVertex2f(100, 100)
    glVertex2f(500, 500)

    glVertex2f(100, 300)
    glVertex2f(300, 500)

    glVertex2f(300, 100)
    glVertex2f(500, 300)
    glEnd()

def draw_tigers_and_goats():
    glEnable(GL_TEXTURE_2D)

    glPointSize(20)
    glBegin(GL_POINTS)
    for point in intersection_points:
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(point[0], point[1], 0.0)
    glEnd()

    draw_tigers(tiger_positions[0])
    draw_goats(goat_positions[1])

    if current_player == 1 and len(goat_positions[0]) + len(goat_positions[1]) < 20:
        nearest_point = min(
            intersection_points,
            key=lambda point: ((point[0] - x) ** 2 + (point[1] - y) ** 2),
        )
        if can_move(nearest_point):
            draw_selected_goat(nearest_point)

    glDisable(GL_TEXTURE_2D)
    
def draw_tigers(positions):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, singa_texture_id)
    glBegin(GL_QUADS)
    for pos in positions:
        offset_x = 40  # Perbesar ukuran harimau
        offset_y = 40

        glColor4f(1.0, 1.0, 1.0, 1.0)  # Gunakan glColor4f untuk menetapkan alpha
        glTexCoord2f(0, 1)
        glVertex2f(pos[0] - offset_x, pos[1] - offset_y)
        glTexCoord2f(1, 1)
        glVertex2f(pos[0] + offset_x, pos[1] - offset_y)
        glTexCoord2f(1, 0)
        glVertex2f(pos[0] + offset_x, pos[1] + offset_y)
        glTexCoord2f(0, 0)
        glVertex2f(pos[0] - offset_x, pos[1] + offset_y)
    glEnd()
    glDisable(GL_BLEND)  # Matikan blending setelah selesai menggambar

def draw_goats(positions):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, kambing_texture_id)
    glBegin(GL_QUADS)
    for pos in positions:
        offset_x = 40  # Perbesar ukuran kambing
        offset_y = 40

        glColor4f(1.0, 1.0, 1.0, 1.0)  # Gunakan glColor4f untuk menetapkan alpha
        glTexCoord2f(0, 1)
        glVertex2f(pos[0] - offset_x, pos[1] - offset_y)
        glTexCoord2f(1, 1)
        glVertex2f(pos[0] + offset_x, pos[1] - offset_y)
        glTexCoord2f(1, 0)
        glVertex2f(pos[0] + offset_x, pos[1] + offset_y)
        glTexCoord2f(0, 0)
        glVertex2f(pos[0] - offset_x, pos[1] + offset_y)
    glEnd()
    glDisable(GL_BLEND)  # Matikan blending setelah selesai menggambar

def draw_selected_goat(position):
    glBindTexture(GL_TEXTURE_2D, kambing_texture_id)  # Use tiger texture temporarily
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2fv(position)
    glEnd()

def is_position_occupied(position):
    return (
        position in tiger_positions[0]
        or position in tiger_positions[1]
        or position in goat_positions[0]
        or position in goat_positions[1]
    )

def get_neighbors(position):
    x, y = position
    return [
        (x + 100, y),  # Posisi sebelah kanan
        (x - 100, y),  # Posisi sebelah kiri
        (x, y + 100),  # Posisi di bawah
        (x, y - 100),  # Posisi di atas
        (x + 100, y + 100),  # Posisi diagonal kanan bawah
        (x - 100, y - 100),  # Posisi diagonal kiri atas
        (x + 100, y - 100),  # Posisi diagonal kanan atas
        (x - 100, y + 100),  # Posisi diagonal kiri bawah
    ]

def can_move(position):
    x, y = position

    # Pengecekan ketersambungan dengan garis pada intersection_points
    connected_to_intersection = any(
        are_connected(position, intersection_point) for intersection_point in intersection_points
    )

    # Pengecekan bahwa posisi yang akan dipilih berdekatan (3 titik terdekat)
    neighbors = get_neighbors(position)
    valid_neighbor = any(
        are_connected(position, neighbor) and not is_position_occupied(neighbor)
        and abs(neighbor[0] - x) <= 100 and abs(neighbor[1] - y) <= 100
        for neighbor in neighbors
    )

    # Pengecekan apakah posisi yang dipilih sudah terisi oleh harimau atau kambing
    position_occupied = is_position_occupied(position)

    # Pengecekan jika harimau ingin memangsa kambing, maka bisa berpindah dengan jarak 200 unit
    if (
        100 <= x <= 500 and 100 <= y <= 500 and not position_occupied
        and connected_to_intersection and valid_neighbor
        and current_player == 0  # Hanya berlaku untuk harimau
    ):
        return True
    elif (
        100 <= x <= 500 and 100 <= y <= 500 and not position_occupied
        and connected_to_intersection and valid_neighbor
    ):
        return True

    return False

def get_neighbors(position):
    x, y = position
    return [
        (x - 100, y),
        (x + 100, y),
        (x, y - 100),
        (x, y + 100),
    ]

def are_connected(position1, position2):
    return (
        abs(position1[0] - position2[0]) == 100 and abs(position1[1] - position2[1]) == 0
        or abs(position1[0] - position2[0]) == 0 and abs(position1[1] - position2[1]) == 100
        or abs(position1[0] - position2[0]) == 100 and abs(position1[1] - position2[1]) == 100
    )

def are_on_same_line(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    return (y2 - y1) * (x3 - x2) == (y3 - y2) * (x2 - x1)

def check_victory():
    global tiger_score, goat_score

    # Check for tiger victory
    if tiger_score >= 2:
        return "Tigers"

    # Check for goat victory
    if len(goat_positions[0]) + len(goat_positions[1]) == 16:
        return "Goats"

    # Check for goat victory if tigers cannot move
    if current_player == 0:
        for tiger_pos in tiger_positions[0] + tiger_positions[1]:
            for neighbor in get_neighbors(tiger_pos):
                if can_move(neighbor):
                    return None  # Tigers can still move, continue the game

        return "Goats"  # Tigers cannot move, goats win

    return None

def draw_victory_text(winner):
    glDisable(GL_TEXTURE_2D)  # Disable texture for displaying text
    text = f"{winner} is the winner!"
    
    # Set up orthographic projection for 2D rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window_width, window_height, 0, -1, 1)  # Use glOrtho instead
    
    # Set up modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text in the center of the screen
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2))
    pygame.display.get_surface().blit(text_surface, text_rect)
    pygame.display.flip()
    
    # Restore the previous projection matrix
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    
    # Restore the previous modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
def main():
    global current_player, x, y, selected_tiger, is_playing, play_music_flag, tiger_score, goat_score
    
    tiger_score = 0  # Initialize tiger_score
    game_over = False 
    winner_status = None
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True 
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                nearest_point = min(
                    intersection_points,
                    key=lambda point: ((point[0] - x) ** 2 + (point[1] - y) ** 2),
                )

                if current_player == 0:
                    if nearest_point in tiger_positions[0]:
                        selected_tiger = nearest_point
                    elif selected_tiger and can_move(nearest_point):
                        # Pindahkan harimau ke titik tujuan jika valid
                        captured_goat = None
                        for goat_pos in goat_positions[0] + goat_positions[1]:
                            if are_connected(selected_tiger, goat_pos) and are_on_same_line(selected_tiger, goat_pos, nearest_point):
                                captured_goat = goat_pos
                                break

                        if captured_goat:
                            tiger_score += 1

                            # Remove captured goat from the board
                            if captured_goat in goat_positions[0]:
                                goat_positions[0].remove(captured_goat)
                            elif captured_goat in goat_positions[1]:
                                goat_positions[1].remove(captured_goat)

                        # Pindahkan harimau
                        tiger_positions[0].remove(selected_tiger)
                        tiger_positions[0].append(nearest_point)
                        selected_tiger = None
                        current_player = 1

                elif current_player == 1:
                    if len(goat_positions[0]) + len(goat_positions[1]) < 20 and can_move(nearest_point):
                        # Posisi kambing yang akan dipindahkan
                        goat_to_move = nearest_point

                        # Cek apakah ada harimau yang dapat memangsa kambing
                        captured_by_tiger = None
                        for tiger_pos in tiger_positions[0] + tiger_positions[1]:
                            if are_connected(tiger_pos, goat_to_move) and are_on_same_line(tiger_pos, goat_to_move, nearest_point):
                                captured_by_tiger = tiger_pos
                                break

                        if captured_by_tiger:
                            # Hilangkan kambing dari papan
                            if goat_to_move in goat_positions[0]:
                                goat_positions[0].remove(goat_to_move)
                            elif goat_to_move in goat_positions[1]:
                                goat_positions[1].remove(goat_to_move)

                        # Pindahkan kambing
                        goat_positions[current_player].append(nearest_point)
                        current_player = 0

                # Inside your main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Trigger music playback here if needed
                pygame.mixer.music.play(-1)  # Play in a loop

        draw_board()
        
        # Check for victory
        winner = check_victory()
        winner = check_victory()                                                                                                    
        if winner:
            if winner == "Tigers":
                subprocess.run(["python", "t_winner.py"])  # Jalankan t_winner.py saat harimau menang
            elif winner == "Goats":
                subprocess.run(["python", "g_winner.py"])  # Jalankan g_winner.py saat kambing menang
            draw_victory_text(winner_status)
            draw_victory_text(winner)
            pygame.display.flip()
            
def wait_for_exit():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
                
def stop_music():
    pygame.mixer.music.stop()

if __name__ == "__main__":
    # play_music()  # Start playing the music when the game starts
    main()