import csv

from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import StatementLine


class FrankfurterSparkasse1822Plugin(Plugin):
    def get_parser(self, filename):
        encoding = self.settings.get('charset', 'iso-8859-1')
        with open(filename, 'r', encoding=encoding) as f:
            lines = f.readlines()
        parser = FrankfurterSparkasse1822Parser(lines)
        parser.statement.account_id = self.settings['account']
        parser.statement.bank_id = self.settings.get('bank', '50050201')
        parser.statement.currency = self.settings.get('currency', 'EUR')
        return parser


class FrankfurterSparkasse1822Parser(CsvStatementParser):
    """
    This plugin tries to parse the provided CSV data into the same
    format, as the discontinued OFX export
    """
    date_format = "%d.%m.%Y"

    def split_records(self):
        return csv.reader(self.fin, delimiter=';')

    def parse_float(self, f):
        """ convert a number in german localization (e.g. 1.234,56) to float """
        return float(f.replace('.', '').replace(',', '.'))

    def parse_record(self, line):
        # FIXME: add header validation
        if self.cur_record < 2:
            return None
        if len(line) < 3:
            """e.g.: ['# 1 vorgemerkte Umsätze nicht angezeigt']"""
            return None
        if not line[2]:
            return None
        sl = StatementLine()
        sl.id = line[1]
        sl.date = self.parse_datetime(line[2])
        sl.amount = self.parse_float(line[4])
        sl.trntype = 'DEBIT' if sl.amount < 0 else 'CREDIT'
        sl.payee = line[7]
        # check for special transactions
        if line[6] == "Entgeltabschluss":
            sl.memo = "%s: %s %s" % (line[6], line[13], line[14])
        elif line[6] == "Wertpapiere" or line[7] == "KREDITKARTENABRECHNUNG":
            sl.memo = "(%s/%s): %s" % (line[8], line[9], " ".join(line[15:]).strip())
        elif not line[8] and not line[9]:
            # empty transaction
            print("empty", line)
            return None
        else:
            sl.memo = "(%s/%s): %s" % (line[8], line[9], " ".join(e for e in line[13:] if e).strip())

        return sl

