# This file is executed on every boot (including wake-boot from deepsleep)
import utime
from umqttsimple import MQTTClient
import ubinascii
from machine import Pin 
import micropython
import network
import esp

esp.osdebug(None)
import gc
gc.collect()

