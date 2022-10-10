import glob
import sys
import pandas
import re
import math

YNAB_CSV_COLUMNS = ['Date', 'Payee', 'Memo', 'Outflow', 'Inflow']
BNP_PATH = '/Users/jasperspruytte/Documents/finance/bnp/'
YNAB_PATH = '/Users/jasperspruytte/Documents/finance/ynab/'


def convert_fortis_csv():
    for file in glob.glob(BNP_PATH + '*.csv'):
        print('Converting csv:', file)
        fortis_csv = pandas.read_csv(file, sep=';')
        ynab_csv = pandas.DataFrame(columns=YNAB_CSV_COLUMNS)
        for index, row in fortis_csv.iterrows():
            amount = float(row['Bedrag'])
            amount_formatted = "{:10.2f}".format(math.fabs(row['Bedrag']))
            ynab_csv = ynab_csv.append({
                'Date': row['Uitvoeringsdatum'],
                'Payee': get_payee(row),
                'Memo': row['Mededeling'],
                'Outflow': amount_formatted if amount <= 0 else None,
                'Inflow': amount_formatted if amount > 0 else None
            }, ignore_index=True)
        ynab_csv.to_csv(YNAB_PATH + 'output.csv', index=False)


def get_payee(row):
    if 'Naam van de tegenpartij' in row and row['Naam van de tegenpartij'] is not None and isinstance(row['Naam van de tegenpartij'], str):
        return row['Naam van de tegenpartij']
    if 'BETALING MET DEBETKAART' in row['Details']:
        debit_regex = r"BETALING MET DEBETKAART NUMMER [0-9 X]*([a-zA-Z. ]*) .*"
        result = re.search(debit_regex, row['Details'])
        return result.group(1) if result else None
    if row['Type verrichting'] == 'Kosten diverse verrichtingen':
        return 'BNP Paribas Fortis'
    return None


if __name__ == '__main__':
    convert_fortis_csv()
