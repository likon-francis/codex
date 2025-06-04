class MQTTClient:
    """Simple placeholder for an MQTT client."""
    def __init__(self):
        self.messages = []

    def connect(self, broker_url: str, port: int = 1883):
        print(f"Connecting to MQTT broker at {broker_url}:{port}")

    def publish(self, topic: str, payload: str):
        print(f"Publish to {topic}: {payload}")
        self.messages.append({"topic": topic, "payload": payload})

    def subscribe(self, topic: str):
        print(f"Subscribing to {topic}")

    def loop_start(self):
        print("MQTT loop started")
