from ofxstatement.plugin import Plugin
from ofxstatement.parser import StatementParser
from ofxstatement.statement import Statement, StatementLine

import sys
from xml.etree import ElementTree
import hashlib



class PostbankXMLPlugin(Plugin):
    def get_parser(self, filename):
        encoding = self.settings.get('charset', 'iso-8859-1')
        file_obj = open(filename, 'r', encoding=encoding)
        parser = PostbankXMLParser(file_obj)
        parser.statement.account_id = self.settings['account']
        #parser.statement.bank_id = self.settings['bank']
        parser.statement.currency = self.settings.get('currency', 'EUR')
        return parser


class PostbankXMLParser(StatementParser):
    date_format = "%Y-%m-%d"

    def __init__(self, file_obj):
        super(PostbankXMLParser,self).__init__()
        self.__data = file_obj.read()
        self.statement = Statement()


    def P(self,*names):
        res = []
        for name in names:
            res.append("{urn:iso:std:iso:20022:tech:xsd:camt.052.001.03}" + name)
        return '/'.join(res)

    def split_records(self):
        root = ElementTree.fromstring(self.__data)
        return root.findall(self.P('BkToCstmrAcctRpt','Rpt','Ntry'))

    def parse_record(self, record):
        P = self.P

        sl = StatementLine()

        sl.date = self.parse_datetime(record.findall(P('ValDt','Dt'))[0].text)
        sl.amount = float(record.findall(P('Amt'))[0].text)
        sl.trntype = 'DEBIT' if (record.findall(P('CdtDbtInd'))[0].text == "DBIT") else 'CREDIT'
        if sl.trntype == 'DEBIT' and sl.amount > 0:
            sl.amount = -sl.amount
        sl.payee = record.findall(P('NtryDtls','TxDtls','RltdPties','Cdtr','Nm'))[0].text
        sl.memo = ' '.join([e.text for e in record.findall(P('NtryDtls','TxDtls','RmtInf','Ustrd'))])

        # generate unique id
        h = hashlib.sha256()
        h.update(str(sl.date).encode('utf-8'))
        h.update(str(sl.amount).encode('utf-8'))
        h.update(str(sl.trntype).encode('utf-8'))
        h.update(str(sl.payee).encode('utf-8'))
        h.update(str(sl.memo).encode('utf-8'))

        sl.id = h.hexdigest()

        return sl



