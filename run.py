from tkinter import Tk, Canvas, Frame, BOTH

import gc

import math

from sys import argv

import utils
from utils import coordinates
from utils import grades
from utils import params
from visualization import primitives

from geometry import point
from geometry import line
from geometry import block

from time import time

params = params.Params(argv[1])
bm_coordintates = coordinates.Coordinates.load(params.get_bm_file(), params.get_bm_fields())
contour_coordinates = coordinates.Coordinates.load(params.get_contour_file(), params.get_contour_fields())
grades = grades.Grades.load(params.get_grades_file(), params.get_grades_fields())

lines = []
p1 = None
min_x = math.inf
min_y = math.inf
max_x = 0
max_y = 0

BLOCK_SIZE = int(params.get_block_size())

blocks = []
counter = 0
s = time()

for index, row in bm_coordintates.iterrows():
    x = float(row[params.get_x()])
    y = float(row[params.get_y()])
    c = float(row[params.get_metal()])
    b = block.Block(x, y, c, counter)
    blocks.append(b)
    counter += 1
e = time()
print("Loaded BM (ms) " + str((e-s)*1000))



s = time()
for index, row in contour_coordinates.iterrows():

    x = float(row[params.get_x()])
    y = float(row[params.get_y()])

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
e = time()

print("Loaded contour, ms " + str((e-s)*1000))

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


no_duplicates = []
duplicates = {}
# Supress the duplicates
for b1 in blocks:
    dup_found = False
    if not duplicates.get(str(b1), None):
        no_duplicates.append(b1)
        duplicates[str(b1)] = True
duplicates = None
blocks = no_duplicates



print("Assigning blocks to contour")

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

# The complexity of this algorithm is O(kt)
# Where k is the number of blocks to draw
# t is the number of grades
for b in blocks_to_draw:
    for index, row in grades.iterrows():
        if row[1] != math.inf:
            if float(row[0]) <= b.cmetal and b.cmetal < float(row[1]):
                b.color = row[2]
                b.grade = int(row[3])
                break
        else:
            if float(row[0]) <= b.cmetal:
                b.color = row[2]
                b.grade = int(row[3])
                break
    canvas.draw_block(point.Point(b.x - min_x + 100, b.y - min_y), point.Point(b.x + BLOCK_SIZE - min_x + 100, b.y + BLOCK_SIZE - min_y), b.color)

# The complexity of this algorithm is O(k^2)
# Where k is the number of blocks that fall inside the contour

# We are going to use the network to search for the blocks with the same grade

s = time()

contour_index = 0

for b in blocks_to_draw:
    b.visited = False

# The complexity of the algorithm is
# O(lvk)
for b in blocks_to_draw:

    # l - number of contours
    if b.visited:
        continue
    
    queue = [b]
    
    visited = [False] * len(blocks_to_draw)
    adjucency_matrix = []

    while len(queue) > 0:

        # v - average number of blocks in contour
        # Get the first item from the list
        
        b1 = queue.pop(0)
        adjucency_matrix.append(b1)

        for b2 in blocks_to_draw:

            # k - number of blocks in the main contour
            # Use only those blocks that were not visited

            if b2.visited:
                continue
            
            if b1.x + BLOCK_SIZE == b2.x and b1.y == b2.y and b1.grade == b2.grade:
                if not b2.visited:                    
                    queue.append(b2)
                    b2.visited = True
                    adjucency_matrix.append(b2)
            
            if b1.x - BLOCK_SIZE == b2.x and b1.y == b2.y and b1.grade == b2.grade:
                if not b2.visited:
                    queue.append(b2)
                    b2.visited = True
                    adjucency_matrix.append(b2)

            if b1.x == b2.x and b1.y + BLOCK_SIZE == b2.y and b1.grade == b2.grade:
                if not b2.visited:                    
                    queue.append(b2)
                    b2.visited = True
                    adjucency_matrix.append(b2)

            if b1.x == b2.x and b1.y - BLOCK_SIZE == b2.y and b1.grade == b2.grade:
                if not b2.visited:                    
                    queue.append(b2)
                    b2.visited = True
                    adjucency_matrix.append(b2)
    
    for i in range(0, len(adjucency_matrix)):
        adjucency_matrix[i].contour = contour_index

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
    canvas.draw_block(point.Point(b.x - min_x, b.y - min_y), point.Point(b.x + BLOCK_SIZE - min_x, b.y + BLOCK_SIZE - min_y), COLORS[b.contour % len(COLORS)])
    canvas.draw_text(point.Point(b.x - min_x + 2.5, b.y - min_y + 2.5), str(b.contour), color="black")

