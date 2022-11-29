# ------------------------- Libraries
import sys

import math
import random
import numpy as np

import pygame as pg
from pygame.locals import *

'''
    An example that are used in game: https://www.youtube.com/watch?v=Q27YGrDNUVE
'''

pg.init()

red    = (255, 0, 0)
blue   = (0, 0, 255)
green  = (0, 255, 0)
yellow = (255,255,0)
olive  = (128,128,0)
grey   = (211, 211, 211)
white  = (255, 255, 255)

p_sv = []

control_polygon_num = 2
Wth, Hgh = 9 * 10**2, 6 * 10**2

screen = pg.display.set_mode((Wth, Hgh))
pg.display.set_caption('Simple Bezier Curve Implementation')
font_size = 11; font_obj = pg.font.SysFont("arial", font_size, True, False)

# ------------------------- Functions
def cartisian(step = 10, gradation_size = 1.2):
    # x axis
    pg.draw.line(screen, green, (0, Hgh/2), (Wth, Hgh/2), 1)
    # y axis
    pg.draw.line(screen, green, (Wth/2, 0), (Wth/2, Hgh), 1)

    # pixel coordinates value of x
    for i in range(0, Wth, step):
        pg.draw.line(screen, green, (i, (Hgh / 2) - gradation_size), (i, (Hgh / 2) + gradation_size), 1)
    # pixel coordinates value of y
    for j in range(0, Hgh, step):
        pg.draw.line(screen, green, ((Wth / 2) - gradation_size, j), ((Wth / 2) + gradation_size, j), 1)

def coordinates_txt(xy):
    cx = (Wth / 2)
    x_ac = int(xy[0] - cx)
    cy = (Hgh / 2)
    y_ac = int(cy - xy[1])

    P = (x_ac, y_ac)
    txt_obj = font_obj.render(f'x-coordinate: {P[0]},    y-coordinate: {P[1]}', False, olive)

    return screen.blit(txt_obj, (xy[0]+20, xy[1]-40))

def photoelectric_effect(circle_pos):
    eft_arr = np.array([17, 17, 17, 17, 17, 16, 16, 16, 17, 17, 17, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 2, 1, 1, 1])
    for i in range(len(eft_arr)):
        pg.draw.circle(screen, [eft_arr[i] * 8] * 3, circle_pos, i + 1, 1)

def bz_math_P(T, p0, p1, p2):
    b1 = (1-T) ** 2
    b2 = 2 * (1 - T) * T
    b3 = T ** 2
    p_xy = [float(p0[i] * b1 + b2 * p1[i] + p2[i] * b3) for i in [0, 1]]
    return p_xy

def bz_math_Q(T, p0, p1, p2):
    q0_xy = [float(p0[i] * (1 - T) + p1[i] * T) for i in [0 ,1]]
    q1_xy = [float(p1[i] * (1 - T) + p2[i] * T) for i in [0, 1]]
    return [q0_xy, q1_xy]

def main_vis(p0, p1, p2):
    screen.fill(0)
    cartisian()
    if len(p_sv) <= control_polygon_num:
        coordinates_txt(m_pos)

    # pixel_coordinates()
    for pi in [p0, p1, p2]:
        photoelectric_effect(circle_pos=pi)
        # pg.draw.circle(screen, grey, pi, 1)
    pg.draw.line(screen, grey, p0, p1, 2)
    pg.draw.line(screen, grey, p1, p2, 2)

    for t in np.arange(0, 1, 0.01):
        bz_vec = bz_math_P(t, p0, p1, p2)
        pg.draw.rect(screen, yellow, (bz_vec[0], bz_vec[1], 1, 1))

# ------------------------- Visualization
run = True
trigger = 0
while run:
    screen.fill(0)
    m_pos = pg.mouse.get_pos()
    coordinates_txt(m_pos)

    cartisian()
    for event in pg.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONUP:
            photoelectric_effect(circle_pos=m_pos); p_sv.append(m_pos)
            # pg.draw.circle(screen, grey, m_pos, 1); p_sv.append(m_pos);
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    screen.fill(0); p_sv = []
                    cartisian()

    if len(p_sv) == control_polygon_num - 1:
        photoelectric_effect(circle_pos=p_sv[0])
        # pg.draw.circle(screen, grey, p_sv[0], 1)
    if len(p_sv) == control_polygon_num:
        p0 = p_sv[0]
        p2 = p_sv[1]
        p1 = m_pos
        main_vis(p0, p1, p2)
    else:
        if len(p_sv) > control_polygon_num:
            for t in np.arange(0, 1, 0.01):
                p0 = p_sv[0]
                p2 = p_sv[1]
                p1 = p_sv[-1]
                main_vis(p0, p1, p2)

                # calcaulate "Q"
                Vec0 = bz_math_Q(t, p0, p1, p2)
                pg.draw.line(screen, (255, 6, 81), Vec0[0], Vec0[1], 2)

                # calcaulate "P"
                Vec1 = bz_math_P(t, p0, p1, p2)
                pg.draw.circle(screen, blue, (Vec1[0], Vec1[1]), 10)

                coordinates_txt((Vec1[0], Vec1[1]))

                pg.time.Clock().tick(60)
                pg.display.update()
    pg.display.update()

pg.quit(); sys.exit()