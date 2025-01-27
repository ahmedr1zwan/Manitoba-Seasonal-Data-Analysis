import pandas as pd
import matplotlib.pyplot as plt

# Replace with the actual file path
file_path = "PUB_IntertieScheduleFlowYear_2024.csv"  
data = pd.read_csv(file_path, skiprows=3) 

# Data Cleaning
# Drop rows with missing values and reset the index
data.dropna(inplace=True)
#data.reset_index(drop=True, inplace=True)

# Rename the first two columns for clarity
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
for col in numeric_columns:
    manitoba_data[col] = pd.to_numeric(manitoba_data[col], errors='coerce')  # Convert to numeric, replace invalid values with NaN

manitoba_data[numeric_columns] = manitoba_data[numeric_columns].fillna(0)

seasonal_manitoba = manitoba_data.groupby('Season').agg({
    'Import': 'mean',
    'Export': 'mean',
    'Flow': 'mean',
    'SK Import': 'mean',
    'SK Export': 'mean',
    'SK Flow': 'mean'
}).reset_index()


#print(data.head())
#print(manitoba_data)
#print(seasonal_manitoba)


# PLOT SEASONAL MANTIOBA DATA

plt.figure(figsize=(10, 6))

# Plot for Manitoba
plt.bar(seasonal_manitoba['Season'], seasonal_manitoba['Import'], width=0.35, label='Manitoba Import')
plt.bar(seasonal_manitoba['Season'], seasonal_manitoba['Export'], width=0.35, bottom=seasonal_manitoba['Import'], label='Manitoba Export')
plt.bar(seasonal_manitoba['Season'], seasonal_manitoba['Flow'], width=0.35, bottom=seasonal_manitoba['Import'] + seasonal_manitoba['Export'], label='Manitoba Flow')

# Add labels, legend, and title
plt.title('Manitoba Seasonal Electricity Flows', fontsize=14)
plt.xlabel('Season', fontsize=12)
plt.ylabel('Electricity Flow (MW)', fontsize=12)
plt.legend(loc='upper left', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the plot to a file
plt.savefig('manitoba_seasonal_flows.png', dpi=300)  # Saves the plot as a high-quality PNG file

# Show the plot (optional)
plt.show()