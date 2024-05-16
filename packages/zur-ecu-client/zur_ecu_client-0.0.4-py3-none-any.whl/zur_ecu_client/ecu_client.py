import json
import traceback
import yaml
import platform
import socket
import sched
import time
from threading import Thread

from messages import Messages
from zur_ecu_client.senml.senml_pack import SenmlPack


class EcuClient:

    def __init__(self, logger, listener, messages) -> None:
        self.listener = listener or (lambda _1, _2: None)
        self.logger = logger
        self.messages = messages
        self.addr = None

        # Load the config file
        with open("src/ethernet_interface/resource/config.yaml", "rt") as f:
            config = yaml.safe_load(f.read())
        # which platform the file is executes to switch ip and port
        environment = "Localhost"
        if platform.release().endswith("tegra"):
            environment = "Jetson"
        # Set values from config file
        self.ECU_IP: str = config["Network"][environment]["ECU_IP"]
        self.ECU_PORT: int = config["Network"][environment]["ECU_PORT"]
        self.CLIENT_IP: str = config["Network"][environment]["DV_IP"]
        self.CLIENT_PORT: str = config["Network"][environment]["DV_PORT"]

        # Establish a udp socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.CLIENT_IP, self.CLIENT_PORT))

        self.thread1 = Thread(target=self.__listening_to_server)
        self.thread2 = Thread(target=self.send)
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def add_messages(self, baseName):
        self.messages.append(baseName)

    def remove_messages(self, baseName):
        if baseName in self.messages:
            self.messages.remove(baseName)

    def __listening_to_server(self):
        while True:
            rx_data: bytes
            self.addr: str
            rx_data, self.addr = self.socket.recvfrom(1024)
            if rx_data:
                data = rx_data.decode("utf-8")
                self.logger.info(
                    f"Received from {self.addr[0]}:{self.addr[1]} -> {data}"
                )
                try:
                    pack_gateway: SenmlPack = SenmlPack(
                        "gateway_name",
                        self.gateway_callback,  # gateway_name is pack name
                    )
                    pack_gateway.from_json(data)
                except:
                    print("ohoh exception")
                    traceback.print_exc()

                # date an listener übergeh

    def gateway_callback(self, record, **kwargs):

        print("found record: " + record.name)
        print("with value: " + str(record.value))
        self.listener(record, self.addr)

    def send_config(self, cfg: Messages.Dv.Cfg):
        msg = cfg
        self.__send_msg(msg)

    def send_control(self, ctrl: Messages.Dv.Ctrl):
        msg = ctrl
        self.__send_msg(msg)

    def send_statistic(self, stat: Messages.Dv.Stat):
        msg = stat
        self.__send_msg(msg)

    def send_acceleration(self, acc: Messages.Dv.Acc):
        msg = acc
        self.__send_msg(msg)

    def __send_msg(self, msg):
        msg = json.dumps(msg).encode("utf-8")
        self.socket.sendto(msg, (self.ECU_IP, self.ECU_PORT))
        self.logger.info(f"Sent to {self.ECU_IP}:{self.ECU_PORT} -> {msg}")

    def __request_messages(self):
        bn_request = []
        for elm in self.messages:
            bn_request.append(
                {"bn": elm, "n": "sensor", "v": "request"}
            )  # TODO: make the name dynamic
        self.__send_msg(bn_request)

    def add_request(self, data):
        pass

    def start(self):
        self.thread1.daemon = True
        self.thread2.daemon = True
        self.thread1.start()
        self.thread2.start()

    def send(self):
        while True:
            self.scheduler.enter(1, 1, self.__request_messages, ())
            self.scheduler.run()

    def close(self):
        self.socket.close()

    def __exit__(self):
        self.close()
