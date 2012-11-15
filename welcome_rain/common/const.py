#RRD_PATH = "/home/james/djagno_project/welcome_rain/rrds"    
#RRD_PATH = "/var/lib/ganglia/rrds"
RRD_PATH = "/home/james/Workspace/Project/WelcomeRain/rrds"

SUMMARY_NODE = "__SummaryInfo__"
NONE_NODE = "None"
RRDFILE_EXT = ".rrd"
NODE_SEPERATOR = "/"
TARGET_SEPERATOR = ";"

LOGGERS = "wr.custom"
DEFAULT_DATA_FIELD = "sum"
API_SERVER = "192.168.0.220"
#API_SERVER = "121.78.236.134"
API_PORT = 8080


RET_FAIL = -1

NODE_TYPE_ROOT = 0
NODE_TYPE_MENU = 1
NODE_TYPE_MENU_START = 2
NODE_TYPE_MENU_END = 3
NODE_TYPE_DATA = 4


# for sub menu tree
NODE_UL = "ul"
NODE_LI = "li"
NODE_LINK = "a"

# for api response error handing
RESPONSE_CODE_OK = 2000
RESPONSE_CODE_ERROR = 2001

RESPONSE_OK = "ok"


# page
APIDATA_EQUAL = "!*"
APIDATA_SEPERATOR = "+$"
ALERT_HISTORY_NUMBER_OF_PAGE = 20

#gmetad
#GMETAD_IP = "192.168.0.11"
GMETAD_IP = "121.78.236.134"
GMETAD_PORT = 8652

#Dashboard Data Count
DASHBOARD_DATA_LIMIT = 30


#For Side Menu
RACK_POWER_CLUSTER="unspecified"
RACK_POWER_HOST = "121.78.236.134"
RACK_POWER_RRD = "rack_-dev-ttyUSB"

SERVER_POWER_CLUSTER="unspecified"
SERVER_POWER_HOST = "121.78.236.134"
SERVER_POWER_RRD = "power"

TEMPERATURE_CLUSTER="unspecified"
TEMPERATURE_HOST = "121.78.236.134"
TEMPERATURE_RRD = "temp"

EXCLUDE_DATA_SOURCE = ["boottime"]

EVENT_LINE_COLOR = "red"

CPU_THRESHOLD = 70
DISK_THRESHOLD = 10
MEMORY_THRESHOLD = 10

#for Dashboard
METRIC_CPU = "cpu_system.rrd"
METRIC_MEMORY = "mem_total.rrd"
METRIC_DISK = "disk_total.rrd"
METRIC_NETWORK_IN ="bytes_in.rrd"
METRIC_NETWORK_OUT ="bytes_out.rrd"
METRIC_WORKLOAD ="load_fifteen.rrd"

DEFAULT_GRID_NAME = "None"

SERVER_ALIVE_THRESHOLD = 300

