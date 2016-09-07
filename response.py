import socket
import usb.core
import paho.mqtt.publish as publish
from datetime import datetime
import json
# Response
# Inverse Logic
# 4 Bytes --> HEADER --> Response from MTI (RITM) --> 0x52, 0x49, 0x54, 0x4d
# 1 Byte --> READER ID --> Broadcast --> 0xff
# 1 Byte --> COMMANDID --> Cancel Operation --> 0x50
# 8 Bytes --> COMMAND PARAMETERS --> 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
# 2 Bytes --> CHECKSUM
RESPONSE_HEADER =  ['0x52', '0x49', '0x54', '0x4d']
BEGIN_HEADER =  ['0x42', '0x49', '0x54', '0x4d']
INVENTORY_RESPONSE = ['0x49', '0x49', '0x54', '0x4d']


COMMAND_DICT = {
    '0x67': 'send_mac',
    '0x60': 'send_firmware',
    '0x6c': 'send_version',
    '0x6d': 'send_update_number_info',
    '0x64': 'send_bootloader_version',
    '0x7': 'send_mac_registers',
    '0x2': 'set_mode',
    '0x40': 'start_inventory',
    '0x1': 'packet discovery',
}

def header_analyser(res):
    header = res[0:4]
    if cmp(header, RESPONSE_HEADER) == 0:
        return 'RESPONSE_HEADER'
    elif cmp(header, BEGIN_HEADER) == 0:
        return 'BEGIN_HEADER'
    elif cmp(header, INVENTORY_RESPONSE) == 0:
        return 'INVENTORY_RESPONSE'
    else:
        return ''.join(res[0:4])

def command_analyzer(res):
    command = res[5:6][0]
    if command in COMMAND_DICT:
        return COMMAND_DICT[command]
    else:
        return command

def paramaters_analyzer(res):
    params = res[7:(len(res)-2)]
    if len(params)<6:
        return 'params'
    return params

antenna_code = 0
def get_antenna_code():
    global antenna_code
    if antenna_code == 0:
        file = open("antenna_code.txt")
        antenna_code = file.read().rstrip()
    return antenna_code

def analyzer(response):
    print 'ok'
    result = {}
    res = [hex(i) for i in response]
    # print len(res)
    result['header'] = header_analyser(res)
    result['command'] = command_analyzer(res)
    result['parameters'] = paramaters_analyzer(res)
    timestamp = datetime.now().time()
    # print 'header: ' + str(antenna_code)
    # print 'command: ' + result['command']
    if len(res)>50:
        print '-'.join(res[26:42])
        print 'Antenna: ' + str(antenna_code) #'-'.join(res[24:25])
        print 'Tag: '+ '-'.join(res[26:42])
        msg = json.dumps({'tag': '-'.join(res[26:42]), 'antenna': str(antenna_code) , 'timestamp': str(timestamp) }, sort_keys=True,indent=4, separators=(',', ': '))
        try:
            publish.single("input/" + get_antenna_code(), msg , hostname="localhost", port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None)
        except:
            pass
    else:
        pass
    print ''
    return result


def read_antenna(dev):
    endpoint = dev[0][(0,0)][1]
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        return analyzer(data)
    except usb.core.USBError as e:
        print e
    except Exception as e:
        print e
