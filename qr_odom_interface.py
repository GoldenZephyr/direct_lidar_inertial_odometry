from zmq_odom_msg import parse_odom_msg
import abc
import zmq
import time
import threading
import numpy as np


class OdomInterface(abc.ABC):
    def get_current_pose(self):
        pass


class ZmqOdomInterface(OdomInterface):
    def __init__(self, odom_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        print(f"Connecting to {odom_address}")
        self.socket.connect(odom_address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket.setsockopt(zmq.CONFLATE, 1)
        print("Connected!")

        self.msg_lock = threading.Lock()
        self.last_odom_msg = None

        self.running = False
        self.background_thread = None

    def get_current_pose(self):
        with self.msg_lock:
            if self.last_odom_msg is None:
                return None
            # TODO: presumably return some sort of QR type here?
            msg = self.last_odom_msg
            return np.array([msg.x, msg.y, msg.z, msg.qx, msg.qy, msg.qz, msg.qw])

    def start(self):
        if self.running:
            raise Exception("Already running. Cannot begin again!")
        self.running = True
        self.background_thread = threading.Thread(target=self.run_background)
        self.background_thread.start()

    def stop(self):
        if not self.running:
            print("Already stopped. Nothing to do.")
            return

        self.running = False
        self.background_thread.join()
        self.background_thread = None

    def run_background(self):
        while self.running:
            self.update_odom()
            time.sleep(0.001)

    def update_odom(self):
        string = self.socket.recv_string()
        msg = parse_odom_msg(string)
        with self.msg_lock:
            self.last_odom_msg = msg


if __name__ == "__main__":
    odom = ZmqOdomInterface("tcp://localhost:5556")
    odom.start()
    for i in range(10):
        print(f"Printing odom {i}")
        pose = odom.get_current_pose()
        print(pose)
        time.sleep(1)
    odom.stop()
