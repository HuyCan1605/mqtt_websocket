import paho.mqtt.client as mqtt
import json
import time
import random
import math

broker = '127.0.0.1'
port = 1883
topic = 'sensor/data'

# Parameters for smooth data generation
frequency = 0.1
amplitude = 10
base_value = 50
noise_level = 2

def generate_smooth_data(base, freq, amp, noise, time_step):
    return base + amp * math.sin(freq * time_step) + random.uniform(-noise, noise)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect(broker, port, 60)

time_step = 0

try:
    while True:
        sensor1 = generate_smooth_data(base_value, frequency, amplitude, noise_level, time_step)
        sensor2 = generate_smooth_data(base_value, frequency, amplitude, noise_level, time_step + 10)  # Offset by 10
        sensor3 = generate_smooth_data(base_value, frequency, amplitude, noise_level, time_step + 20)  # Offset by 20

        data = {
            'sensor1': sensor1,
            'sensor2': sensor2,
            'sensor3': sensor3
        }

        client.publish(topic, json.dumps(data))
        print(f"Published data: {data}")

        time_step += 1
        time.sleep(1)  # Send data every second
except KeyboardInterrupt:
    print("Stopping data generation")
finally:
    client.disconnect()
