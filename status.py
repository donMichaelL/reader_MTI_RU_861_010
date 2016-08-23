import time
import usb.core
import json
import paho.mqtt.publish as publish
from subprocess import Popen, PIPE


antenna_code = 0
VENDOR_ID = '24e9'

def get_antenna_code():
    global antenna_code
    if antenna_code == 0:
        file = open("antenna_code.txt")
        antenna_code = file.read().rstrip()
    return antenna_code

def findVendorProductId():
    p = Popen('lsusb', shell=True, stdout=PIPE)
    output, err = p.communicate()
    start_of_vendor_id = output.find(str(VENDOR_ID))
    if start_of_vendor_id != -1:
        idProductStr = output[start_of_vendor_id+5:start_of_vendor_id+9]
        idProduct = int('0x'+idProductStr, 16)
        idVentor = int('0x'+VENDOR_ID, 16)
        return (idVentor, idProduct)

while 1:
    try:
        try:
            idVendor, idProduct = findVendorProductId()
            usb.core.find(idVendor=idVendor, idProduct=idProduct)
            msg = json.dumps({'antenna': str(get_antenna_code()), 'status': 'connected'}, sort_keys=True, indent=4, separators=(',', ': '))
            print 'connected'
        except Exception as e:
            msg = json.dumps({'antenna': str(get_antenna_code()), 'status': 'not connected'}, sort_keys=True, indent=4, separators=(',', ': '))
            print 'not antenna'
        publish.single("status", msg , hostname="localhost", port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None)
    except Exception as e:
        print e, 'not connected'
    time.sleep(5)
