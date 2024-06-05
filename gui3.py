import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

pygame.init()

window_width, window_height = 1280, 720
font_path = "assets/font.ttf"

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

def draw_button(pos, text, font, base_color, text_color=(0, 0, 0)):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    x, y, width, height = pos

    glBegin(GL_QUADS)
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        glColor3fv(base_color)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)

        if click[0] == 1:
            glEnd()
            return True
    else:
        glColor3fv(base_color)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)

    glEnd()

    draw_text(text, font, text_color, x + width / 2, y + height / 2, centered=True)

    return False

def play():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if draw_button((window_width / 2 - 100, 250, 200, 50), "PLAY", pygame.font.Font(font_path, 20), (215, 252, 212), text_color=(0, 0, 0)):
            return

        if draw_button((window_width / 2 - 100, 460, 200, 50), "BACK", pygame.font.Font(font_path, 20), (255, 255, 255), (0, 255, 0), text_color=(0, 0, 0)):
            return

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def options():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if draw_button((window_width / 2 - 100, 250, 200, 50), "BACK", pygame.font.Font(font_path, 20), (255, 255, 255), (0, 255, 0), text_color=(0, 0, 0)):
            return

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_text("MAIN MENU", pygame.font.Font(font_path, 100), (182, 143, 64), window_width / 2, 100)

        if draw_button((window_width / 2 - 100, 250, 200, 50), "PLAY", pygame.font.Font(font_path, 20), (215, 252, 212), text_color=(0, 0, 0)):
            play()

        if draw_button((window_width / 2 - 100, 550, 200, 50), "QUIT", pygame.font.Font(font_path, 20), (215, 252, 212), text_color=(0, 0, 0)):
            pygame.quit()
            quit()

        pygame.display.flip()
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
    glOrtho(0, window_width, window_height, 0, -1, 1)

    main_menu()
