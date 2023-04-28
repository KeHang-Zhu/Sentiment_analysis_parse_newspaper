import os
import pandas as pd
from collections import defaultdict

# Read the CSV file and filter the DataFrame
df = pd.read_csv('/n/home09/zkh/Panic/4_20_CA_newspapers - 4_20_CA_newspapers.csv', encoding='latin-1')
df.columns = [c.strip() for c in df.columns]
df['First Issue Date'] = pd.to_datetime(df['First Issue Date'])
df['Last Issue Date'] = pd.to_datetime(df['Last Issue Date'])
df['First Issue Year'] = df['First Issue Date'].dt.year
df['Last Issue Year'] = df['Last Issue Date'].dt.year
df_filtered = df[(df['First Issue Year'] < 1940) & (df['Last Issue Year'] > 1920)]

# Create a dictionary to store the mapping of LCCN to State
lccn_to_state = {row['LCCN']: row['State'] for _, row in df_filtered.iterrows()}

# Initialize the results dictionary
results = defaultdict(lambda: defaultdict(lambda: {'score': 0, 'number': 0}))

# Iterate over the directories and files in the 'urls' folder
root_dir = '/n/holyscratch01/kozinsky_lab/Kehang/panic/urls'
for lccn in os.listdir(root_dir):
    if lccn in lccn_to_state:
        state = lccn_to_state[lccn]
        lccn_dir = os.path.join(root_dir, lccn)
        for year_file in os.listdir(lccn_dir):
            year = int(year_file[:-4])  # Remove '.txt' and convert to int
            with open(os.path.join(lccn_dir, year_file), 'r') as f:
                score, number = [float(x) for x in f.readlines()]
                results[state][year]['score'] += score
                results[state][year]['number'] += number

# Write the final dictionary to 'result.txt'
# with open('result.txt', 'w') as f:
#     for state, years in results.items():
#         for year, data in years.items():
#             f.write(f"{state}, {year}, {data['score']}, {data['number']}\n")
# Sort the final dictionary by state and then year
sorted_results = sorted(
    [(state, year, data['score'], data['number'])
     for state, years in results.items()
     for year, data in years.items()],
    key=lambda x: (x[0], x[1])
)

# Write the sorted results to 'result.txt'
with open('result.txt', 'w') as f:
    for state, year, score, number in sorted_results:
        f.write(f"{state}, {year}, {score}, {number}\n")

