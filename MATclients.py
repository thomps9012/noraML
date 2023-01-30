import pandas as pd
from pprint import pprint

mat_clients = pd.read_csv("2021_MAT_clients.csv").drop_duplicates("PID")

print('------------------------------------')
print('NORA 2021 MAT Client Count')
print('-------------------------------------')
pprint(mat_clients.count())
print('------------------------------------')
print('NORA 2021 MAT Clients')
print('-------------------------------------')
pprint(mat_clients)
