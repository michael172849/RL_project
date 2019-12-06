import pandas as pd

def preprocessGpsData(df:pd.DataFrame):
    raise NotImplementedError()
    
def addHomeLabels(df:pd.DataFrame):
    """
    replace "unknown" labels for gps data to "Home" at the start and the end of a data per day
    """
    # list of tuples (subject_number(directory name), day) 
    # that we're going to NOT replace (doesn't make sense replacing unknown to home)
    omit_starts = []  
    omit_ends = []