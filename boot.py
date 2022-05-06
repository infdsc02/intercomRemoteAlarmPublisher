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

__LED_ERROR__ = Pin(12, Pin.OUT, value=0)
__TWO_MINUTES__ = 120000
__WIFI_CONFIG__ = {
    'ssid':'<WIFI_SSID>',
    'password':'<WIFI_PASS>'
}


def connect_wifi():
    get_elapsed_time = lambda start_time: utime.ticks_diff(utime.ticks_ms(), start_time)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    start_time = utime.ticks_ms()
    sta_if.connect(__WIFI_CONFIG__['ssid'], __WIFI_CONFIG__['password'])
    
    print('Trying to connect to ', __WIFI_CONFIG__['ssid'] +"...")
    
    # Waits two minutes for wifi connection
    while (not sta_if.isconnected()) and (get_elapsed_time(start_time) < __TWO_MINUTES__):
        pass
    
    if(sta_if.isconnected()):
        print('Connected to ', __WIFI_CONFIG__['ssid'] +"...")
        return True
    else:
        print("It couldn't connect to ", __WIFI_CONFIG__['ssid'])
        return False

if __name__ == "__main__":
    connected = connect_wifi()
    if not connected:
        __LED_ERROR__.value(1)
        sys.exit(-1)