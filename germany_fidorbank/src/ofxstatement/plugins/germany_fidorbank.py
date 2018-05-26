import csv
import hashlib
import re

from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import StatementLine


class FidorBankAGPlugin(Plugin):
    def get_parser(self, filename):
        encoding = self.settings.get('charset', 'utf-8')
        with open(filename, 'r', encoding=encoding) as f:
            lines = f.readlines()
        parser = FidorBankAGParser(lines)
        parser.statement.account_id = self.settings['account']
        parser.statement.bank_id = self.settings.get('bank', '50050201')
        parser.statement.currency = self.settings.get('currency', 'EUR')
        return parser


class FidorBankAGParser(CsvStatementParser):
    """
    This plugin tries to parse the provided CSV data into OFX format.
    """
    date_format = "%d.%m.%Y"

    def split_records(self):
        return csv.reader(self.fin, delimiter=';')

    def parse_float(self, f):
        """ convert a number in german localization (e.g. 1.234,56) to float """
        return float(f.replace('.', '').replace(',', '.'))

    def parse_record(self, line):
        if self.cur_record < 2:
            return None
        sl = StatementLine()
        # Build an ID based on an MD5 of the whole line.
        original_line = ";".join(line)
        hl = hashlib.new('md5');
        hl.update(original_line.encode('utf-8'))
        sl.id = hl.hexdigest()
        sl.date = self.parse_datetime(line[0])
        sl.amount = self.parse_float(line[3])
        sl.trntype = 'DEBIT' if sl.amount < 0 else 'CREDIT'
        # Payees generally follow a few formats.
        # Variations in Beschreibung:
        #   MasterCard Onlinekauf bei <PAYEE>
        #   MasterCard Gutschrift in Höhe von <AMOUNT> bei <PAYEE>
        # Variations in Beschreibung2:
        #   Empfänger: <PAYEE>, IBAN: <IBAN>, BIC: <BIC>
        #   Absender: <PAYEE>, IBAN: <IBAN>, BIC: <BIC>
        # Beschreibung2 is empty when the payee is in Beschreibung.
        # Default to blank for unknown patterns.
        sl.payee = ''

        beschreibung2 = "" + line[2]
        if (beschreibung2).strip() != '':
            # Split the Beschreibung2 value by comma, then each list element by comma. Use the second value of the
            # first element for the Payee.
            desc_parts = beschreibung2.split(",")
            desc1_parts = ("" + desc_parts[0]).split(":")
            sl.payee = ("" + desc1_parts[1]).strip()
        else:
            pattern = re.compile('.+ bei (.+)$')
            match = pattern.match(line[1])
            if match:
                sl.payee = match.group(1)

        # Use Beschreibung as the memo.
        sl.memo = line[1]

        return sl
