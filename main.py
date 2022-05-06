from machine import Pin, ADC, reset, unique_id
from time import sleep
import network
import utime
import sys

__MQTT_SERVER__ = <IP_TO_THE_MQTT_BROKER>

__CLIENT_ID__ = ubinascii.hexlify(unique_id())
__TOPIC_PUB__ = b'INTERCOM_RING'

__ACTIVATION_THRESHOLD__ = 1000


def mqtt_connect():
    client = MQTTClient(__CLIENT_ID__, __MQTT_SERVER__)
    client.connect()
    print('Connected to %s MQTT broker.' % (__MQTT_SERVER__))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    reset()


if __name__ == "__main__":
    try:
        client = mqtt_connect()
    except OSError as e:
        restart_and_reconnect()

    input_pin = ADC(Pin(33))
    input_pin.atten(ADC.ATTN_11DB)  # Full range: 3.3v

    ADC.width(ADC.WIDTH_12BIT)
    sample_count = 0
    acum = 0
    signal_act = False

    while True:
        try:
            readed_value = input_pin.read()
            if sample_count < 10:
                sample_count += 1
                acum += readed_value
            else:
                samples_mean = int(acum / 10)
                rounded_mean = round(samples_mean / 100) * 100
                if not signal_act and rounded_mean >= __ACTIVATION_THRESHOLD__:
                    signal_act = True
                    client.publish(__TOPIC_PUB__, "")
                elif rounded_mean <= __ACTIVATION_THRESHOLD__:
                    signal_act = False

                acum = 0
                sample_count = 0
            sleep(0.05)
        except OSError as e:
            restart_and_reconnect()
