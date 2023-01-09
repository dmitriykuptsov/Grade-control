class Block():
    def __init__(self, x, y, cmetal, index):
        self.x = x
        self.y = y
        self.cmetal = cmetal
        self.grade = 0
        self.contour = None
        self.visited = False
        self.index = index
        self.adjucent = []
        self.color = "gray"
        self.total_blocks_in_contour = 0
        self.average_content = 0
        self.sum_average_content = 0

    def __str__(self):
        return "Block: x=" + str(self.x) + " y=" + str(self.y) + " contour=" + str(self.contour) 