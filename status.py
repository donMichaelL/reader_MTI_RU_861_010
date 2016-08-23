import time
import json
import paho.mqtt.publish as publish

antenna_code = 0
def get_antenna_code():
    global antenna_code
    if antenna_code == 0:
        file = open("antenna_code.txt")
        antenna_code = file.read().rstrip()
    return antenna_code


while 1:
    try:
        print 'ok'
        msg = json.dumps({'antenna': str(get_antenna_code())}, sort_keys=True,indent=4, separators=(',', ': '))
        publish.single("input/" + get_antenna_code(), "Hello" , hostname="localhost", port=1883, client_id="",
        keepalive=60, will=None, auth=None, tls=None)
        print 'connected'
    except Exception as e:
        print e, 'not connected'
    time.sleep(5)
