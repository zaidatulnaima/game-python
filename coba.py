import pygame
from pygame.locals import *
from OpenGL.GL import *

pygame.init()

window_width = 600
window_height = 600

pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
glOrtho(0, window_width, window_height, 0, -1, 1)

intersection_points = [(100 * i, 100 * j) for i in range(1, 6) for j in range(1, 6)]

current_player = 1  # Ubah inisialisasi giliran pertama ke pemain kambing (1)

tiger_positions = [[(100, 500), (500, 100), (500, 500), (100, 100)], []]
goat_positions = [[], []]

x, y = 0, 0
selected_tiger = None  # Inisialisasi variabel selected_tiger

def draw_board():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLineWidth(5)

    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(1, 6):
        glVertex2f(100, 100 * i)
        glVertex2f(500, 100 * i)

        glVertex2f(100 * i, 100)
        glVertex2f(100 * i, 500)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
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

    glPointSize(20)
    glBegin(GL_POINTS)
    for point in intersection_points:
        glVertex3f(point[0], point[1], 0.0)
    glEnd()

    draw_tigers_and_goats()

    pygame.display.flip()

def draw_tigers_and_goats():
    glPointSize(20)
    glBegin(GL_POINTS)

    glColor3f(1.0, 0.0, 0.0)
    for pos in tiger_positions[0]:
        glVertex2fv(pos)

    glColor3f(0.5, 0.0, 0.0)
    if current_player == 0 and len(tiger_positions[0]) == 4:
        nearest_point = min(
            intersection_points,
            key=lambda point: ((point[0] - x) ** 2 + (point[1] - y) ** 2),
        )
        if can_move(nearest_point) and nearest_point not in tiger_positions[0]:
            glVertex2fv(nearest_point)

            # Tambahan kode: Jika titik terdekat dipilih, pindahkan harimau ke titik tersebut
            if can_move(nearest_point) and nearest_point not in tiger_positions[0]:
                tiger_positions[0] = [nearest_point]

    glColor3f(0.0, 0.0, 1.0)
    for pos in goat_positions[1]:
        glVertex2fv(pos)

    glColor3f(0.0, 0.0, 0.5)
    if current_player == 1 and len(goat_positions[0]) + len(goat_positions[1]) < 20:
        nearest_point = min(
            intersection_points,
            key=lambda point: ((point[0] - x) ** 2 + (point[1] - y) ** 2),
        )
        if can_move(nearest_point):
            glVertex2fv(nearest_point)

    glEnd()

def is_position_occupied(position):
    return (
        position in tiger_positions[0]
        or position in tiger_positions[1]
        or position in goat_positions[0]
        or position in goat_positions[1]
    )

def check_winner():
    if len(goat_positions[1 - current_player]) >= 5:
        return 1 - current_player
    elif not any(can_move(pos) for pos in goat_positions[current_player]):
        return current_player
    return None

def display_winner_message(winning_player):
    font = pygame.font.Font(None, 36)
    text = font.render(
        f"Selamat, Pemain {winning_player + 1} berhasil!", True, (255, 255, 255)
    )
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
    pygame.display.get_surface().blit(text, text_rect)
    pygame.display.flip()

def can_move(position):
    x, y = position

    # Pengecekan ketersambungan dengan garis pada intersection_points
    connected_to_intersection = any(
        are_connected(position, intersection_point) for intersection_point in intersection_points
    )

    # Pengecekan bahwa ada garis yang menghubungkan titik posisi
    valid_move = any(
        are_connected(position, destination) for destination in intersection_points
    )

    # Pengecekan apakah ada kambing dalam radius 100 unit dari titik awal harimau
    goats_nearby = any(
        abs(goat[0] - x) <= 100 and abs(goat[1] - y) <= 100
        for goat in goat_positions[0] + goat_positions[1]
    )

    if goats_nearby:
        # Jika ada kambing di dekat harimau, harimau hanya boleh bergerak 200 unit dari titik awal
        return 100 <= x <= 500 and 100 <= y <= 500 and not is_position_occupied(position) and connected_to_intersection and valid_move and (abs(x - 100) >= 200 or abs(x - 500) >= 200 or abs(y - 100) >= 200 or abs(y - 500) >= 200)
    else:
        # Jika tidak ada kambing di dekat harimau, harimau hanya boleh bergerak 100 unit dari titik awal
        goats_within_200_units = any(
            abs(goat[0] - x) <= 200 and abs(goat[1] - y) <= 200
            for goat in goat_positions[0] + goat_positions[1]
        )
        
        # Pengecekan apakah ada kambing di antara posisi awal harimau dan tujuan pindah harimau
        goat_in_path = any(
            are_on_same_line(selected_tiger, goat_pos, position)
            for goat_pos in goat_positions[0] + goat_positions[1]
        )

        return 100 <= x <= 500 and 100 <= y <= 500 and not is_position_occupied(position) and connected_to_intersection and valid_move and not goats_within_200_units and not goat_in_path

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

def main():
    global current_player, x, y, selected_tiger

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                nearest_point = min(
                    intersection_points,
                    key=lambda point: ((point[0] - x) ** 2 + (point[1] - y) ** 2),
                )

                if current_player == 0:
                    # Pilih harimau (merah) untuk dipindahkan
                    if nearest_point in tiger_positions[0]:
                        selected_tiger = nearest_point

                    # Pindahkan harimau ke titik tujuan jika valid
                    elif selected_tiger and can_move(nearest_point):
                        # Pengecekan apakah ada kambing yang dapat dimakan
                        captured_goat = None
                        for goat_pos in goat_positions[0] + goat_positions[1]:
                            if are_on_same_line(selected_tiger, goat_pos, nearest_point):
                                captured_goat = goat_pos
                                break

                        if captured_goat:
                            # Hilangkan kambing dari papan
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
                            # Perubahan pada bagian ini untuk memeriksa ketersambungan harimau dan kambing
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
                winner = check_winner()
                if winner is not None:
                    display_winner_message(winner)

        draw_board()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
