#!/usr/bin/python
import sys
import usb.core
import usb.util
import time
import commands
from datetime import datetime
from subprocess import Popen, PIPE
import response


VENDOR_ID = '24e9'

def printToFile(log_message):
    f = open('log.txt', 'a')
    timestamp = '[' + str(datetime.now()) + ']'
    f.write(timestamp + ': ' + log_message + '\n')
    f.close()

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



def receive_data():
    response.print_dictionary(response.read_antenna(dev))
    response.print_dictionary(response.read_antenna(dev))
    time.sleep(1)
    response.print_dictionary(response.read_antenna(dev))
    response.print_dictionary(response.read_antenna(dev))
    response.print_dictionary(response.read_antenna(dev))
    print '-----------------------------------'





def initialization():
    print 'startin initialization'
    # cancel 0x50
    ep.write(bytearray(commands.cancel_operation))
    # get mac 0x67(x5)
    for item in commands.read_mac:
        ep.write(bytearray(item))
        receive_data()
    # get firmware 0x60
    ep.write(bytearray(commands.get_firmware))
    #response.print_dictionary(response.read_antenna(dev))
    receive_data()
    # get version 0x6c
    ep.write(bytearray(commands.get_version))
    receive_data()
    # get update_number 0x6d
    ep.write(bytearray(commands.get_upd_num))
    receive_data()
    # get bootloader 0x64
    ep.write(bytearray(commands.get_bootloader))
    receive_data()
    # get update_number 0x07
    ep.write(bytearray(commands.mac_registers))
    receive_data()
    printToFile('Initialization success')



# configure antenna
def antenna_configuration():
    ep.write(bytearray(commands.set_antenna_port_state))
    receive_data()

    ep.write(bytearray(commands.set_sense_threshold))
    receive_data()

    ep.write(bytearray(commands.set_antena_config))
    receive_data()

    printToFile('Antenna 1 configuration success')


def antenna_configuration_2():
    ep.write(bytearray(commands.set_antenna_port_state_2))
    receive_data()

    ep.write(bytearray(commands.set_sense_threshold_2))
    receive_data()

    ep.write(bytearray(commands.set_antena_config_2))
    receive_data()
    printToFile('Antenna 2 configuration success')


# # retrieve inventory 0x03
# ep.write(bytearray(commands.retrieve_inventory))
# response.print_dictionary(response.read_antenna(dev))

# set mode 0x02
def run_inventory():
    ep.write(bytearray(commands.set_mode))
    receive_data()

    # start inventory 0x40
    ep.write(bytearray(commands.tag_inventory))
    receive_data()
    receive_data()
    printToFile('Run Inventory success')


def starting_process():
    discover_reader()
    initialization()
    antenna_configuration()
    antenna_configuration_2()
    run_inventory()




starting_process()


# time.sleep(4)
# print '-------------------'
# print bytearray(commands.get_status)
# ep.write(bytearray(commands.get_status))
# response.print_dictionary(response.read_antenna(dev))
# print '_---------------------'

while 1:
    if response.read_antenna(dev) != None:
        pass
    else:
        if usb.core.find(idVendor=idVendor, idProduct=idProduct):
            print 'ok'
        else:
            printToFile('Error Lost Reader')
            time.sleep(5)
            starting_process()





# GPIO.cleanup()




# # release the device
# usb.util.release_interface(dev, interface)
# # reattach the device to the OS kernel
# dev.attach_kernel_driver(interface)
