#!/usr/bin/python
import sys
import usb.core
import usb.util
import time
import commands
from datetime import datetime
from subprocess import Popen, PIPE

import response
import RPi.GPIO as GPIO ## Import GPIO library


VENDOR_ID = '24e9'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, True)
time.sleep(5)
GPIO.output(7, False)


f = open('log.txt', 'w')

def printToFile(log_message):
    timestamp = '[' + str(datetime.now()) + ']'
    f.write(timestamp + ': ' + log_message + '\n')

def findVendorProductId():
    p = Popen('lsusb', shell=True, stdout=PIPE)
    output, err = p.communicate()
    start_of_vendor_id = output.find(str(VENDOR_ID))
    if start_of_vendor_id != -1:
        idProductStr = output[start_of_vendor_id+5:start_of_vendor_id+9]
        printToFile('Reader Found with Product Id ' + idProductStr)
        idProduct = int('0x'+idProductStr, 16)
        idVentor = int('0x'+VENDOR_ID, 16)
        return (idVentor, idProduct)
    printToFile('Reader Not Found')

# Connect With Reader
def discover_reader():
    found_reader = False
    while not found_reader:
        global dev, idVendor, idProduct
        try:
            idVendor, idProduct = findVendorProductId()
            dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
            interface = 0
            endpoint = dev[0][(0,0)][1]
            cfg = dev.get_active_configuration()
            intf = cfg[(0,0)]
            found_reader = True
            global ep
            ep = usb.util.find_descriptor(
                intf,
                # match the first OUT endpoint
                custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT)
            assert ep is not None
        except  Exception, err:
            printToFile('Exception in discover_reader ' + str(err))
            time.sleep(5)
            pass


def initialization():
    # cancel 0x50
    ep.write(bytearray(commands.cancel_operation))
    # get mac 0x67(x5)
    for item in commands.read_mac:
        ep.write(bytearray(item))
        response.print_dictionary(response.read_antenna(dev))
    # get firmware 0x60
    ep.write(bytearray(commands.get_firmware))
    response.print_dictionary(response.read_antenna(dev))
    # get version 0x6c
    ep.write(bytearray(commands.get_version))
    response.print_dictionary(response.read_antenna(dev))
    # get update_number 0x6d
    ep.write(bytearray(commands.get_upd_num))
    response.print_dictionary(response.read_antenna(dev))
    # get bootloader 0x64
    ep.write(bytearray(commands.get_bootloader))
    response.print_dictionary(response.read_antenna(dev))
    # get update_number 0x07
    ep.write(bytearray(commands.mac_registers))
    response.print_dictionary(response.read_antenna(dev))
    printToFile('Initialization success')



# configure antenna
def antenna_configuration():

    ep.write(bytearray(commands.set_antenna_port_state))
    response.print_dictionary(response.read_antenna(dev))

    ep.write(bytearray(commands.set_sense_threshold))
    response.print_dictionary(response.read_antenna(dev))

    ep.write(bytearray(commands.set_antena_config))
    response.print_dictionary(response.read_antenna(dev))
    printToFile('Antenna 1 configuration success')


def antenna_configuration_2():
    ep.write(bytearray(commands.set_antenna_port_state_2))
    response.print_dictionary(response.read_antenna(dev))

    ep.write(bytearray(commands.set_sense_threshold_2))
    response.print_dictionary(response.read_antenna(dev))

    ep.write(bytearray(commands.set_antena_config_2))
    response.print_dictionary(response.read_antenna(dev))
    printToFile('Antenna 2 configuration success')


# # retrieve inventory 0x03
# ep.write(bytearray(commands.retrieve_inventory))
# response.print_dictionary(response.read_antenna(dev))

# set mode 0x02
def run_inventory():
    print 'intentory'
    ep.write(bytearray(commands.set_mode))
    print bytearray(commands.set_mode)
    response.print_dictionary(response.read_antenna(dev))

    # start inventory 0x40
    ep.write(bytearray(commands.tag_inventory))
    response.print_dictionary(response.read_antenna(dev))
    response.print_dictionary(response.read_antenna(dev))
    printToFile('Run Inventory success')


discover_reader()
initialization()
antenna_configuration()
antenna_configuration_2()
run_inventory()



while 1:
    if response.read_antenna(dev) != None:
        pass
    else:
        if usb.core.find(idVendor=idVendor, idProduct=idProduct):
            print 'ok'
        else:
            printToFile('Error Lost Reader')
            time.sleep(5)
            GPIO.output(7, False)
            discover_reader()
            initialization()
            antenna_configuration()
            antenna_configuration_2()
            run_inventory()





GPIO.cleanup()




# # release the device
# usb.util.release_interface(dev, interface)
# # reattach the device to the OS kernel
# dev.attach_kernel_driver(interface)
