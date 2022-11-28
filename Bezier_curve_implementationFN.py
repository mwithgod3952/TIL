# -------------------------Libraries
import sys

import math
import random
import numpy as np

import pygame as pg
from pygame.locals import *
# -------------------------

pg.init()

red    = (255, 0, 0)
blue   = (0, 0, 255)
green  = (0, 255, 0)
grey   = (211, 211, 211)

p_sv = []
control_polygon_num = 2
Wth, Hgh = 9 * 10**2, 6 * 10**2

screen = pg.display.set_mode((Wth, Hgh))
pg.display.set_caption('Simple Bezier Curve Implementation')

# ------------------------- Functions
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
    for pi in [p0, p1, p2]:
        photoelectric_effect(circle_pos=pi)
    pg.draw.line(screen, grey, p0, p1, 2)
    pg.draw.line(screen, grey, p1, p2, 2)

    for t in np.arange(0, 1, 0.01):
        bz_vec = bz_math_P(t, p0, p1, p2)
        pg.draw.rect(screen, green, (bz_vec[0], bz_vec[1], 1, 1))

# ------------------------- Visualization
run = True
while run:
    m_pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONUP:
            photoelectric_effect(circle_pos=m_pos); p_sv.append(m_pos)
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    screen.fill(0); p_sv = []

    if len(p_sv) == control_polygon_num:
        p0 = p_sv[0]
        p2 = p_sv[1]
        p1 = m_pos
        main_vis(p0, p1, p2)
    else:
        if len(p_sv) > control_polygon_num:
            for t in np.arange(0, 1, 0.01):
                screen.fill(0)
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

                pg.time.Clock().tick(30)
                pg.display.update()
    pg.display.update()

pg.quit(); sys.exit()