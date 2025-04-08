import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# 載入 .env 文件中的環境變數
load_dotenv()


class MQTTSubscriber:
    def __init__(self, message_callback=None):
        # 從 .env 文件中讀取參數
        self.broker = os.getenv("MQTT_BROKER", "localhost")  # 預設為 localhost
        self.port = int(os.getenv("MQTT_PORT", 1883))  # 預設為 1883
        self.topic = os.getenv("MQTT_TOPIC", "sensor/data")  # 預設為 sensor/data

        # 初始化 MQTT 客戶端
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # 設定回呼函數
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # 儲存外部回調函數
        self.message_callback = message_callback

    # 當成功連線時執行的回呼函數
    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"✅ 連線成功！訂閱主題：{self.topic}")
            client.subscribe(self.topic)  # 連線成功後訂閱指定的主題
        else:
            print(f"⚠️ 連線失敗，錯誤碼：{rc}")

    # 當接收到訊息時執行的回呼函數
    def on_message(self, client, userdata, msg):
        print(f"📩 收到訊息: {msg.topic} → {msg.payload.decode('utf-8')}")
        if self.message_callback:
            self.message_callback(msg)

    # 啟動 MQTT 客戶端
    def start(self):
        print("📡 MQTT Subscriber 啟動，等待訊息...")
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()


# 使用封裝的類別
if __name__ == "__main__":
    # 定義一個外部回調函數
    def custom_callback(msg):
        print(f"🔔 外部回調函數執行: {msg.topic} → {msg.payload.decode('utf-8')}")

    # 傳入外部回調函數
    subscriber = MQTTSubscriber(message_callback=custom_callback)
    subscriber.start()
