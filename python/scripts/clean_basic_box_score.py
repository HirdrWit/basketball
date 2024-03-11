import re
import csv
from python.data import team_standings

# Temp Step 4: Clean the CSV File, output as output_file.csv
input_file_path = '../data/basic_box_score_stats.csv'
output_file_path = '../data/output_file.csv'


def time_to_minutes(time_str):
    # Split the time string into hours and minutes
    hours, minutes = map(int, time_str.split(':'))

    # Convert hours to minutes and add to the total minutes
    total_minutes = hours * 60 + minutes

    return total_minutes

def is_minutes(text):
    pattern = r'(\d+):(\d+)'  # Regular expression pattern to match [12:34]
    match = re.search(pattern, text)
    if match:
        return True
    return False


# Read from input CSV file and write to output CSV file
with open(input_file_path, 'r', newline='') as input_file, open(output_file_path, 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Iterate over each row in the input CSV file
    for i, row in enumerate(reader):
        if i == 0:
            writer.writerow(row)
            continue

        if not is_minutes(row[3]):
            continue

        ts = team_standings.get_dict()
        row[0] = ts.get(row[0])
        row[1] = ts.get(row[1])
        row[3] = time_to_minutes(row[3])


        writer.writerow(row)
