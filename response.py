import socket
import datetime
import usb.core
import paho.mqtt.publish as publish
# Response
# Inverse Logic
# 4 Bytes --> HEADER --> Response from MTI (RITM) --> 0x52, 0x49, 0x54, 0x4d
# 1 Byte --> READER ID --> Broadcast --> 0xff
# 1 Byte --> COMMANDID --> Cancel Operation --> 0x50
# 8 Bytes --> COMMAND PARAMETERS --> 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
# 2 Bytes --> CHECKSUM
DEFAULT_HEADER =  ['0x52', '0x49', '0x54', '0x4d']
BEGIN_HEADER =  ['0x42', '0x49', '0x54', '0x4d']
RESPONSE = ['0x49', '0x49', '0x54', '0x4d']

def find_last_ip_digit():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    ip = s.getsockname()[0]
    return ip.split('.')[-1]

ANTENNA = find_last_ip_digit()

COMMAND_DICT = {
    '0x67': 'send_mac',
    '0x60': 'send_firmware',
    '0x6c': 'send_version',
    '0x6d': 'send_update_number_info',
    '0x64': 'send_bootloader_version',
    '0x7': 'send_mac_registers',
    '0x2': 'set_mode',
    '0x40': 'start_inventory',
    '0x1': 'packet',
}

RFID = ['0x30', '0x0', '0x3', '0x0', '0x12', '0x75', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x15', '0xdc', '0xad']

def header_analyser(res):
    header = res[0:4]
    if cmp(header, DEFAULT_HEADER) == 0:
        return 'DEFAULT_HEADER'
    elif cmp(header, BEGIN_HEADER) == 0:
        return 'BEGIN_HEADER'
    elif cmp(header, RESPONSE) == 0:
        return 'RESPONSE'
    else:
        return res[0:4]

def command_analyzer(res):
    command = res[5:6][0]
    if command in COMMAND_DICT:
        return COMMAND_DICT[command]
    else:
        return command

def paramaters_analyzer(res):
    params = res[7:(len(res)-2)]
    print len(params)
    if len(params)<6:
        return 'params'
    return params#[19:35]


def analyzer(response):
    result = {}
    res = [hex(i) for i in response]
    # print res
    result['header'] = header_analyser(res)
    result['command'] = command_analyzer(res)
    result['parameters'] = paramaters_analyzer(res)
    if cmp(result['parameters'], RFID) == 0:
        i = 10
        # publish.single("airsoul", "%s This is a new Message" %(i), hostname="localhost",
    	# port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None)
    timestamp = datetime.datetime.now()
    #print 'Tag: ' + '-'.join(result['parameters']) + ' Antenna: ' + ANTENNA + ' ' + str(timestamp)
    print '-'.join(result['header']) + '-'.join(result['command']) + '-'.join(result['parameters'])
    # with open("log.txt", "a") as fo:
    #     fo.write('\nTag: ' + '-'.join(result['parameters']) + ' Antenna: ' + ANTENNA + ' ' + str(timestamp))
    return result


def read_antenna(dev):
    endpoint = dev[0][(0,0)][1]
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        return analyzer(data)
    except usb.core.USBError as e:
        data = None


def _print_dictionary(dictionary):
    # try :
    #     for key, value in dictionary.items():
    #         print key + ': '+ value,
    #     print '-------------'
    # except:
    #     pass
    pass

def print_dictionary(data):
    pass
    # print "________________________________________________________________________"
    # # print data
    # print "________________________________________________________________________"
