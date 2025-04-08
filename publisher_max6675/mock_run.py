import json
import logging
import os
import random
import time

# 載入 .env 檔案
from dotenv import load_dotenv
from mqtt_pub import MQTTClient

load_dotenv()

# 設定 LOG 檔案，動態生成檔案名稱
#   確保 logs 資料夾存在
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filename = os.path.join(log_dir, f"Publisher_log_{time.strftime('%Y%m%d')}.txt")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    logging.info("Start logging...")
    # 初始化 MQTT 客戶端與溫度感測器
    mqtt_client = MQTTClient()

    # 從 .env 檔案中讀取設定
    getPoint = os.getenv("INFLUXDB_POINT", "default_point")
    getTagCfg = json.loads(
        os.getenv("INFLUXDB_TAGCFG", '{"default_tag": "default_tag"}')
    )
    getInterval = int(os.getenv("SENSOR_READ_INTERVAL", 1))

    try:
        while True:
            # 讀取溫度
            temperature = random.uniform(
                0.0, 100.0
            )  # 模擬溫度讀取，實際應用中應替換為 sensor.read_temperature()
            # InfluxDB 時間格式
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            # 發送到 MQTT Broker
            # 構建 JSON 格式的 payload
            payload = json.dumps(
                {
                    "point": getPoint,
                    "tagCfg": getTagCfg,
                    "value": temperature,
                    "time": timestamp,
                }
            )
            mqtt_client.publish(payload=payload)

            # 寫入 LOG 檔案
            logging.info(f"Send payload: {payload}")

            # 每秒執行一次
            time.sleep(getInterval)
    except KeyboardInterrupt:
        print("程式中斷")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"Error: {e}")
    finally:
        logging.info("Sensor closed")
        print("SPI 連線已關閉")


if __name__ == "__main__":
    main()
