class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def __str__(self):
        return str(self.p1) + " " + str(self.p2)
    
    def intersect_line_line(self, line):
        # Checks if the two lines intersect
        #(i) compute the slopes
        m1 = (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)
        m2 = (line.p2.y - line.p1.y)/(line.p2.x - line.p1.x)
        #(ii) compute the b's
        b1 = self.p2.y - self.p2.x * m1
        b2 = line.p2.y - line.p2.x * m2
        #Solve the system of equations
        if (m1 == m2):
            return False
        x = (b1 - b2) / (m2 - m1)
        y = self.p1.x * m1 + b1
        if self.p2.x > self.p1.x and line.p2.x > line.p1.x:
            return (x < self.p2.x) and (x > self.p1.x) and (x < line.p2.x) and (x > line.p1.x)
        if self.p2.x < self.p1.x and line.p2.x > line.p1.x:
            return (x > self.p2.x) and (x < self.p1.x) and (x < line.p2.x) and (x > line.p1.x)
        if self.p2.x > self.p1.x and line.p2.x < line.p1.x:
            return (x < self.p2.x) and (x > self.p1.x) and (x > line.p2.x) and (x < line.p1.x)
        if self.p2.x < self.p1.x and line.p2.x < line.p1.x:
            return (x > self.p2.x) and (x < self.p1.x) and (x > line.p2.x) and (x < line.p1.x)
        return False

    def intersect_ray_line(self, ray):
        # Check if the ray and line intersect
        #(i) compute the slopes
        m1 = (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)
        m2 = (ray.p2.y - ray.p1.y)/(ray.p2.x - ray.p1.x)
        #(ii) compute the b's
        b1 = self.p2.y - self.p2.x * m1
        b2 = ray.p2.y - ray.p2.x * m2
        #Solve the system of equations
        if (m1 == m2):
            return False
        x = (b1 - b2) / (m2 - m1)
        y = self.p1.x * m1 + b1
        if self.p2.x > self.p1.x:
            return (x < self.p2.x) and (x > self.p1.x)
        if self.p2.x < self.p1.x:
            return (x > self.p2.x) and (x < self.p1.x)
        return False
    
    def intersect_ray_ray(self, ray):
        # Checks if the two rays intersect
        #(i) compute the slopes
        m1 = (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)
        m2 = (ray.p2.y - ray.p1.y)/(ray.p2.x - ray.p1.x)
        return m1 != m2

    def intersect_to_the_right(self, ray):
        # Checks if the ray intersects to the right the line segment
        if self.intersect_ray_line(ray):
            #(i) compute the slopes
            m1 = (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)
            m2 = (ray.p2.y - ray.p1.y)/(ray.p2.x - ray.p1.x)
            #(ii) compute the b's
            b1 = self.p2.y - self.p2.x * m1
            b2 = ray.p2.y - ray.p2.x * m2
            #Solve the system of equations
            if (m1 == m2):
                return False
            x = (b1 - b2) / (m2 - m1)
            y = self.p1.x * m1 + b1
            if ray.p1.x <= x:
                return True
        return False
