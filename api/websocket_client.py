import websocket
import json
import threading
import ssl

class SystemairWebSocket:
    def __init__(self, access_token, on_message_callback):
        self.access_token = access_token
        self.on_message_callback = on_message_callback
        self.ws = None
        self.thread = None

    def on_message(self, ws, message):
        data = json.loads(message)
        self.on_message_callback(data)

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")

    def on_open(self, ws):
        print("WebSocket connection opened")

    def connect(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            f"wss://homesolutions.systemair.com/streaming/",
            header=[
                f"Sec-WebSocket-Protocol: accessToken, {self.access_token}",
                "Origin: https://homesolutions.systemair.com",
            ],
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.thread = threading.Thread(target=self.ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}})
        self.thread.daemon = True
        self.thread.start()

    def disconnect(self):
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()