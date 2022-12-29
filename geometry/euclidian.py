from math import sqrt

class EuclidianCoordinates():
    @staticmethod
    def distance_3d(x, y, z):
        return sqrt(x*x + y*y + z*z)
    @staticmethod
    def distance_2d(x, y):
        return sqrt(x*x + y*y)
