from machine import Pin
import time, ujson
import dht
from umqtt.simple import MQTTClient

# Ubidots configuration
DEVICE_LABEL = "pir"
UBIDOTS_BROKER = "industrial.api.ubidots.com"
UBIDOTS_PORT = 1883
UBIDOTS_USER = "BBUS-VKMrY9nBvYdn5QpmgN2jsZQ6beUh3E"
UBIDOTS_TOPIC = "/v2.0/devices/" + DEVICE_LABEL

print("Menyambungkan ke MQTT server... ", end="")
client = MQTTClient(DEVICE_LABEL, UBIDOTS_BROKER, UBIDOTS_PORT, user=UBIDOTS_USER, password="")
client.connect()
print("Tersambung!")

# Pin definitions
pirPin = Pin(15, Pin.IN)  # PIR sensor pin (input)
ledPin = Pin(16, Pin.OUT)  # LED pin (output)
dhtPin = Pin(21, Pin.IN)  # DHT22 sensor pin (input)
dhtSensor = dht.DHT22(dhtPin)

# Main loop
while True:
    try:
        # Read PIR sensor
        motion_value = pirPin.value()
        ledPin.value(motion_value)

        # Read DHT22 sensor
        dhtSensor.measure()
        temperature = dhtSensor.temperature()
        humidity = dhtSensor.humidity()

        # Create JSON payload
        data = ujson.dumps({
            "gerak": {
                "value": motion_value,
                "context": {"status": "Gerak" if motion_value == 1 else "Tidak Gerak"}
            },
            "suhu": {"value": temperature},
            "kelembaban": {"value": humidity}
        })
        
        # Publish data
        client.publish(UBIDOTS_TOPIC, data)
        
    except Exception as e:
        print("Error:", e)
    
    time.sleep(2)  # Delay for 2 seconds
