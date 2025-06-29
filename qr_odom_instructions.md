# Installation:
* [ROS2](https://docs.ros.org/en/humble/Installation.html)
* [Livox SDK](https://github.com/Livox-SDK/Livox-SDK2/blob/master/README.md)
* [Livox ROS Node](https://github.com/Livox-SDK/livox_ros_driver2)
* [Direct Lidar Inertial Odometry (fork)](https://github.com/GoldenZephyr/direct_lidar_inertial_odometry)

# Running Lidar Odom

0. Launch the Livox Node:


1. Launch the odometry node:
```
ros2 launch direct_lidar_inertial_odometry dlio.launch.py rviz:=false pointcloud_topic:=/livox/lidar imu_topic:=/livox/imu
```
2. For testing, launch the standalone odom zmq subscriber:

```
python3 zmq_odom_sub.py
```

This is a very minimal script that will verify that the odometry is being published over the specified ZMQ socket.

3. To use the odometry in a real application, you can do something like this:
```python
interface = ZmqOdomInterface("tcp://localhost:5556")
interface.start()
for i in range(10):
    print(f"Printing odom {i}")
    pose = interface.get_current_pose()
    print(pose)
    time.sleep(1)
interface.stop()
```
