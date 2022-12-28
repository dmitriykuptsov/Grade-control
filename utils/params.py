import pandas as pd

class Params():
    def __init__(self, file):
        df = pd.read_csv(file, sep=";")
        self.params = {}
        for index, row in df.iterrows():
            print(row[0])
            if row[0] == "BM":
                self.params["BM"] = row[1]
            if row[0] == "CONTOUR":
                self.params["CONTOUR"] = row[1]
            if row[0] == "BM_FIELDS":
                self.params["BM_FIELDS"] = [row[1], row[2], row[3]]
            if row[0] == "CONTOUR_FILEDS":
                self.params["CONTOUR_FILEDS"] = [row[1], row[2]]
            if row[0] == "X":
                self.params["X"] = row[1]
            if row[0] == "Y":
                self.params["Y"] = row[1]                
            if row[0] == "METAL":
                self.params["METAL"] = row[1]
            if row[0] == "GRADES":
                self.params["GRADES"] = row[1]
            if row[0] == "GRADES_FIELDS":
                self.params["GRADES_FIELDS"] = [row[1], row[2], row[3], row[4]]
            if row[0] == "BLOCK_SIZE":
                self.params["BLOCK_SIZE"] = row[1]
            if row[0] == "OUTPUT":
                self.params["OUTPUT"] = row[1]
    def get_grades_file(self):
        return self.params["GRADES"]
    def get_grades_fields(self):
        return self.params["GRADES_FIELDS"]
    def get_bm_file(self):
        return self.params["BM"]
    def get_contour_file(self):
        return self.params["CONTOUR"]
    def get_bm_fields(self):
        return self.params["BM_FIELDS"]
    def get_contour_fields(self):
        return self.params["CONTOUR_FILEDS"]
    def get_x(self):
        return self.params["X"]
    def get_y(self):
        return self.params["Y"]
    def get_metal(self):
        return self.params["METAL"]
    def get_block_size(self):
        return self.params["BLOCK_SIZE"]
    def get_ouput_file(self):
        return self.params["OUTPUT"]