s1 = time()

# The complexity of the algorithm is O(lv^2)
output_strings = []
result = []
for i in range(0, contour_index - 1):
    # O(l) - number of contours
    blocks_in_contour = []
    for b in blocks_to_draw:
        # O(k) - number of blocks to draw
        if b.contour == i:
            blocks_in_contour.append(b)
    sclines = []
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
            sclines.append(line.Line(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y), point.Point(b1.x + BLOCK_SIZE + 200 - min_x, b1.y - min_y + BLOCK_SIZE)))
            canvas.draw_line(point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y), point.Point(b1.x + BLOCK_SIZE + 200 - min_x, b1.y - min_y + BLOCK_SIZE), width=4, color="red")
        if not left:
            sclines.append(line.Line(point.Point(b1.x + 200 - min_x, b1.y - min_y), point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE)))
            canvas.draw_line(point.Point(b1.x + 200 - min_x, b1.y - min_y), point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE), width=4, color="red")
        if not top:
            sclines.append(line.Line(point.Point(b1.x + 200 - min_x, b1.y - min_y), point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y)))
            canvas.draw_line(point.Point(b1.x + 200 - min_x, b1.y - min_y), point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y), width=4, color="red")
        if not bottom:
            sclines.append(line.Line(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE), point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y + BLOCK_SIZE)))
            canvas.draw_line(point.Point(b1.x + 200 - min_x, b1.y - min_y + BLOCK_SIZE), point.Point(b1.x + 200 - min_x + BLOCK_SIZE, b1.y - min_y + BLOCK_SIZE), width=4, color="red")

    """
    o = 0
    s = 0
    visited = [False] * len(sclines)
    c1 = 0
    
    while True:

        for e in range(0, len(sclines)):

            if visited[e]:
                continue

            if ((sclines[s].p2.x == sclines[e].p1.x and sclines[s].p2.y == sclines[e].p1.y)):
                canvas.draw_line(sclines[e].p1, sclines[e].p2, width=4, color="black")
                result.append(str(sclines[e].p1.x) + ";" + str(sclines[e].p1.y) + ";" + str(i))
                visited[e] = True
                s = e
                c1 += 1
                break

            if (sclines[s].p2.x == sclines[e].p2.x and sclines[s].p2.y == sclines[e].p2.y):
                canvas.draw_line(sclines[e].p1, sclines[e].p2, width=4, color="black")
                result.append(str(sclines[e].p1.x) + ";" + str(sclines[e].p1.y) + ";" + str(i)) 
                visited[e] = True
                s = e
                c1 += 1
                break

            if (sclines[s].p1.x == sclines[e].p2.x and sclines[s].p1.y == sclines[e].p2.y):
                canvas.draw_line(sclines[e].p1, sclines[e].p2, width=4, color="black")
                result.append(str(sclines[e].p2.x) + ";" + str(sclines[e].p2.y) + ";" + str(i))
                visited[e] = True
                s = e
                c1 += 1
                break

            if (sclines[s].p1.x == sclines[e].p1.x and sclines[s].p1.y == sclines[e].p1.y):
                canvas.draw_line(sclines[e].p1, sclines[e].p2, width=4, color="black")
                result.append(str(sclines[e].p2.x) + ";" + str(sclines[e].p2.y) + ";" + str(i))
                visited[e] = True
                s = e
                c1 += 1
                break

            if c1 < len(sclines) and s == o:
                print("One contour is done")
                for i in range(0, len(visited)):
                    if not visited:
                        s = i
                        o = i
                        break
        
        if c1 == len(sclines):
            break
    """
e1 = time()
print("Saving contours in the file, ms: " + str(((e1-s1)*1000)))

fd = open("output/strings2.csv", "w")
for s in result:
    fd.write(s + "\n")
fd.close()

root.mainloop()
