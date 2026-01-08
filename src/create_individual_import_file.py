"""
  This script creates a new individuals.csv file listing all the new contributors. It does this
   by reading the records in the exported ActBlue report (Contributions over a specified time period
  under Downloads) csv file, identifying the contributors by name (First + Last), comparing those
  to the list of already-imported names (stored in data/names.txt) and creating a new
  import file with a name ending in _individual.csv.

  The advantage of tracking already imported names is otherwise you have to go through a tedious
  process of merging or correcting names in FECfile during the import process.

  As per the instructions on the importing data to FECFile linked above, drop that file
  onto the comma2fs.exe file which converts the csv to an ASCII 28 formatted file with an .fs extension

  Import that file into FECfile by selecting Tools - Import Names.
"""
import xlrd
import csv
from datetime import datetime

DATA_DIR = 'data/'

FEC_SCHEDULE_A_TEMPLATE = 'FECFILE Import format-V8.0.1.0.xls'
FEC_SCHEDULE_A_SHEET = 'IND-ORG (Template)'
ACTBLUE_FILE = 'westchester-playa-democratic-club---federal-account-34964-contributions-2025_01_01-2026_01_08.csv'
TARGET_WINDOWS_DIRECTORY = '/Volumes/[C] Windows 11/Users/cthomas/Development/WPDC/FEC_Filings/'
FEC_FORMATTED_CSV = ACTBLUE_FILE.replace('.csv', '_individual.csv')
NAMES_LIST_FILE = 'names.txt'

FORM_TYPE = 'SA11AI'
ENTITY_TYPE = 'IND'
MCAN = 0


def generate_csv_header(xls_worksheet: xlrd.sheet.Sheet) -> list[str]:
    """
    Creates a list of import file field names from the template worksheet.
    :param xls_worksheet: FECfile template worksheet
    :return: A list of table field headers
    """

    print(type(xls_worksheet))

    header_list = []
    for col_index in range(21):
        header_list.append(xls_worksheet.cell_value(rowx=0, colx=col_index))

    return header_list


def load_previous_unique_people() -> list[str]:
    """
    Load the list of previously submitted contributors
    :return: A list of names, First + ' ' + Last
    """

    unique_names = []
    with open(DATA_DIR + NAMES_LIST_FILE, 'r') as names_file:
        names_reader = csv.reader(names_file)
        for name in names_reader:
            unique_names.append(name)

    return unique_names


def append_new_unique_people(new_people_names_list: list[str]):
    """
    Append the new names of contributors from this reporting
    period to the running list of unique names
    :param new_people_names_list: A list of First + ' ' + Last names
    :return: Nothing
    """

    with open(DATA_DIR + NAMES_LIST_FILE, 'a') as names_file:
        for name in new_people_names_list:
            names_file.write(name)


def main():
    """Initiate the generation of a ActBlue export to an FEC Names Import formatted file"""

    row_serial_number = 1
    unique_people = load_previous_unique_people()
    fec_template_workbook = xlrd.open_workbook(DATA_DIR + FEC_SCHEDULE_A_TEMPLATE)
    schedule_a_worksheet = fec_template_workbook.sheet_by_name(FEC_SCHEDULE_A_SHEET)
    with open(TARGET_WINDOWS_DIRECTORY +
              FEC_FORMATTED_CSV, 'w') as fec_csv:
        csv_writer = csv.writer(fec_csv)
        csv_header = generate_csv_header(schedule_a_worksheet)
        csv_writer.writerow(csv_header)

        with open(DATA_DIR + ACTBLUE_FILE, 'r') as actblue_csv:
            csv_reader = csv.reader(actblue_csv)
            next(csv_reader, None)
            for row in csv_reader:

                CON_NAME_F = row[10]
                CON_NAME_L = row[11]
                FULL_NAME = CON_NAME_F + ' ' + CON_NAME_L

                if FULL_NAME not in unique_people:
                    CON_ADDR_1 = row[12]
                    CON_ADDR_CITY = row[14]
                    CON_ADDR_STATE = row[15]
                    CON_ADDR_ZIP = row[16]
                    CON_OCC = row[18]
                    CON_EMP = row[19]
                    fec_row = [row_serial_number, '', ENTITY_TYPE, '',
                               CON_NAME_L, CON_NAME_F, '', '', '',
                               CON_ADDR_1, '', CON_ADDR_CITY, CON_ADDR_STATE, CON_ADDR_ZIP,
                               CON_EMP, CON_OCC, '', '', '', '', MCAN]

                    csv_writer.writerow(fec_row)
                    unique_people.append(FULL_NAME)
                    row_serial_number += 1


if __name__ == "__main__":
    main()