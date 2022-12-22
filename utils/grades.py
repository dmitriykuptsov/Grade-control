import pandas as pd

class Grades():
    @staticmethod
    def normalize(coordintates):
        pass
    @staticmethod
    def load(file, columns):
        df = pd.read_csv(file, sep=";")
        return df[columns]
