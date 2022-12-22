from tkinter import Tk, Canvas, Frame, BOTH

import math

import utils
from utils import coordinates
from utils import grades
from visualization import primitives

from geometry import point
from geometry import line
from geometry import block

from time import time

bm_coordintates = coordinates.Coordinates.load("data/BM_OCTOBER_2022_FINAL.csv", ["EAST", "NORTH", "Cu_PCT"])
contour_coordinates = coordinates.Coordinates.load("data/TEST_AREA.csv", ["EAST", "NORTH"])
grades = grades.Grades.load("data/grades.csv", ["START", "END", "COLOR"])

lines = []
p1 = None
min_x = math.inf
min_y = math.inf
max_x = 0
max_y = 0

BLOCK_SIZE = 5

blocks = []
counter = 0
for index, row in bm_coordintates.iterrows():
    x = float(row['EAST'].replace(",", "."))
    y = float(row['NORTH'].replace(",", "."))
    c = float(row['Cu_PCT'].replace(",", "."))
    b = block.Block(x, y, c, counter)
    blocks.append(b)
    counter += 1

for index, row in contour_coordinates.iterrows():

    x = float(row['EAST'].replace(",", "."))
    y = float(row['NORTH'].replace(",", "."))

    if x > max_x:
        max_x = x

    if y > max_y:
        max_y =  y + BLOCK_SIZE

    if x < min_x:
        min_x = x

    if y < min_y:
        min_y = y
    
    if p1 != None:
        p2 = point.Point(x, y)
        l = line.Line(point.Point(p1.x, p1.y), p2)
        lines.append(l)
        p1 = p2
    else:   
        p1 = point.Point(x, y)

for l in lines:
    l.p1.x -= min_x
    l.p1.y -= min_y
    l.p2.x -= min_x
    l.p2.y -= min_y

max_x_ = max_x - min_x
max_y_ = max_y - min_y
min_y_ = min_y - min_y
min_x_ = min_x - min_x


