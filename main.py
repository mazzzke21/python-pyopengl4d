import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def rotation_matrix_4d(angle, axis1, axis2):
    c = np.cos(angle)
    s = np.sin(angle)
    matrix = np.identity(4)
    matrix[axis1, axis1] = c
    matrix[axis1, axis2] = -s
    matrix[axis2, axis1] = s
    matrix[axis2, axis2] = c
    return matrix

def project_4d_to_3d(point_4d):
    w = point_4d[3]
    scale = 2 / (4 + w)
    return point_4d[:3] * scale

def draw_tesseract():
    vertices_4d = np.array([
        [-1, -1, -1, -1],
        [ 1, -1, -1, -1],
        [ 1,  1, -1, -1],
        [-1,  1, -1, -1],
        [-1, -1,  1, -1],
        [ 1, -1,  1, -1],
        [ 1,  1,  1, -1],
        [-1,  1,  1, -1],
        [-1, -1, -1,  1],
        [ 1, -1, -1,  1],
        [ 1,  1, -1,  1],
        [-1,  1, -1,  1],
        [-1, -1,  1,  1],
        [ 1, -1,  1,  1],
        [ 1,  1,  1,  1],
        [-1,  1,  1,  1]
    ], dtype=float)

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
        (8, 9), (9, 10), (10, 11), (11, 8),
        (12, 13), (13, 14), (14, 15), (15, 12),
        (8, 12), (9, 13), (10, 14), (11, 15),
        (0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13), (6, 14), (7, 15)
    ]

    glColor3f(1.0, 1.0, 1.0) 
    glBegin(GL_LINES)
    for edge in edges:
        p1 = vertices_4d[edge[0]]
        p2 = vertices_4d[edge[1]]
        
        rotated_p1 = np.dot(rotation_matrix_4d(angle_x, 0, 3), p1)
        rotated_p1 = np.dot(rotation_matrix_4d(angle_y, 1, 3), rotated_p1)
        rotated_p1 = np.dot(rotation_matrix_4d(angle_z, 2, 3), rotated_p1)

        rotated_p2 = np.dot(rotation_matrix_4d(angle_x, 0, 3), p2)
        rotated_p2 = np.dot(rotation_matrix_4d(angle_y, 1, 3), rotated_p2)
        rotated_p2 = np.dot(rotation_matrix_4d(angle_z, 2, 3), rotated_p2)
        
        projected_p1 = project_4d_to_3d(rotated_p1)
        projected_p2 = project_4d_to_3d(rotated_p2)
        
        glVertex3f(projected_p1[0], projected_p1[1], projected_p1[2])
        glVertex3f(projected_p2[0], projected_p2[1], projected_p2[2])

    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)  

    global angle_x, angle_y, angle_z
    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0

    clock = pygame.time.Clock()  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        angle_x += 0.001 * clock.get_time()
        angle_y += 0.002 * clock.get_time()
        angle_z += 0.003 * clock.get_time()
        

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        draw_tesseract()

        pygame.display.flip()
        clock.tick(60) #fps


if __name__ == "__main__":
    main()
