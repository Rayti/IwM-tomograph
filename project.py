import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib as plt


def loadImage(path):
    img = mpimg.imread(path)
    return img

#alpha in grades, detectorposition = emitorPosition with alpha + 180
def emitorPosition(previousPosition, origin, alpha):
    alpha = alpha * math.pi / 180
    x0 = previousPosition[0]
    y0 = previousPosition[1]
    xOrigin = origin[0]
    yOrigin = origin[1]
    x1 = xOrigin + (x0 - xOrigin) * math.cos(alpha) - (y0 - yOrigin) * math.sin(alpha)
    y1 = yOrigin + (x0 - xOrigin) * math.sin(alpha) + (y0 - yOrigin) * math.cos(alpha)
    print("x1 -> ", x1)
    print("y1 -> ", y1)
    return [x1, y1]

def bresenham(p0, p1):
    
    pts = []
    
    x0 = p0[0]
    y0 = p0[1]
    
    x1 = p1[0]
    y1 = p1[1]
    
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    err = dx - dy
    while True:
        pts.append((x0,y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2*err
        if e2 > -dy:
            err = err - dy
            x0 = x0 + sx
        if e2 < dx:
            err = err + dx
            y0 = y0 + sy

print(bresenham([5,1], [3,3]))
            
for i in range(0, 1):
    print("\ni -> ", i)
    emitorPosition([3, 2], [3, 3], (math.pi/ 10) * i)

st.write("""
    # My first app
    Hello *world!*
    """)

st.image(loadImage('./tomograf-zdjecia/Kropka.jpg'))
