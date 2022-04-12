import pandas as pd

iop_length_of_stay = pd.read_csv('nora_2021_IOP.csv')
housing_length_of_stay = pd.read_csv('nora_2021_Housing.csv')

# distilled_data = iop_length_of_stay.drop(columns=['Provider ', 'Client ', 'Chart ', 'Facility', 'Encounter ', 'Charges ', 'Chargeable CoPay ', 'Copay Notes ', 'Copay ', 'Billed ', 'Appointment Status', 'Billing Errors'])
distilled_data = housing_length_of_stay.drop(columns=['Provider ', 'Client ', 'Chart ', 'Facility', 'Encounter ', 'Charges ', 'Chargeable CoPay ', 'Copay Notes ', 'Copay ', 'Billed ', 'Appointment Status', 'Billing Errors'])


# find oldest encounter for each client from distilled data
oldest_encounter = distilled_data.groupby('ID ').min()
oldest_encounter['Date/Appt '] = pd.to_datetime(oldest_encounter['Date/Appt '])
newest_encounter = distilled_data.groupby('ID ').max()
newest_encounter['Date/Appt '] = pd.to_datetime(newest_encounter['Date/Appt '])
print('----------------------------------------------------')
print(' ')
print('oldest encounter')
print('====================================================')
print(oldest_encounter.head())
print('----------------------------------------------------')
print(' ')
print('----------------------------------------------------')
print('newest encounter')
print('====================================================')
print(newest_encounter.head())


# find length of stay for each client from distilled data
length_of_stay = newest_encounter['Date/Appt '] - oldest_encounter['Date/Appt ']
length_of_stay = length_of_stay.apply(lambda x: x.days)
length_of_stay = pd.DataFrame(length_of_stay)
length_of_stay.columns = ['Length of Stay']
length_of_stay['Length of Stay'] = length_of_stay['Length of Stay'].astype(int)
client_count = 0
print('----------------------------------------------------')
print(' ')
print('client length of stay')
print('====================================================')
for(i, row) in length_of_stay.iterrows():
    if(row['Length of Stay'] < 0):
        length_of_stay.at[i, 'Length of Stay'] = 0
    if(row['Length of Stay'] != 0):
        client_count += 1
        print(row['Length of Stay'])
print('----------------------------------------------------')
print('====================================================')
print('Total Client Count:')
print(client_count)
print('----------------------------------------------------')
print('Average Length of Stay: ')
print(length_of_stay['Length of Stay'].mean())

