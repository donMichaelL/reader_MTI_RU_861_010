#  operation = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd2, 0x0d ]

# operation = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xd2, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0xf7, 0x22]
# operation = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xdc, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0x7f, 0x10]
# operation = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xe6, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0xbc, 0xba]
operation = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0x0e, 0x01, 0xf4, 0x01, 0x00, 0x00, 0x00, 0xa0, 0x23]



def crc16(packet, bit_length):
    position = 0
    shift = 0xFFFF

    for i in range(0, bit_length):
        if i%8 == 0:
            data = packet[position] << 8
            position += 1
        val = shift ^ data
        shift = shift << 1
        shift = shift & 0xffff
        data = data  << 1
        data = data & 0xff00
        val = val & 0xff00
        if(val & 0x8000):
            shift = shift ^ 0x1021;
    return shift;

crc = crc16(operation, 14*8) ^ 0xffff
operation.append(crc & 0xFF)
operation.append( crc >> 8)

for num in operation:
    print hex(num)
