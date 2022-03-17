import json
import os
import websocket
import time
import socket


class JetsonSocket:
    URL = "ws://192.168.10.12:4000"

    def __init__(self, mes2crtl: list, mesfromcrtl: list) -> None:
        self.mes2crtl = mes2crtl
        self.mesfromcrtl = mesfromcrtl
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
            self.mes2crtl.append(
                {
                    "command": "turnLeft",
                    "time": 1,  # sec
                    # etc...
                }
            )

        def turnRight():
            self.mes2crtl.append(
                {
                    "command": "turnRight",
                    "time": 1,  # sec
                    # etc...
                }
            )

        def goForward():
            self.mes2crtl.append(
                {
                    "command": "goForward",
                    "time": 1,  # sec
                    # etc...
                }
            )

        def goBackward():
            self.mes2crtl.append(
                {
                    "command": "goBackward",
                    "time": 1,  # sec
                    # etc...
                }
            )

        def terminate():
            self.mes2crtl.append(
                {
                    "command": "terminate",
                    # etc...
                }
            )
            self.connect = False

        def initiate():
            self.mes2crtl.append(
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
                ws.run_forever()
            except websocket.WebSocketException:
                print(f"[Error] Failed connecting to {self.URL}, trying again...")
            time.sleep(3)

    def on_message(self, ws, message):
        cmd, payload = self.parseServerData(message)
        if cmd in list(self.METHODS.keys()):
            self.METHODS[cmd](payload)
            print(f"[Connect] {cmd} is executed successfully")
            # TODO: add response
            # if len(self.mesfromcrtl) > 0:
            #     self.send2Server(ws, self.mesfromcrtl.get_front())
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
        self.send2Server(
            ws,
            {
                "command": "boardInfo",
                "payload": {
                    "type" "name": os.name,
                    "ip": socket.gethostbyname(socket.gethostname()),
                },
            },
        )

    def send2Server(self, ws, mes):
        ws.send(json.dumps(mes))

    # def on_close
    # def on_error


# example usage
if __name__ == "__main__":
    # socket puts message to this buffer, controller gets message from this buffer
    # TODO: format alignment
    mes2control = []
    # socket gets message from this buffer, controller puts message to this buffer
    # TODO: format alignment
    mesfromcontrol = []
    jetsonSocket = JetsonSocket(mes2crtl=mes2control, mesfromcrtl=mesfromcontrol)
    jetsonSocket.start()
