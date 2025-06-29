import zmq

#zmq_odom_publisher_.bind("tcp://*:5556");

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

addr = "tcp://localhost:5556"
print(f"Connecting to {addr}")
socket.connect(addr)
socket.setsockopt_string(zmq.SUBSCRIBE, "")
print("Connected!")

# Process 100 updates
total_temp = 0
for update_nbr in range(100):
    string = socket.recv_string()
    x, y, z = string.split()
    print(f"update {update_nbr}")
    print(f"{x=}, {y=}, {z=}")


