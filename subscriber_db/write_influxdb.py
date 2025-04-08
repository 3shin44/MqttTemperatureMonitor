import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# 載入 .env 檔案
load_dotenv()


class InfluxDBWriter:
    def __init__(self):
        # 從 .env 檔案讀取 InfluxDB 設定
        self.influxdb_url = os.getenv("INFLUXDB_URL")
        self.influxdb_org = os.getenv("INFLUXDB_ORG")
        self.influxdb_bucket = os.getenv("INFLUXDB_BUCKET")
        self.influxdb_token = os.getenv("INFLUXDB_TOKEN")

        # 初始化 InfluxDB 客戶端
        self.client = InfluxDBClient(
            url=self.influxdb_url, token=self.influxdb_token, org=self.influxdb_org
        )
        # 使用同步寫入
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.delete_api = self.client.delete_api()

    def write_temperature(self, data: dict):
        """
        接收 JSON 格式的資料並寫入 InfluxDB
        :param data: JSON 格式的資料

        """
        try:
            # 從 JSON 資料中提取資訊
            point_name = data.get("point", "default_point")
            tag_cfg = data.get("tagCfg", {})  # 修改為 tagCfg
            value = data.get("value", 0.0)
            time_str = data.get("time", datetime.now(timezone.utc))  # 預設為當前時間

            # 建立數據點
            point = (
                Point(point_name)
                .field("value", float(value))
                .time(time_str, WritePrecision.NS)
            )
            for key, val in tag_cfg.items():  # 使用 tagCfg 的 key-value
                point = point.tag(key, val)

            # 寫入數據
            self.write_api.write(
                bucket=self.influxdb_bucket, org=self.influxdb_org, record=point
            )
            print("✅ Data written successfully!")

        except Exception as e:
            print(f"❌ Failed to write data: {e}")

    def delete_temperature_data(self, delete_condition: str):
        """
        刪除 InfluxDB 中符合條件的數據
        :param delete_condition: 刪除條件的字串，例如 '_measurement="temperature"'
        """
        try:
            start_time = "1970-01-01T00:00:00Z"  # 刪除所有數據的起始時間
            stop_time = datetime.now(timezone.utc).isoformat()  # 使用標準庫的 UTC 時區

            self.delete_api.delete(
                start_time,
                stop_time,
                delete_condition,
                bucket=self.influxdb_bucket,
                org=self.influxdb_org,
            )
            print(f"✅ Data matching condition '{delete_condition}' has been deleted.")
        except Exception as e:
            print(f"❌ Failed to delete data: {e}")

    def close(self):
        # 關閉客戶端
        self.client.close()


# 測試用程式碼
if __name__ == "__main__":
    import time

    writer = InfluxDBWriter()
    try:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        test_data = {
            "point": "temperature_test",
            "tagCfg": {"sensor": "temperature", "module": "max6675"},
            "value": 100.0,
            "time": timestamp,
        }
        # writer.write_temperature(test_data)

        # writer.delete_temperature_data('_measurement="temperature"')

    finally:
        writer.close()
        print("✅ Client closed successfully!")
