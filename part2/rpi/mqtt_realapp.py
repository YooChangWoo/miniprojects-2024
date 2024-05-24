# mqtt_realapp.py
# 온도습도센서데이터 통신, RGB LED Setting
# MQTT -> json transfer
# mqtt_realapp.py
# MQTT -> json transfer
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import datetime as dt
import json

red_pin = 4
green_pin = 6
dht_pin = 18

dev_id = 'PKNU82'
loop_num = 0

def onConnect(client, userdata, flags, reason_code, properties):
    print(f'연결성공 : {reason_code}')
    client.subscribe('pknu/rcv/')

def onMessage(client, userdata, msg):
    print(f'{msg.topic} + {msg.payload}')

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)  # 중요!!
GPIO.setup(dht_pin, GPIO.IN)
dhtDevice = adafruit_dht.DHT11(board.D18)

## 
## 
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) 

# 192.168.5.4 window ip
mqttc.connect('192.168.5.4', 1883, 60) 

mqttc.loop_start()
while True:
    time.sleep(2) # DHT11 2초마다 갱신이 잘됨

    try:
        temp = dhtDevice.temperature
        humd = dhtDevice.humidity
        print(f'{loop_num} - Temp:{temp}/humid"{humd}')

        origin_data = { 'DEV_ID' : dev_id,
                       'CURR_DT' : dt.datetime.now().strftime('%Y-%m-%d %H: %M: %S'),
                       'TYPE' : 'TEMPHUMID',
                       'VALUE' : f'{temp}|{humd}'
                       } # dictionary data
        pub_data = json.dumps(origin_data, ensure_ascii=False)

        mqttc.publish('pknu/data/', pub_data)
        loop_num += 1
    except RuntimeError as ex:
        print(ex.args[0])
    except KeyboardInterrupt:
        break

mqttc.loop_stop()
dhtDevice.exit()
## 실행 끝