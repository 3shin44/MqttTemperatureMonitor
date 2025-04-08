import time

import spidev

"""
MAX6675 溫度計的 SPI 接腳定義

以下串接適用Rpi 3B+

- VCC 接到 Raspberry Pi 的 3.3V
- GND 接到 Raspberry Pi 的 GND
- SCK (時鐘) 接到 GPIO11 (SCLK)
- CS (Chip Select) 接到 GPIO8 (CE0)
- MISO (Master In Slave Out) 接到 GPIO9 (MISO)
"""


class Max6675Sensor:
    """
    MAX6675 溫度感測器的封裝類別
    """

    def __init__(self, bus=0, device=0, max_speed_hz=50000):
        """
        初始化 SPI 設備
        :param bus: SPI bus 編號
        :param device: SPI device 編號
        :param max_speed_hz: SPI 最大速度 (Hz)
        """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)  # 開啟 SPI
        self.spi.max_speed_hz = max_speed_hz  # 設定 SPI 速度

    def read_temperature(self):
        """
        讀取溫度的函式
        :return: 攝氏溫度
        """
        # MAX6675 溫度計讀取命令 (16-bit)
        response = self.spi.xfer2([0x00, 0x00])

        # 讀取回應 (2 bytes)
        high_byte = response[0]
        low_byte = response[1]

        # 組裝 16-bit 數值
        temp = ((high_byte << 8) | low_byte) >> 3

        # 計算攝氏溫度
        temperature = temp * 0.25
        return temperature

    def close(self):
        """
        關閉 SPI 設備
        """
        self.spi.close()

    def continuous_send_temperature(self, interval=1):
        """
        持續讀取溫度
        :param interval: 讀取間隔時間 (秒)
        """
        try:
            while True:
                temp = self.read_temperature()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # 產生時間戳
                print(f"{timestamp} - Temperature: {temp}°C")
                time.sleep(interval)  # 每秒讀取一次
        except KeyboardInterrupt:
            print("程式結束")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        finally:
            self.close()


# 使用範例
if __name__ == "__main__":
    sensor = Max6675Sensor()
    try:
        sensor.continuous_send_temperature(interval=2)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sensor.close()
