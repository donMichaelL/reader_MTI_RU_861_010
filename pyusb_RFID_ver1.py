#!/usr/bin/python
import sys
import usb.core
import usb.util
import time
import commands
import response
# decimal vendor and product values
dev = usb.core.find(idVendor=0x24e9, idProduct=0x0861)
interface = 0
endpoint = dev[0][(0,0)][1]
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

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


# configure antenna
def antenna_configuration():
    ep.write(bytearray(commands.set_antenna_port_state))
    response.print_dictionary(response.read_antenna(dev))

    ep.write(bytearray(commands.set_sense_threshold))
    response.print_dictionary(response.read_antenna(dev))

    ep.write(bytearray(commands.set_antena_config))
    response.print_dictionary(response.read_antenna(dev))

# # retrieve inventory 0x03
# ep.write(bytearray(commands.retrieve_inventory))
# response.print_dictionary(response.read_antenna(dev))

# set mode 0x02
def run_inventory():
    ep.write(bytearray(commands.set_mode))
    print bytearray(commands.set_mode)
    response.print_dictionary(response.read_antenna(dev))

    # start inventory 0x40
    ep.write(bytearray(commands.tag_inventory))
    response.print_dictionary(response.read_antenna(dev))
    response.print_dictionary(response.read_antenna(dev))

initialization()
antenna_configuration()
run_inventory()

while 1:
    if response.read_antenna(dev) != None:
        pass
    else:
        initialization()
        antenna_configuration()
        run_inventory()









# # release the device
# usb.util.release_interface(dev, interface)
# # reattach the device to the OS kernel
# dev.attach_kernel_driver(interface)
