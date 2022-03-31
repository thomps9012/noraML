import pandas as pd
import pprint

all_client_diagnoses = pd.read_csv('2021_encounters_with_diagnoses.csv')
print(all_client_diagnoses.columns)

nora_clients = all_client_diagnoses.drop_duplicates('Pid').drop(columns=['Date Of Service', 'Encounter', 'Age', 'Service Code'])
nora_diagnoses = nora_clients[nora_clients.Facility == 'Northern Ohio Recovery Association'].replace(['F10.10', 'F10.11', 'F10.20', 'F10.21', 'F10.239'], 'Alcohol abuse').replace(['F11.20', 'F11.21'], 'Opioid abuse').replace(['F12.10', 'F12.20', 'F12.90', 'F12.21'], 'Cannabis abuse').replace(['F14.11', 'F14.20'], 'Cocaine abuse').replace(['F15.10', 'F15.11', 'F15.20'], 'Other Stimulant abuse').replace(['F16.10', 'F16.20'], 'Hallucinogen abuse').replace('F41.1', 'Anxiety Disorder').replace('Z03.89', 'No Diagnosis').groupby('Diagnosis Code 1').count()
lorain_diagnoses = nora_clients[nora_clients.Facility == 'Lorain'].replace(['F10.10', 'F10.20'], 'Alcohol abuse').replace(['F11.20', 'F11.21'], 'Opioid abuse').replace(['F12.20', 'F12.11','F12.21'], 'Cannabis abuse').replace('F13.20', 'Sedative abuse').replace(['F14.20'], 'Cocaine abuse').replace(['F15.20'], 'Other Stimulant abuse').replace(['F31.61'], 'Bipolar Disorder').replace('F41.1', 'Anxiety Disorder').replace('Z53.20', 'Patient Left for Unspecified Reasons').groupby('Diagnosis Code 1').count()
print('------------------------------------')
print('NORA All Client Primary Diagnosis')
print('------------------------------------')
pprint.pprint(nora_diagnoses)
print('-------------------------------------')
print('Lorain All Client Primary Diagnosis')
print('------------------------------------')
pprint.pprint(lorain_diagnoses)
print('-------------------------------------')