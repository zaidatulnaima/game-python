import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import subprocess
import math
import sys

pygame.init()

# Inisialisasi Pygame
window_width, window_height = 600, 600

font_path = "assets/font3.otf"

def draw_text(text, font, color, x, y, centered=True):
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_width(), text_surface.get_height()

    glRasterPos2f(x - width / 2, y + height / 2)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x - width / 2, y + height / 2)
    glTexCoord2f(1, 0)
    glVertex2f(x + width / 2, y + height / 2)
    glTexCoord2f(1, 1)
    glVertex2f(x + width / 2, y - height / 2)
    glTexCoord2f(0, 1)
    glVertex2f(x - width / 2, y - height / 2)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)

def draw_button(pos, text, font, base_color, text_color=(0, 0, 0), depth=0.1, corner_radius=10):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    x, y, width, height = pos
    segments = 30  # Number of segments for the circle approximation

    # Check if mouse is inside the button
    is_inside = x < mouse[0] < x + width and y < mouse[1] < y + height

    glBegin(GL_QUADS)

    # Front face
    glColor3fv(base_color)  # Change color when mouse is inside
    glVertex3f(x + corner_radius, y, depth)
    glVertex3f(x + width - corner_radius, y, depth)
    glVertex3f(x + width, y + corner_radius, depth)
    glVertex3f(x + width, y + height - corner_radius, depth)
    glVertex3f(x + width - corner_radius, y + height, depth)
    glVertex3f(x + corner_radius, y + height, depth)
    glVertex3f(x, y + height - corner_radius, depth)
    glVertex3f(x, y + corner_radius, depth)

    # Back face
    for i in range(segments):
        angle1 = math.radians((i / segments) * 90)
        angle2 = math.radians(((i + 1) / segments) * 90)

        glVertex3f(x + corner_radius * math.cos(angle1), y + corner_radius * math.sin(angle1), -depth)
        glVertex3f(x + corner_radius * math.cos(angle2), y + corner_radius * math.sin(angle2), -depth)
        glVertex3f(x + width - corner_radius * math.cos(angle2), y + height - corner_radius * math.sin(angle2), -depth)
        glVertex3f(x + width - corner_radius * math.cos(angle1), y + height - corner_radius * math.sin(angle1), -depth)

    # Connecting side faces
    for i in range(segments):
        angle1 = math.radians((i / segments) * 90)
        angle2 = math.radians(((i + 1) / segments) * 90)

        glVertex3f(x + corner_radius * math.cos(angle1), y + corner_radius * math.sin(angle1), depth)
        glVertex3f(x + corner_radius * math.cos(angle2), y + corner_radius * math.sin(angle2), depth)
        glVertex3f(x + width - corner_radius * math.cos(angle2), y + height - corner_radius * math.sin(angle2), depth)
        glVertex3f(x + width - corner_radius * math.cos(angle1), y + height - corner_radius * math.sin(angle1), depth)

    glEnd()

    draw_text(text, font, text_color, x + width / 2, y + height / 2, centered=True)

    return is_inside and click[0] == 1  # Return True only when mouse is inside and left button is clicked

def play():
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Keluar dari program

        # Kondisi jika tombol "PLAY" diklik
        if draw_button((window_width / 2 - 100, 500, 200, 50), "PLAY", pygame.font.Font(font_path, 30), (215, 252, 212), text_color=(0, 0, 0)):
            subprocess.run([sys.executable, "point.py"])  # Jalankan winner.py menggunakan subproses

        pygame.display.flip()
        pygame.time.Clock().tick(30)

screen = pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
glOrtho(0, window_width, window_height, 0, -1, 1)

bg_texture = pygame.image.load("assets/bg_hutan.jpg")
bg_texture_data = pygame.image.tostring(bg_texture, "RGB", 1)

# Membuat latar belakang OpenGL
bg = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, bg)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, bg_texture.get_width(), bg_texture.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, bg_texture_data)

# Generate and bind textures for text rendering
text_texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, text_texture)

# Font initialization
pygame.font.init()
font = pygame.font.Font(font_path, 36)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        
        glBindTexture(GL_TEXTURE_2D, bg)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)  # Invert y-axis coordinate
        glVertex2f(0, 0)
        glTexCoord2f(1, 1)  # Invert y-axis coordinate
        glVertex2f(window_width, 0)
        glTexCoord2f(1, 0)  # Invert y-axis coordinate
        glVertex2f(window_width, window_height)
        glTexCoord2f(0, 0)  # Invert y-axis coordinate
        glVertex2f(0, window_height)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        if draw_button((window_width / 2 - 93, 500, 200, 50), "PLAY", pygame.font.Font(font_path, 30), (139, 69, 19), text_color=(0, 0, 0)):
            play()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
