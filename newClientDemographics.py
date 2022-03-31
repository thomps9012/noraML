import pandas as pd
import pprint

newclient_diagnoses = pd.read_csv('2021_possible_diagnoses.csv')
print(newclient_diagnoses.columns)

newclient_primary = newclient_diagnoses.drop(columns=['Diagnosis Date ', 'Client Name ', 'PID ', 'External ID ', 'Age '])
nora_newclient_diagnoses = newclient_primary.groupby('Diagnosis Name ').count()
nora_newclient_gender = newclient_primary.groupby('Gender ').count()
print('NORA New Client Primary Diagnosis')
print('------------------------------------')
pprint.pprint(nora_newclient_diagnoses)
print('-------------------------------------')
print('NORA New Client Gender Breakdown')
print('-------------------------------------')
pprint.pprint(nora_newclient_gender)
print('------------------------------------')