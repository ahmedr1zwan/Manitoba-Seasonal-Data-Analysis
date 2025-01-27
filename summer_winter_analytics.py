import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = "PUB_IntertieScheduleFlowYear_2024.csv"  # Replace with the actual file path
data = pd.read_csv(file_path, skiprows=3)  

# Data Cleaning
# Drop rows with missing values and reset the index
data.dropna(inplace=True)
#data.reset_index(drop=True, inplace=True)


data.rename(columns={data.columns[0]: 'Date', data.columns[1]: 'Hour'}, inplace=True)
data = data.iloc[1:]  # Skip the repeated header row
data.reset_index(drop=True, inplace=True)

data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

manitoba_data = data.filter(regex='^(Date|Hour|MANITOBA)', axis=1).copy()

manitoba_data.rename(columns={
    'MANITOBA': 'Import',
    'MANITOBA.1': 'Export',
    'MANITOBA.2': 'Flow',
    'MANITOBA SK': 'SK Import',
    'MANITOBA SK.1': 'SK Export',
    'MANITOBA SK.2': 'SK Flow'
}, inplace=True)

manitoba_data['Month'] = pd.to_datetime(manitoba_data['Date']).dt.month
manitoba_data['Season'] = manitoba_data['Month'].apply(lambda x: 'Winter' if x in [12, 1, 2] else
                                                       ('Summer' if x in [6, 7, 8] else 'Other'))

numeric_columns = ['Import', 'Export', 'Flow', 'SK Import', 'SK Export', 'SK Flow']

# Convert to numeric, replace invalid values with NaN
for col in numeric_columns:
    manitoba_data[col] = pd.to_numeric(manitoba_data[col], errors='coerce')  

manitoba_data[numeric_columns] = manitoba_data[numeric_columns].fillna(0)

seasonal_peaks = manitoba_data.groupby('Season').agg({
    'Import': ['mean', 'max'],  # Find the mean and max for Import
    'Export': ['mean', 'max'],  # Find the mean and max for Export
    'Flow': ['mean', 'max'],    # Find the mean and max for Flow
    'SK Import': ['mean', 'max'],
    'SK Export': ['mean', 'max'],
    'SK Flow': ['mean', 'max']
}).reset_index()




# Flatten multi-level columns for easier readability
seasonal_peaks.columns = ['Season'] + [
    f"{col[0]}_{col[1]}" for col in seasonal_peaks.columns[1:]
]

# Display results
print(seasonal_peaks)

# Extract specific seasonal data for Winter and Summer
winter_peaks = seasonal_peaks[seasonal_peaks['Season'] == 'Winter']
summer_moderation = seasonal_peaks[seasonal_peaks['Season'] == 'Summer']

# Display Winter and Summer details
print("Winter  Values:")
print(winter_peaks)

print("Summer  Values:")
print(summer_moderation)

