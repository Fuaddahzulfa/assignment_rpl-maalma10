import network
import time
from machine import Timer
import random
from umqtt.simple import MQTTClient

print("Menyambungkan WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(1)
print(" Tersambung!")