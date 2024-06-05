import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import subprocess

pygame.init()

window_width, window_height = 800, 600
font_path = "assets/font2.ttf"

def draw_text(text, font, color, x, y, centered=True):
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_width(), text_surface.get_height()

    if centered:
        x -= width / 2

    glRasterPos2f(x, y + height / 2)

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
    glVertex2f(x, y + height / 2)
    glTexCoord2f(1, 0)
    glVertex2f(x + width, y + height / 2)
    glTexCoord2f(1, 1)
    glVertex2f(x + width, y - height / 2)
    glTexCoord2f(0, 1)
    glVertex2f(x, y - height / 2)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)

def draw_button(text, font, color, x, y, width, height, centered=True):
    # Draw a button with text
    glColor3fv(color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

    # Draw text on the button
    draw_text(text, font, (0, 0, 0), x + width / 2, y + height / 2, centered)

def main_menu():
    back_button_width, back_button_height = 100, 40
    back_button_x, back_button_y = window_width - back_button_width - 10, window_height - back_button_height - 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the click is on the "Back" button
                if (
                    back_button_x < event.pos[0] < back_button_x + back_button_width
                    and back_button_y < event.pos[1] < back_button_y + back_button_height
                ):
                    # Run gui.py when the "Back" button is clicked
                    subprocess.run(["python", "gui.py"])

        glClearColor(1.0, 0.96, 0.85, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_text("Goat's Win", pygame.font.Font(font_path, 80), (102, 103, 64), window_width / 2, window_height / 2)
        
        # Draw the "Back" button
        draw_button("Back", pygame.font.Font(font_path, 24), (255, 255, 255), back_button_x, back_button_y, back_button_width, back_button_height)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
    glOrtho(0, window_width, window_height, 0, -1, 1)

    main_menu()
