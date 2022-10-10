import pandas as pd

class Indicators():
    def __init__(self):
        self.df = pd.read_csv('routes4.csv',header=None)
        pass