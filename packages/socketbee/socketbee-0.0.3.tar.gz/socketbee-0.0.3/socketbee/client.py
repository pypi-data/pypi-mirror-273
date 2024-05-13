import socketio
from time import sleep


class SocketBee:
    def __init__(self, app_id, app_key, options=None):
        if options is None:
            options = {}
        self.app_id = app_id
        self.app_key = app_key
        self.options = options
        self.app_secret = options.get('secret', None)
        self.sio = socketio.Client()

        self.server = options.get('server', 'east-1.socket.socketbee.com')
        self.port = options.get('port', 443)
        self.protocol = options.get('protocol', 'https')

        self.socket = None
        self.channel = None

        @self.sio.event
        def connect():
            print('Connected')

        @self.sio.event
        def disconnect():
            print('Disconnected')

        self.url = f"{self.protocol}://{self.server}:{self.port}/?client_events={self.options.get('client_events', 'false')}"

    def connect(self):
        self.sio.connect(self.url, namespaces=[f'/{self.app_id}'],
                         headers={'key': self.app_key, 'secret': self.app_secret}
                         )
        sleep(0.01)  # wait for connexion with the server to be fully established
        return self

    def broadcast(self, event_name, event_data, channel=None):
        self.channel = channel
        # Send the event
        event = {
            "channel": self.channel,
            "event": event_data
        }
        self.sio.emit(event_name, event, namespace=f'/{self.app_id}')

    def close(self):
        # Disconnect after sending the event
        self.sio.disconnect()
