import osi3.osi_sensorview_pb2
import osi3.osi_sensordata_pb2
import osi3.osi_detectedobject_pb2

# create SensorView
sensorView = osi3.osi_sensorview_pb2.SensorView()
# feed SensorView with information
car1 = sensorView.global_ground_truth.moving_object.add()
car1.base.dimension.height = 2.0
car1.base.dimension.length = 3.5
car1.base.dimension.width = 1.8
v_x = 5 # Velocity in x in m/s
car1.base.velocity.x = v_x
car1.base.position.x = 0
car1.base.position.y = 3
car1.base.position.z = 0
car1.id.value = 0
car1.type = car1.TYPE_VEHICLE
car1.vehicle_classification.type = car1.vehicle_classification.TYPE_COMPACT_CAR

sensorView.generic_sensor_view.add()
sensorView.generic_sensor_view._values[0].view_configuration.sensor_id.value = 0
sensorView.generic_sensor_view._values[0].view_configuration.mounting_position.position.x = 1
sensorView.generic_sensor_view._values[0].view_configuration.mounting_position.position.y = 0.5
sensorView.generic_sensor_view._values[0].view_configuration.mounting_position.position.z = 0.2


# tree = sensorView.global_ground_truth.stationary_object.add()
tree= osi3.osi_detectedobject_pb2.DetectedStationaryObject()
tree.base.dimension.height = 4
tree.base.dimension.width = 3
tree.base.dimension.length = 4
tree.base.position.x = 2
tree.base.position.y = 5
tree.base.position.z = 0

tree.header.ground_truth_id.add()
tree.header.ground_truth_id._values[0].value=1

tree.candidate.add()
tree.candidate._values[0].probability= 0.4
tree.candidate._values[0].classification.type= 0
# tree.candidate._values[0].classification.type= "TYPE_BUILDING"
tree.candidate.add()
tree.candidate._values[1].probability= 0.6
tree.candidate._values[1].classification.type= 3
#tree.id = 1


# Create SensorData
sensorData = osi3.osi_sensordata_pb2.SensorData()
sensorData.sensor_view.add() # required to use CopyFrom later
sensorData.stationary_object.add()
sensorData.stationary_object._values[0].base.CopyFrom(tree.base)
sensorData.stationary_object._values[0].header.CopyFrom(tree.header)
sensorData.stationary_object._values[0].candidate.add()
sensorData.stationary_object._values[0].candidate.add()
sensorData.stationary_object._values[0].candidate._values[0].CopyFrom(tree.candidate._values[0])
sensorData.stationary_object._values[0].candidate._values[1].CopyFrom(tree.candidate._values[1])

sensorData.mounting_position.CopyFrom(sensorView.generic_sensor_view._values[0].view_configuration.mounting_position)
sensorData.occupant.add()
sensorData.occupant._values[0].header.ground_truth_id.add()
sensorData.occupant._values[0].header.ground_truth_id._values[0].value = 0
#occ.header.ground_truth_id._values[0] = 1
#sensorData.occupant._values[0]

# Save SensorView
f = open("SensorView2.txt", "wb")
f_data = open("SensorData2.txt", "wb")
for i in range(10):
    # SView
    sensorView.timestamp.seconds = i
    sensorView.global_ground_truth.timestamp.seconds = i
    # SData
    sensorData.timestamp.seconds = i

    for j in range(10):
        sensorView.timestamp.nanos = j * 100000000
        sensorView.global_ground_truth.timestamp.nanos = j * 100000000
        sensorView.global_ground_truth.moving_object._values[0].base.position.x = v_x * i + v_x / 10 * j
        sensorView.host_vehicle_data.location.CopyFrom(sensorView.global_ground_truth.moving_object._values[0].base)
        #print(sensorView)
        proto_bytes = sensorView.SerializeToString()
        f.write(proto_bytes + b"$$__$$")

        # SensorData
        sensorData.timestamp.nanos = j * 100000000
        sensorData.sensor_view._values[0].CopyFrom(sensorView)
        sensorData.host_vehicle_location.CopyFrom(sensorView.global_ground_truth.moving_object._values[0].base)
        #sensorData.stationary_object_header.DataQualifier.DATA_QUALIFIER_AVAILABLE
        print(sensorData)
        proto_bytes_data = sensorData.SerializeToString()
        f_data.write(proto_bytes_data + b"$$__$$")
f.close()
f_data.close()

