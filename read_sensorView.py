import sys
import os
from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_sensordata_pb2 import SensorData
import struct

def main():

    args = sys.argv
    calling_script = os.path.abspath(args[0])
    exe_dir = os.path.dirname(calling_script)
    fileDir=exe_dir+"\\"+"example_sensor_view.txt"

    """Initialize SensorView and SensorData"""
    sensorview = SensorView()
    sensordata = SensorData()

    """Clear SensorData"""
    sensordata.Clear()

    
    st = open(fileDir,"rb").read()
    """The received string buffer can now be parsed"""

    sensorview.ParseFromString(st)
    sensordata.ParseFromString(st)

    f = open("test_trace001.osi", "ab")
    bytes_buffer = sensorview.SerializeToString()
    f.write(struct.pack("<L", len(bytes_buffer)) + bytes_buffer)
    f.close()
    #it actually parse only the first time stamp of the whole simulation
    """Print SensorView"""
    print(sensorview)

if __name__ == "__main__":
    main()