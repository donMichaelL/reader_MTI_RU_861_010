# Commands
# Inverse Logic
# 4 Bytes --> HEADER --> Command from MTI (CITM) --> 0x43, 0x49, 0x54, 0x4d
# 1 Byte --> READER ID --> Broadcast --> 0xff
# 1 Byte --> COMMANDID --> Cancel Operation --> 0x50
# 8 Bytes --> COMMAND PARAMETERS --> 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
# 2 Bytes --> CHECKSUM


#--------------------------------------------- BEFORE INVENTORY ---------------------------------------------------

# 0x50 --> Cancel Operation
cancel_operation = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd2, 0x0d ]
# 0x67 --> Read Mac in 5 Messages
# read the first part 0x5f
read_mac_first   = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x67, 0x5f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xdd, 0x5a ]
# read the second part 0x60
read_mac_second  = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x67, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc3, 0xc5 ]
# read the third part 0x61
read_mac_third   = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x67, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x82 ]
# read the fourth part 0x62
read_mac_fourth  = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x67, 0x62, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x65, 0x4a ]
# read the fifth part 0x63
read_mac_fifth   = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x67, 0x63, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xb6, 0x0d ]
read_mac = [read_mac_first, read_mac_second, read_mac_third, read_mac_fourth, read_mac_fifth ]

# 0x60 --> Retrieving the MAC Firmware Version Information
get_firmware     = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd0, 0xf9 ]

# 0x6c --> Retrieving the MAC-Resident OEMCfg Version Information
get_version     = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x6c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x4c ]

# 0x6d --> Retrieving the MAC-Resident OEMCfg Update Number Information
get_upd_num     = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x6d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe3, 0xa7 ]

# 0x64 -->Retrieving the Boot-loader Firmware Version Information
get_bootloader  = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x65 ]

# 0x07 --> Retrieving Low-Level MAC Registers
mac_registers   = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x07, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0x3f ]

#--------------------------------------------- BEFORE INVENTORY ---------------------------------------------------

#--------------------------------------------- SETTING PORT 0 CONFIGURATION ---------------------------------------------------

# 0x10 --> Setting antenna port state enable/disable
set_antenna_port_state = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x10, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6a, 0xea ]

# 0x14 --> Setting global antenna sense threshold
set_sense_threshold = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x14, 0xff, 0xff, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd9, 0x3a ]

# 0x12 --> Setting antenna port configurationd SPECIFY dbs, dwell time,
# 20db
# set_antena_config = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0xc8, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x00, 0x30, 0xb1 ]

# 21db
# set_antena_config = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0xd2, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x00, 0x50 , 0x75]

# 22db
# set_antena_config = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0xdc, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x00, 0x8d, 0x47]

# 23db
# set_antena_config = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0xe6, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x00, 0x4e, 0xed]

# 24db
set_antena_config = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0xf0, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x00, 0x10, 0x7b]

# 25db
#set_antena_config = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0xfa, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x00, 0x5e, 0x88]

#27db
#set_antena_config = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0x0e, 0x01, 0xf4, 0x01, 0x00, 0x00, 0x00, 0xa0, 0x23]

# 30db
# set_antena_config = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x00, 0x2c, 0x01, 0xf4, 0x01, 0x00, 0x00, 0x00, 0xb5, 0x2d  ]


#---------------------------------------------  END SETTING PORT CONFIGURATION ---------------------------------------------------

#--------------------------------------------- SETTING PORT 1 CONFIGURATION ---------------------------------------------------
# 0x10 --> Setting antenna port state enable/disable
set_antenna_port_state_2   = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x10, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xb9, 0xad]

# 0x14 --> Setting global antenna sense threshold
set_sense_threshold_2   = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x14, 0xff, 0xff, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd9, 0x3a]

#20db
# set_antena_config_2 = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xc8, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0xc2, 0xe6]

# 21db
# set_antena_config_2 = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xd2, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0xf7, 0x22]

# 22db
# set_antena_config_2 = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xdc, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0x7f, 0x10]

# 23db
set_antena_config_2 =  [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xe6, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0xbc, 0xba]

# 24db
# set_antena_config_2 = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xf0, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0xe2, 0x2c]

#25db
#set_antena_config_2 = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0xfa, 0x00, 0xf4, 0x01, 0x00, 0x00, 0x01, 0xac, 0xdf]

# 27db
# set_antena_config_2 = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0x0e, 0x01, 0xf4, 0x01, 0x00, 0x00, 0x01, 0x52, 0x74]

# 30db
# set_antena_config_2 = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x12, 0x01, 0x2c, 0x01, 0xf4, 0x01, 0x00, 0x00, 0x01 , 0x47, 0x7a]

#---------------------------------------------  END SETTING PORT CONFIGURATION ---------------------------------------------------

#---------------------------------------------  INVENTORY ONCE OR Continious ---------------------------------------------------

# 0x03 --> Retrieve configuration
retrieve_inventory =  [0x43, 0x49, 0x54, 0x4d, 0xff, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xb1, 0x2c]

# 0x02 --> Setting the Operation Mode 0xff 0x02  0x0(0:Continious or 1:non-Continuous)
set_mode        =     [0x43, 0x49, 0x54, 0x4d, 0xff, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x92, 0xc7]

# 0x40 --> Tag Inventory Operation
tag_inventory   = [0x43, 0x49, 0x54, 0x4d, 0xff, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2c, 0x5e ]


get_status     =  [0x43, 0x49, 0x54, 0x4d, 0xff, 0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfb, 0xfe]
