import platform
import socket
import json
import yaml
import logging
import traceback
from messages import Messages

# Load config
with open("src/ethernet_interface/resource/config.yaml", "rt") as f:
    config = yaml.safe_load(f.read())
Platform = "Localhost"
if platform.release().endswith("tegra"):
    Platform = "Jetson"


# Connection settings for this server, from config
SERVER_IP = config["Network"][Platform]["TEST_SERVER_IP"]
SERVER_PORT = config["Network"][Platform]["TEST_SERVER_PORT"]
# Connection settings to ECU, from config
REMOTE_IP = config["Network"][Platform]["DV_IP"]
REMOTE_PORT = config["Network"][Platform]["DV_PORT"]

mock_data = []
pedal: Messages.ECU.Pedal = Messages.ECU.Pedal(
    throttleLeft=int(3),
    throttleRight=int(3),
    brakeFront=int(3),
    brakeBack=str(3),
)
ping_msg: Messages.Dv.Ping = Messages.Dv.Ping(ping="ping")

hvcb: Messages.ECU.HVCB = Messages.ECU.HVCB(LVAccu=3, V24=4, V12=5, LVShutdown=False)


pedal_to_string = pedal.get()
ping_to_string = ping_msg.get()
hvcb = hvcb.get()
mock_data.append(pedal_to_string)
mock_data.append(ping_to_string)
mock_data.append(hvcb)


class Server:

    def __init__(self):
        logging.basicConfig(format="%(levelname)s:  %(message)s", level=logging.DEBUG)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((SERVER_IP, SERVER_PORT))
        logging.info("Server is running on {}:{}".format(SERVER_IP, SERVER_PORT))

    def start(self):
        self.send_data(json.dumps([{"bn": "Test server is up"}]))
        logging.debug("start receiving")

        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                data = data.decode("utf-8")
                logging.debug(
                    "Received from {}:{} -> {}".format(addr[0], addr[1], data)
                )
                self.return_message(data, mock_data)
            except KeyboardInterrupt:
                if self.socket:
                    self.socket.close()
                break

    def return_message(self, data, mock_data):
        data_list_dict = json.loads(data)
        for element in data_list_dict:
            if element["v"] == "request":
                # send back the requested messages
                for mock in mock_data:
                    mock_data_dicts = json.loads(mock)
                    for dic in mock_data_dicts:
                        if dic.get("bn") == element["bn"]:
                            self.send_data(json.dumps(mock_data_dicts))
                            break
                        else:
                            # TODO: make the print to a pretty log:  logging.ERROR("ohoh %s not in mockdata", dic.get('bn'))
                            print("ohoh bn not in mock data, try again :/")
            else:
                # send back response message
                response = []
                response.append(
                    {"bn": element["bn"], "n": element["n"], "v": "response"}
                )
                self.send_data(json.dumps(response))

    def send_data(self, data) -> None:
        data = data.encode("utf-8")
        self.socket.sendto(data, (REMOTE_IP, REMOTE_PORT))
        logging.info("Sent to {}:{} -> {}".format(REMOTE_IP, REMOTE_PORT, data))

    def close(self):
        self.socket.close()


def main():
    server = Server()
    try:
        server.start()
    except Exception:
        traceback.print_exc()

    finally:
        server.close()


if __name__ == "__main__":
    main()
