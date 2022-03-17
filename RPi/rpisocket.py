import json
import os
import websocket
import time
import socket


class RPiSocket:
    URL = "ws://192.168.10.12:4000"

    def __init__(self, queue: list) -> None:
        self.queue = queue
        self.connect = True  # maybe change state
        self.METHODS = {
            "turnLeft": turnLeft,
            "turnRight": turnRight,
            "goForward": goForward,
            "goBackward": goBackward,
            "terminate": terminate,
            "initiate": initiate,
        }

        def turnLeft():
            self.queue.append(
                {
                    "command": "turnLeft",
                    "time": 1,  # sec
                    # etc...
                }
            )

        def turnRight():
            self.queue.append(
                {
                    "command": "turnRight",
                    "time": 1,  # sec
                    # etc...
                }
            )

        def goForward():
            self.queue.append(
                {
                    "command": "goForward",
                    "time": 1,  # sec
                    # etc...
                }
            )

        def goBackward():
            self.queue.append(
                {
                    "command": "goBackward",
                    "time": 1,  # sec
                    # etc...
                }
            )

        def terminate():
            self.queue.append(
                {
                    "command": "terminate",
                    # etc...
                }
            )
            self.connect = False

        def initiate():
            self.queue.append(
                {
                    "command": "initiate",
                    # etc...
                }
            )

    def start(self):
        while self.connect:
            try:
                ws = websocket.WebSocketApp(
                    self.URL, on_message=self.on_message, on_open=self.on_open
                )
            except websocket.WebSocketException:
                print(f"[Error] Failed connecting to {self.URL}, trying again...")
            time.sleep(3)

    def on_message(self, ws, message):
        cmd, payload = self.parseServerData(message)
        if cmd in list(self.METHODS.keys()):
            self.METHODS[cmd](payload)
            print(f"[Connect] {cmd} is executed successfully")
        else:
            print(
                f"[Error] {cmd} doesn't belongs to current exist methods {list(self.METHODS.keys())}"
            )

    def parseServerData(self, message: str):
        print(f"[Connect] Message from server: {message}")
        try:
            message = json.loads(message)
            cmd = message["command"]
            payload = message["payload"]
            return cmd, payload
        except json.JSONDecodeError:
            print(f"[Error] Invalid json format: {message}")

    def on_open(self, ws):
        print(f"[Connect] {os.name} successfully connect to server")
        ws.send(
            json.dumps(
                {
                    "command": "boardInfo",
                    "payload": {
                        "type" "name": os.name,
                        "ip": socket.gethostbyname(socket.gethostname()),
                    },
                }
            )
        )

    # def on_close
    # def on_error


# example usage
if __name__ == "__main__":
    eventQueue = []
    rpiSocket = RPiSocket(eventQueue)
    rpiSocket.start()
