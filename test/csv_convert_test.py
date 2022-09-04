import unittest
import src.convert as convert


class CsvConvertTest(unittest.TestCase):
    def test_something(self):
        convert.convert_fortis_csv('dat/example_bnp_paribas.csv')

        self.assertEqual(True, True)  # add assertion here

    def test_payee_named(self):
        row = {
            'Naam van de tegenpartij': 'Jos'
        }

        payee = convert.get_payee(row)

        self.assertEqual(payee, 'Jos')  # add assertion here

    def test_payee_debit(self):
        row = {
            'Naam van de tegenpartij': float('nan'),
            'Details': 'BETALING MET DEBETKAART NUMMER 4871 04XX XXXX 5894 TAKEAWAY.COM AMSTERDAM 28/08/2022 BANKREFERENTIE : 2208290527395430 VALUTADATUM : 28/08/2022'
        }

        payee = convert.get_payee(row)

        self.assertEqual(payee, 'TAKEAWAY.COM AMSTERDAM')  # add assertion here

    def test_payee_debit_2(self):
        row = {
            'Naam van de tegenpartij': float('nan'),
            'Details': 'BETALING MET DEBETKAART NUMMER 4871 04XX XXXX 5894 4370 OKAY GENT GENT 27/08/2022 UITGEVOERD OP 27/08 BANKREFERENTIE : 2208272119007366 VALUTADATUM : 27/08/2022'
        }

        payee = convert.get_payee(row)

        self.assertEqual(payee, 'OKAY GENT GENT')  # add assertion here

    def test_payee_monthly_costs(self):
        row = {
            'Naam van de tegenpartij': float('nan'),
            'Details': 'something',
            'Type verrichting': 'Kosten diverse verrichtingen'
        }

        payee = convert.get_payee(row)

        self.assertEqual(payee, 'BNP Paribas Fortis')  # add assertion here



if __name__ == '__main__':
    unittest.main()
