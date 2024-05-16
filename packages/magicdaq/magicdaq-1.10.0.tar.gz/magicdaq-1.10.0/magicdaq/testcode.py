#*** Testing the Multi DAQ Changes Locally ***
import time

from api_class import MagicDAQDevice

daq_one = MagicDAQDevice()
daq_two = MagicDAQDevice()



list_of_all_connected_daqs = daq_one.list_all_daqs()
print('List of connected daqs: ', list_of_all_connected_daqs)

daq_one.open_daq_device(list_of_all_connected_daqs[0])
daq_two.open_daq_device(list_of_all_connected_daqs[1])

daq_one.set_analog_output(0, 2.7)
print('daq_two analog input 0 voltage: ', daq_two.read_analog_input(0))


print('daq_one serial number: ', daq_one.get_serial_number())
print('daq_two serial number: ', daq_two.get_serial_number())


daq_one.set_digital_output(0,1)
daq_two.set_digital_output(0,0)

# print('Pausing to check')
# time.sleep(120)

daq_one.close_daq_device()
daq_two.close_daq_device()

#time.sleep(60)


#
# print('Pausing before making next!')
# time.sleep(10)
# print('Making next MagicDAQ object!')
# #daq_two = MagicDAQClient64Bit()
# print('ALL OBJECTS NOW MADE')
#
# time.sleep(30)


# object_build_complete_time = time.time()
#
# print('Time to create DAQ code object: ', object_build_complete_time - object_build_start_time)
#
# daq_one.open_daq_device()
#
# print('This is serial number: ', daq_one.get_serial_number())
#
# serial_num_complete_time = time.time()
#
# print('Time to open daq and get serial number: ', serial_num_complete_time - object_build_complete_time)

#daq_one.close_daq_device()
