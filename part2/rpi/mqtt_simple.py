# mqtt_simple.py
import time
import paho.mqtt.client as mqtt

loop_num = 0

def onConnect(client, userdata, flags, reason_code, properties):
    print(f'Conneted result code : {reason_code}')
    client.subscribe('pknu82/rcv')

def onMessage(client, userdata, msg):
    print(f'{msg.topic} +{msg.payload}')

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # 2023.9 이후 버전 업 
mqttc.on_connect = onConnect # 접속시 이벤트
mqttc.on_connect = onMessage # 접속시 이벤트

# 19.168.5.2 WINDOW IP
mqttc.connect('192.168.5.4', 1883, 60)

mqttc.loop_start()
while True:
    mqttc.publish('pknu82/data', loop_num)
    loop_num += 1
    time.sleep(1)

mqttc.loop_stop()