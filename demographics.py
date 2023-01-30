import pandas as pd
import pprint


all_client_diagnoses = pd.read_csv('2019_present_diagnosis.csv')
print(all_client_diagnoses.columns)
nora_clients = all_client_diagnoses.drop_duplicates('Pid').drop(columns=['Date Of Service', 'Encounter', 'Age', 'Service Code'])

nora_gender = nora_clients[nora_clients.Facility == 'Northern Ohio Recovery Association'].groupby('Gender').count()

lorain_gender = nora_clients[nora_clients.Facility == 'Lorain'].groupby('Gender').count()
print('------------------------------------')
print('NORA All Client Gender Breakdown')
print('-------------------------------------')
pprint.pprint(nora_gender)
print('------------------------------------')
print('Lorain All Client Gender Breakdown')
print('-------------------------------------')
pprint.pprint(lorain_gender)
print('------------------------------------')

client_encounters = pd.read_csv('2019_2022_encounters.csv')
print(client_encounters.columns)
nora_clients = client_encounters.drop_duplicates('PID')

nora_category = nora_clients[nora_clients.Facility == 'Northern Ohio Recovery Association'].groupby('Category').count()

lorain_category = nora_clients[nora_clients.Facility == 'Lorain'].groupby('Category').count()
print('------------------------------------')
print('NORA All Client Category Breakdown')
print('-------------------------------------')
pprint.pprint(nora_category)
print('------------------------------------')
print('Lorain All Client Category Breakdown')
print('-------------------------------------')
pprint.pprint(lorain_category)
print('------------------------------------')