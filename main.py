from machine import Pin, ADC, reset, unique_id
from time import sleep
import network
import utime
import sys
import wifimgr


__CLIENT_ID__ = ubinascii.hexlify(unique_id())
__TOPIC_PUB__ = b'INTERCOM_RING'

__ACTIVATION_THRESHOLD__ = 1000

debounce_time = 0
        
        
def mqtt_connect(server_host, port, user, password):
    global __CLIENT_ID__
    client = MQTTClient(client_id=__CLIENT_ID__, server=server_host, port=port, user=user, password=password)
    client.connect()
    print('Connected to %s MQTT broker.' % (server_host))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    reset()
    
        
if __name__ == "__main__":
    input_pin = ADC(Pin(33))
    input_pin.atten(ADC.ATTN_11DB)  # Full range: 3.3v
    
    sample_count = 0
    acum = 0
    signal_act = False
    
    wlan = wifimgr.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D
        
    try:
        mqtt_broker_host, mqtt_broker_port, mqtt_broker_user, mqtt_broker_password = wifimgr.read_mqtt_broker_conf()
        client = mqtt_connect(server_host=mqtt_broker_host, port=int(mqtt_broker_port), user=mqtt_broker_user, password=mqtt_broker_password)
    except OSError as e:
        print(str(e))
        restart_and_reconnect()

    
    while True:
        
        if gc.mem_free() < 102000:
          gc.collect()
          
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
