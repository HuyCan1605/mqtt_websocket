import paho.mqtt.client as mqtt
import json

broker = '127.0.0.1'
port = 1883
topic = 'sensor/data'
threshold_up = 55.0
threshold_down = 40.0

# Actuator statuses
actuator_statuses = {
    'actuator1': False,
    'actuator2': False,
    'actuator3': False
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    sensor_data = json.loads(msg.payload.decode())
    check_thresholds(sensor_data)

def check_thresholds(sensor_data):
    global actuator_statuses
    print("---------------------------------------------")
    if sensor_data['sensor1'] > threshold_up or sensor_data['sensor1'] < threshold_down:
        if not actuator_statuses['actuator1']:
            actuator_statuses['actuator1'] = True
            print("Actuator 1 turn on")
    else:
        if actuator_statuses['actuator1']:
            actuator_statuses['actuator1'] = False
            print("Actuator 1 turn off")

    if sensor_data['sensor2'] > threshold_up or sensor_data['sensor2'] < threshold_down:
        if not actuator_statuses['actuator2']:
            actuator_statuses['actuator2'] = True
            print("Actuator 2 turn on")
    else:
        if actuator_statuses['actuator2']:
            actuator_statuses['actuator2'] = False
            print("Actuator 2 turn off")

    if sensor_data['sensor3'] > threshold_up or sensor_data['sensor3'] < threshold_down:
        if not actuator_statuses['actuator3']:
            actuator_statuses['actuator3'] = True
            print("Actuator 3 turn on")
    else:
        if actuator_statuses['actuator3']:
            actuator_statuses['actuator3'] = False
            print("Actuator 3 turn off")
    print("---------------------------------------------")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()
