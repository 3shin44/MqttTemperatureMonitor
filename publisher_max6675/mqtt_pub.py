import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()


class MQTTClient:
    def __init__(self, broker=None, port=1883, topic=None):
        self.broker = broker or os.getenv("MQTT_BROKER", "localhost")
        self.port = port or int(os.getenv("MQTT_TOPIC", "1883"))
        self.topic = topic or os.getenv("MQTT_TOPIC", "sensor/data")
        self.client = mqtt.Client()
        self.client.connect(self.broker, self.port, 60)

    def publish(self, topic=None, payload=None, qos=0, retain=False):
        """
        發送訊息到 MQTT Broker
        :param topic: 要發送的主題
        :param payload: 要發送的訊息
        :param qos: 訊息的 QoS 等級
        :param retain: 是否保留訊息
        """
        topic = topic or self.topic
        self.client.publish(topic, payload, qos, retain)


if __name__ == "__main__":
    mqtt_client = MQTTClient()
    mqtt_client.publish(payload="Hello, MQTT!")
    print(f"📤 發送訊息到主題 {mqtt_client.topic}: Hello, MQTT!")  # 發送訊息
