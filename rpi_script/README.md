# Raspberry pi Pub/Sub 快速啟動腳本

## 路徑結構

```
│── start-all.sh
│── stop-all.sh
│── publisher_max6675
│      └──docker-compose.yml
└── subscriber
       └──docker-compose.yml
```

## 說明

### 全部啟動：讀取溫度並回寫資料庫

`sudo bash start-all.sh`

先啟動SUB等待數據，再啟動PUB讀取溫度並發布至BROKER

### 全部停止：停止讀取溫度，再停止監聽服務

`sudo bash stop-all.sh`