import sys
from tqdm import tqdm
import csv
import logging
import datetime
import locale
from googletrans import Translator

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

# Get the input and output file paths from the command line arguments
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Specify the indices of the columns in the CSV file
date_column_index = 0
time_column_index = 1
description_column_index = 2

translator = Translator()

logger.info(f"Reading CSV file: {input_file_path}")

# Read the CSV file skipping the header row
with open(input_file_path, "r") as file:
    reader = csv.reader(file)
    next(reader)
    rows = list(reader)

logger.info("finished reading CSV file")

# Process the Date and Time columns and update their localized values
with tqdm(total=len(rows), desc="Processing rows") as pbar:
    for row in rows:
        # Translate the Description to German
        description = row[description_column_index]
        translation = translator.translate(description, dest="de")
        row[description_column_index] = translation.text

        # Parse the Date value
        date_str = row[date_column_index]
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        # Convert the Time strings to datetime objects. Falls back to "%h:%m" if
        # the time parsing fails
        if row[time_column_index] != "":
            time_str = row[time_column_index]

            try:
                time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
            except ValueError:
                time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()

            # Format the Time object with German localization
            formatted_time = time_obj.strftime(locale.nl_langinfo(locale.T_FMT))
            row[time_column_index] = formatted_time

        # Format the Date object with German localization
        formatted_date = date_obj.strftime(locale.nl_langinfo(locale.D_FMT))
        row[date_column_index] = formatted_date

        row.append("Pau Perez")

        pbar.update(1)

# Add headers to the rows
header = ["Datum", "Zeit", "Beschreibung", "Autor"]
rows.insert(0, header)

# Write the updated rows back to the CSV file
with open(output_file_path, "w", newline="") as file:
    writer = csv.writer(file, dialect="excel")
    writer.writerows(rows)

logger.info(
    f"CSV file processed, localized to German and stored to {output_file_path}."
)
