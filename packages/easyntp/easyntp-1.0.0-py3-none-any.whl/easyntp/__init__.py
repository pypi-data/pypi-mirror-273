import datetime
from time import ctime
import ntplib

__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '1.0.0'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/lang-library/py-easyntp'
__all__ = ['EasyNTPClient']


class EasyNTPClient(object):
    def __init__(self, ntp_server_host = 'ntp.nict.jp'):
        self.ntp_client = ntplib.NTPClient()
        self.ntp_server_host = ntp_server_host

    def now(self):
        res = self.ntp_client.request(self.ntp_server_host)
        return datetime.datetime.strptime(ctime(res.tx_time), "%a %b %d %H:%M:%S %Y")

    def format_now(self, timeformat = '%Y/%m/%d %H:%M:%S'):
        t = self.now()
        return t.strftime(timeformat)
