import csv

# Open the CSV file for reading and create a new CSV file for writing
with open('test.csv', mode='r') as input_file,open('test.csv', mode='w') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)

    # Iterate through the rows and replace "Absent" with "0" in the third column
    for row in csv_reader:
            print(row)
            row[2] = "1"
            csv_writer.writerow(row)

print("Replacement completed. The updated data is saved in 'output.csv'.")