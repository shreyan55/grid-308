import csv

# Input CSV file name
input_csv_filename = 'apps/ml/data/flipkart_com-ecommerce_sample.csv'

# Output CSV file name for the first 10 entries
output_csv_filename = 'apps/ml/data/output.csv'

# Open the input CSV file for reading
with open(input_csv_filename, 'r', newline='') as input_csv_file:
    csv_reader = csv.reader(input_csv_file)
    
    # Read the header if it exists
    header = next(csv_reader, None)
    
    # Read the first 10 rows from the CSV file
    first_10_entries = [header] + [next(csv_reader) for _ in range(5)]

# Create a new CSV file and write the first 10 entries to it
with open(output_csv_filename, 'w', newline='') as output_csv_file:
    csv_writer = csv.writer(output_csv_file)
    csv_writer.writerows(first_10_entries)

print("First 10 entries extracted and saved to", output_csv_filename)
