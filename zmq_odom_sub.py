import zmq
from zmq_odom_msg import parse_odom_msg

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
    msg = parse_odom_msg(string)
    print(msg)
