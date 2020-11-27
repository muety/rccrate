import paho.mqtt.client as mqtt

from .handlers.simple import SimpleCachingHandler

TOPIC_CONTROL_LON = 'rccrate/control/throttle'
TOPIC_CONTROL_LAT = 'rccrate/control/steering'

class Bridge:
    def __init__(self, host='localhost', port=1883):
        self.client = mqtt.Client()

        self.host = host
        self.port = port

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        self.handlers = {
            'control/throttle': SimpleCachingHandler(0, lambda m: int(m)),
            'control/steering': SimpleCachingHandler(0, lambda m: int(m))
        }

    def __del__(self):
        self.client.disconnect()

    def connect(self):
        print('MQTT connecting')
        self.client.connect(self.host, self.port, 10)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def get_handler(self, name):
        return self.handlers[name]

    def _on_connect(self, client, userdata, flags, rc):
        print('MQTT connected')
        
        self.client.subscribe(TOPIC_CONTROL_LON, 0)
        self.client.subscribe(TOPIC_CONTROL_LAT, 0)

        self.client.message_callback_add(TOPIC_CONTROL_LON, self._dispatch_handler(self.handlers['control/throttle']))
        self.client.message_callback_add(TOPIC_CONTROL_LAT, self._dispatch_handler(self.handlers['control/steering']))

    def _on_disconnect(self, client, userdata, rc):
        print('MQTT disconnected')

    def _on_message(self, client, userdata, message):
        print(f'(Got unhandled message at topic "{message.topic}")')

    def _dispatch_handler(self, handler):
        def handle(client, userdata, message):
            handler.handle(message.payload)
        return handle