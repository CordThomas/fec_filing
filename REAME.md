# FEC Filing with ActBlue

This project is a collection of Python scripts that facilitate treasurer reporting
requirements to the Federal Election Commission (FEC). The FEC offers free software
to manage all aspects of filing, [FECfile](https://efilingapps.fec.gov/registration/fecfile.htm).

FECfile has some basic import features that can significantly streamline adding
contributor names and contribution transactions to the FECfile database for submission 
to the FEC. These import procedures are explained on the 
[FECfile website](https://www.fec.gov/help-candidates-and-committees/filing-reports/importing-data-fecfile/)
where you can download the data format converter. The format converter download includes 
an executable and templates for IND/ORG names, Schedule A, Schedule B and Schedule H4 data.

The FECfile software unfortunately only runs on Windows, despite being largely written in Java. 
These scripts will run on either Windows or MacOS. I do most of my development in Mac, so 
if there are issues running on Windows, let me know.

Also note, this is not an endorsement of ActBlue; just happens to be the donor management platform
our political action committee has chosen.

## Installation

Currently, this is simply a set of Python standalone scripts. Clone the repository to your 
local computer, navigate into the **fec_file** directory and execute the following:

```pip install -r requirements.txt```

## Usage

### Retrieve ActBlue Data for Current Reporting Period

The FECfile software maintains a local database of all previously submitted information, 
people and transactions. This means that each reporting period, you only need to retrieve
the records for that period and FECfile will handle things like figuring out which
donors are to be itemized vs not given their total annual giving to date. For instance, 
if you are reporting for Q2 2026 in an election year, you would download the transactions
from ActBlue from 4/1/2026 to 6/30/2026.

* Log into your [ActBlue](www.actblue.com) account and navigate to Downloads using the left navigation.
* Enter the date range for the reporting period in the *Contributions over a specified time period* 
section and chose Export CSV
* Copy the file, likely delivered to your Downloads directory with a name including the name of your PAC and 
account information, to the local data directory in this project

### Generate the Updated Names Import Source

From the fec_filing root directory, execute

```python src/create_individual_import_file.py```

This creates a file that ends in _individual.csv in the data directory.
It also updates the data/names.txt file with new names not previously imported (see script for details)

### Generate the Updated Transactions Import Source

From the fec_filing root directory, execute

```python src/convert_actblue_to_fec_schedule_a.py```

This creates a file that ends in _scheda.csv in the data directory.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)