import pandas as pd
import os

def get_cmp1():
    data_path = os.path.join(os.path.dirname(__file__), 'cmp1.csv')
    return pd.read_csv(data_path)
def get_adm1():
    data_path = os.path.join(os.path.dirname(__file__), 'adm1.csv')
    return pd.read_csv(data_path)

def get_enr1():
    data_path = os.path.join(os.path.dirname(__file__), 'enr1.csv')
    return pd.read_csv(data_path)

def get_crs1():
    data_path = os.path.join(os.path.dirname(__file__), 'crs1.csv')
    return pd.read_csv(data_path)

