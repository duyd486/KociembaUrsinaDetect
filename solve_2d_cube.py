import cv2
import numpy as np
import kociemba as Cube



sign_conv = {
    'green': 'F',
    'white': 'U',
    'blue': 'B',
    'red': 'R',
    'orange': 'L',
    'yellow': 'D'
}

color = {
    'red': (0, 0, 255),
    'orange': (0, 165, 255),
    'blue': (255, 0, 0),
    'green': (0, 128, 0),
    'white': (255, 255, 255),
    'yellow': (0, 255, 255),
    'black': (0, 0, 0),
}

font = cv2.FONT_HERSHEY_SIMPLEX
textPoints = {
    'up': [['U', 242, 202], ['W', (255, 255, 255), 260, 208]],
    'right': [['R', 380, 354], ['R', (0, 0, 255), 398, 360]],
    'front': [['F', 242, 354], ['G', (0, 255, 0), 260, 360]],
    'down': [['D', 242, 508], ['Y', (0, 255, 255), 260, 514]],
    'left': [['L', 104, 354], ['O', (0, 165, 255), 122, 360]],
    'back': [['B', 518, 354], ['B', (255, 0, 0), 536, 360]],
}



def detect_solve(state):
    raw = ''
    for i in state:
        for j in state[i]:
            raw += sign_conv[j]
    #print("answer:", Cube.solve(raw))
    return Cube.solve(raw)


def color_detect(h, s, v):
    # print(h,s,v)
    if (h > 140 and h <= 180 and s > 45) or (h > 0 and h < 5 and s > 45):
        return 'red'
    elif h >= 5 and h < 21 and s > 45:
        return 'orange'
    elif h > 20 and h <= 40 and s > 45:
        return 'yellow'
    elif h > 40 and h < 90 and s > 45:
        return 'green'
    elif h >= 90 and h < 140 and s > 45:
        return 'blue'
    elif s <= 50:
        return 'white'

    return 'red'


def draw_stickers(frame, stickers, name):
    for x, y in stickers[name]:
        cv2.rectangle(frame, (x, y), (x + 30, y + 30), (255, 255, 255), 2)


def draw_preview_stickers(frame, stickers):
    stick = ['front', 'back', 'left', 'right', 'up', 'down']
    for name in stick:
        for x, y in stickers[name]:
            cv2.rectangle(frame, (x, y), (x + 40, y + 40), (255, 255, 255), 2)


def texton_preview_stickers(frame, stickers):
    stick = ['front', 'back', 'left', 'right', 'up', 'down']
    for name in stick:
        for x, y in stickers[name]:
            sym, x1, y1 = textPoints[name][0][0], textPoints[name][0][1], textPoints[name][0][2]
            cv2.putText(preview, sym, (x1, y1), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            sym, col, x1, y1 = textPoints[name][1][0], textPoints[name][1][1], textPoints[name][1][2], \
            textPoints[name][1][3]
            cv2.putText(preview, sym, (x1, y1), font, 0.5, col, 1, cv2.LINE_AA)


def fill_stickers(frame, stickers, sides):
    for side, colors in sides.items():
        num = 0
        for x, y in stickers[side]:
            cv2.rectangle(frame, (x, y), (x + 40, y + 40), color[colors[num]], -1)
            num += 1



preview = np.zeros((700,800,3), np.uint8)