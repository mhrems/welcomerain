'''
Created on Sep 26, 2012

@author: bond
'''

#PLUGIN_NAME = 'power1'
#SERIAL_PORT = '/dev/ttyUSB0'

SERIAL_TIMEOUT = 1
SERIAL_DEMO_DATA = 'S:    01VO:    01Am:    01Wa: 13012Wh:  10001PD:     01Hz  E'

AD_DATA_MIN_LEN = 50
AD_DATA_START_STR = 'S'
AD_DATA_END_STR = 'E'
ADPOWER_KEY_VALUE_SEPARATOR = '+'

MYSQL_HOST = 'localhost'
MYSQL_USER = 'esco'
MYSQL_PASSWORD = 'dptmzh123'
MYSQL_DATABASE = 'esco'
MYSQL_RACK_POWER_TABLE = 'power_rack'

NOTI_SMTP_EMAIL = 'mhr.noti@gmail.com'
NOTI_SMTP_PASS = 'vkdnjapdlf'
NOTI_FROM_EMAIL = 'mhr.noti@gmail.com'
NOTI_TO_EMAIL = 'mhr.noti@gmail.com'
EMAIL_TITLE = 'power measurement message'
