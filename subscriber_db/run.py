import json
import logging
import os
import time

from mqtt_sub import MQTTSubscriber
from write_influxdb import InfluxDBWriter

# 確保 logs 資料夾存在
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filename = os.path.join(log_dir, f"Subscriber_log_{time.strftime('%Y%m%d')}.txt")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def process_message(msg):
    """
    處理接收到的 MQTT 訊息
    :param msg: MQTT 訊息物件
    """
    try:
        # 將訊息解碼為 JSON 格式
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(f"🔔 處理訊息: {data}")

        # 寫入 InfluxDB
        influx_writer.write_temperature(data)

        # 寫入日誌
        logging.info(f"Received: {payload}")
    except json.JSONDecodeError:
        error_message = f"❌ 無法解析訊息為 JSON: {msg.payload.decode('utf-8')}"
        print(error_message)
        logging.error(error_message)
    except Exception as e:
        error_message = f"❌ 處理訊息時發生錯誤: {e}"
        print(error_message)
        logging.error(error_message)


if __name__ == "__main__":
    # 初始化 InfluxDBWriter
    influx_writer = InfluxDBWriter()

    try:
        # 初始化 MQTTSubscriber 並傳入處理訊息的回調函數
        subscriber = MQTTSubscriber(message_callback=process_message)
        subscriber.start()
    except KeyboardInterrupt:
        print("🛑 程式中止")
    finally:
        # 關閉 InfluxDB 客戶端
        influx_writer.close()
        print("✅ InfluxDB 客戶端已關閉")
