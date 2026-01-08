"""
  This script transforms an ActBlue report exported (Contributions over a specified time period
  under Downloads) csv file into an FECFile supported format as described in the template
  referenced in the instructions on the FEC site:
  https://www.fec.gov/help-candidates-and-committees/filing-reports/importing-data-fecfile/
  So far this supports the Schedule A or itemized contributions table, otherwise known
  as transactions in the FECFile software.

  The script will create a file with a name ending in _scheda.csv

  As per the instructions on the importing data to FECFile linked above, drop that file
  onto the comma2fs.exe file which converts the csv to an ASCII 28 formatted file with an .fs extension

  Import that file into FECfile by selecting Tools - Import Transactions.
"""
import xlrd
import csv
from datetime import datetime

DATA_DIR = 'data/'

FEC_SCHEDULE_A_TEMPLATE = 'FECFILE Import format-V8.0.1.0.xls'
FEC_SCHEDULE_A_SHEET = 'Sch A (Template)'
ACTBLUE_FILE = 'westchester-playa-democratic-club---federal-account-34964-contributions-2025_01_01-2026_01_08.csv'
TARGET_WINDOWS_DIRECTORY = '/Volumes/[C] Windows 11/Users/cthomas/Development/WPDC/FEC_Filings/'
FEC_FORMATTED_CSV = ACTBLUE_FILE.replace('.csv', '_scheda.csv')

FORM_TYPE = 'SA11AI'
ENTITY_TYPE = 'PAC'
ELECTION_CODE = 'G2026'


def generate_csv_header(xls_worksheet: xlrd.sheet.Sheet) -> list[str]:
    """
    Creates a list of import file field names from the template worksheet.
    :param xls_worksheet: FECfile template worksheet
    :return: A list of table field headers
    """
    header_list = []
    for col_index in range(45):
        header_list.append(xls_worksheet.cell_value(rowx=0, colx=col_index))

    return header_list


def main():
    """Initiate the conversion of a ActBlue export to an FEC Schedule A
       Transaction Import formatted file"""

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

                CON_DATE_RAW = row[1].split(' ')[0]
                date_obj = datetime.strptime(CON_DATE_RAW, '%m/%d/%y')
                CON_DATE = date_obj.strftime('%Y%m%d')

                CON_AMT = row[2]
                CON_NAME_F = row[10]
                CON_NAME_L = row[11]
                CON_ADDR_1 = row[12]
                CON_ADDR_CITY = row[14]
                CON_ADDR_STATE = row[15]
                CON_ADDR_ZIP = row[16]
                CON_OCC = row[18]
                CON_EMP = row[19]
                fec_row = [FORM_TYPE, '', '', '', '', ENTITY_TYPE, '',
                           CON_NAME_L, CON_NAME_F, '', '', '',
                           CON_ADDR_1, '', CON_ADDR_CITY, CON_ADDR_STATE, CON_ADDR_ZIP,
                           ELECTION_CODE, '', CON_DATE, CON_AMT, '', '',
                           CON_EMP, CON_OCC, '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', 'I', '', '']

                csv_writer.writerow(fec_row)


if __name__ == "__main__":
    main()