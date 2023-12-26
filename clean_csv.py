import pandas as pd
from io import StringIO
import re
from datetime import datetime, timedelta

# Simulated CSV content based on the user's image
csv_content = """recorded,TEMP °C,HUMIDITY %,PRESSURE mBar,CO2 ppm,VOC ppb,PM1 μg/m3,PM2_5 μg/m3
2023-12-10T08:47:02,28.49,52.68,,643,,,
2023-12-10T08:47:04,,,1009,,46,1,2
2023-12-10T08:51:49,,,,,,,
"""

# Read the CSV content into a DataFrame
df = pd.read_csv(StringIO(csv_content), parse_dates=['recorded'])

# Function to combine rows that are within 10 seconds of each other
def combine_rows(df):
    # Sort by the recorded time
    df = df.sort_values(by='recorded')

    # Initialize an empty DataFrame for the combined rows
    combined_df = pd.DataFrame()

    # Iterate over the DataFrame rows
    for _, row in df.iterrows():
        # If the combined DataFrame is empty, add the row to it
        if combined_df.empty:
            combined_df = combined_df.append(row, ignore_index=True)
        else:
            # Check the time difference between the current row and the last row of the combined DataFrame
            time_diff = row['recorded'] - combined_df.iloc[-1]['recorded']
            if time_diff <= timedelta(seconds=10):
                # Combine the rows by taking the maximum of each column, ignoring NaN
                combined_df.iloc[-1] = combined_df.iloc[-1].combine_first(row)
            else:
                # If the time difference is more than 10 seconds, add the row as a new entry
                combined_df = combined_df.append(row, ignore_index=True)

    return combined_df

# Combine rows that are within 10 seconds of each other
combined_df = combine_rows(df)

# Drop rows where all columns except 'recorded' are NaN
cleaned_df = combined_df.dropna(subset=combined_df.columns.difference(['recorded']), how='all')

# Convert cleaned DataFrame back to CSV
cleaned_csv = cleaned_df.to_csv(index=False)

# Display cleaned CSV content
print(cleaned_csv)

# Save the cleaned CSV to a file
cleaned_file_path = '/mnt/data/cleaned_data.csv'
with open(cleaned_file_path, 'w') as file:
    file.write(cleaned_csv)

cleaned_file_path
