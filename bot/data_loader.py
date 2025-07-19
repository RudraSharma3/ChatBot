import pandas as pd

def load_employee_data(filepath="data/employees.csv"):
    return pd.read_csv(filepath)