root = Tk()
graphics = primitives.Graphics(root)
root.attributes('-fullscreen', True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
canvas = primitives.Canvas(width, height, 0, 0, max_x_, max_y_, 100, graphics)
canvas.draw_grid()
for l in lines:
    canvas.draw_line(l.p1, l.p2, width=5)

DELTA = 100
blocks_to_draw = []

# The complexity of this algorithm is O(nm)
# Where n is the number of blocks
# and m is the number of lines in the contour

s = time()

index = 0
for b in blocks:
    counter = 0
    if b.x - min_x < 0 or b.y - min_y < 0:
        continue;
    for l in lines:
        ray = line.Line(point.Point(b.x - min_x, b.y - min_y), point.Point(b.x + DELTA - min_x, b.y - min_y))
        if l.intersect_to_the_right(ray):
            counter += 1
    if counter % 2 == 1:
        b.index = index
        blocks_to_draw.append(b)
        index += 1
e = time()

print("Total blocks: " + str(len(blocks)))
print("Total blocks to draw: " + str(len(blocks_to_draw)))
print("Find blocks inside the main contour: " + str((e-s)*1000))

# The complexity of this algorithm is O(k)
# Where k is the number of blocks to draw
for b in blocks_to_draw:
    if b.cmetal >= 0 and b.cmetal < 0.15:
        color = "gray"
    elif b.cmetal >= 0.15 and b.cmetal < 0.20:
        color = "green"
    elif b.cmetal >= 0.20 and b.cmetal < 0.30:
        color = "blue"
    elif b.cmetal >= 0.30 and b.cmetal < 0.46:
        color = "red"
    else:
        color = "orange"
    canvas.draw_block(point.Point(b.x - min_x + 100, b.y - min_y), point.Point(b.x + BLOCK_SIZE - min_x + 100, b.y + BLOCK_SIZE - min_y), color)


# The complexity of this block of code is O(k)
# Where k is the number of blocks inside the master contour
for b in blocks_to_draw:
    if b.cmetal >= 0 and b.cmetal < 0.15:
        b.grade = 1
    elif b.cmetal >= 0.15 and b.cmetal < 0.20:
        b.grade = 2
    elif b.cmetal >= 0.20 and b.cmetal < 0.30:
        b.grade = 4
    elif b.cmetal >= 0.30 and b.cmetal < 0.46:
        b.grade = 5
    else:
        b.grade = 6

# The complexity of this algorithm is O(k^2)
# Where k is the number of blocks that fall inside the contour

# We are going to use the network to search for the blocks with the same grade

s = time()

contour_index = 0

for b in blocks_to_draw:
    b.visited = False

for b in blocks_to_draw:
    # l - number of contours
    if b.visited:
        continue
    queue = [b]
    adjucency_matrix = []
    visited = [False] * len(blocks_to_draw)
    b.contour = contour_index
    for i in range(0, len(blocks_to_draw)):
        adjucency_matrix.append([None] * len(blocks_to_draw))
    while len(queue) > 0:
        # v - average number of blocks in contour
        # Get the first item from the list
        b1 = queue.pop(0)
        b1.visited = True
        adjucency_matrix[b1.index][b1.index] = b
        for b2 in blocks_to_draw:
            # k - number of blocks in the main contour
            # Use only those blocks that were not visited
            if b2.visited:
                continue
            if b1.x + BLOCK_SIZE == b2.x and b1.y == b2.y and b1.grade == b2.grade and b2.visited == False:
                b2.visited = True
                adjucency_matrix[b1.index][b2.index] = b2
                queue.append(b2)
            if b1.x - BLOCK_SIZE == b2.x and b1.y == b2.y and b1.grade == b2.grade and b2.visited == False:
                b2.visited = True
                adjucency_matrix[b1.index][b2.index] = b2
                queue.append(b2)
            if b1.x == b2.x and b1.y + BLOCK_SIZE == b2.y and b1.grade == b2.grade and b2.visited == False:
                b2.visited = True
                adjucency_matrix[b1.index][b2.index] = b2
                queue.append(b2)
            if b1.x == b2.x and b1.y - BLOCK_SIZE == b2.y and b1.grade == b2.grade and b2.visited == False:
                b2.visited = True
                adjucency_matrix[b1.index][b2.index] = b2
                queue.append(b2)
    
    for i in range(0, len(adjucency_matrix)):
        for j in range(0, len(adjucency_matrix)):
            if adjucency_matrix[i][j]:
                adjucency_matrix[i][j].contour = contour_index

    contour_index += 1
# The complexity of the whole algorithm is O(max(lkv, nm))
e = time()
print("Find subcontours: " + str((e-s)*1000))

# The complexity of this algorithm is O(k)
# Where k is the number of blocks to draw
COLORS  =['linen', 'red', 'green', 'blue', 'bisque', 'orange',
'white', 'yellow',  'blue', 'black', 'lavender',
'dark gray', 'pink', 'purple', 'green', 'white',
'gold', 'gray', 'khaki', 'midnight blue', 'medium sea green', 'lime green', 'yellow green',
'rosy brown', 'medium slate blue', 'light coral', 'medium blue', 'tomato', 
'dodger blue', 'salmon']

for b in blocks_to_draw:
    canvas.draw_block(point.Point(b.x - min_x, b.y - min_y), point.Point(b.x + BLOCK_SIZE - min_x, b.y + BLOCK_SIZE - min_y), COLORS[b.contour])

output_strings = []
result = []
for i in range(0, contour_index - 1):
    # O(l) - number of contours
    blocks_in_contour = []
    for b in blocks_to_draw:
        # O(k) - number of blocks to draw
        if b.contour == i:
            blocks_in_contour.append(b)
    end = []
    start = []
    # O(v^2) - average number of blocks in contour
    for b1 in blocks_in_contour:
        
        left = False
        right = False
        top = False
        bottom = False

        for b2 in blocks_in_contour:
            if b1.x + BLOCK_SIZE == b2.x and b1.y == b2.y:
                right = True
            if b1.x - BLOCK_SIZE == b2.x and b1.y == b2.y:
                left = True
            if b1.x == b2.x and b1.y + BLOCK_SIZE == b2.y:
                bottom = True
            if b1.x == b2.x and b1.y - BLOCK_SIZE == b2.y:
                top = True
        if not right:
            start.append(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y))
            end.append(point.Point(b1.x + BLOCK_SIZE + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            end.append(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y))
            start.append(point.Point(b1.x + BLOCK_SIZE + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            #print(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y))
            #print(point.Point(b1.x + BLOCK_SIZE + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            #print('-----')
            canvas.draw_line(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y), point.Point(b1.x + BLOCK_SIZE + 200 - min_x, b1.y - min_y + BLOCK_SIZE), width=4, color="red")
        if not left:
            start.append(point.Point(b1.x + 200 - min_x, b1.y - min_y))
            end.append(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            end.append(point.Point(b1.x + 200 - min_x, b1.y - min_y))
            start.append(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            #print(point.Point(b1.x + 200 - min_x, b1.y - min_y))
            #print(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            #print('-----')
            canvas.draw_line(point.Point(b1.x + 200 - min_x, b1.y - min_y), point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE), width=4, color="red")
        if not top:
            start.append(point.Point(b1.x + 200 - min_x, b1.y - min_y))
            end.append(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y))
            end.append(point.Point(b1.x + 200 - min_x, b1.y - min_y))
            start.append(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y))
            #print(point.Point(b1.x + 200 - min_x, b1.y - min_y))
            #print(point.Point(b1.x + BLOCK_SIZE + 200 - min_x, b1.y - min_y))
            #print('-----')
            canvas.draw_line(point.Point(b1.x + 200 - min_x, b1.y - min_y), point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y), width=4, color="red")
        if not bottom:
            start.append(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            end.append(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y + BLOCK_SIZE))
            end.append(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            start.append(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y + BLOCK_SIZE))
            #print(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            #print(point.Point(b1.x + BLOCK_SIZE + 200 - min_x, b1.y - min_y + BLOCK_SIZE))
            #print('-----')
            canvas.draw_line(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE), point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y + BLOCK_SIZE), width=4, color="red")
    
    """
    visited = []
    queue = [0]
    #result.append(str(start[0].x) + ";" + str(start[0].y) + ";" + str(i))
    for i in range(0, len(start)):
        print(str(start[i]) + " " + str(end[i]))
    print("-----------------")
    """
    z = 0
    s = 0
    e = None
    """
    while e != 0:
        for s in range(0, len(start)):
            if end[e].x == start[s].x and end[e].y == start[s].y:
                #result.append(str(end[s].x) + ";" + str(end[s].y) + ";" + str(i))
                canvas.draw_line(start[e], end[s], width=4, color="black")
                #print(str(end[s].x) + ";" + str(end[e].y) + ";" + str(i))
                e = s
    print(">>>>>>>>>>>>>>")
    """
    #break
fd = open("output/strings2.csv", "w")
for s in result:
    fd.write(s + "\n")
fd.close()

#root.mainloop()
