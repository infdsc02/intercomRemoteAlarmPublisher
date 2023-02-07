# intercomRemoteAlarmPublisher
Nodo de MQTT que se encarga de publicar un mensaje cuando llaman al portero automático.

El material utilizado fue:
  1. Vídeoportero Fermax modelo 9445. 
  2. Az-Delivery ESP32 Dev Kit C V2.
  3. Step Down LM2596
  
 El software está escrito en MicroPython utilizando las librerías [MQTTSimple](https://github.com/RuiSantosdotme/ESP-MicroPython/tree/master/code/MQTT) y [WiFiManager](https://github.com/tayfunulu/WiFiManager), esta última se ha modificado para poder introducir la configuración de conexión del broker MQTT.
 
 Para detectar que alguien ha llamado se ha conectado el pin 33 del ESP32 al led del videoportero y con el ADC se detecta que el voltage sobrepasa cierto umbral (aprox. 1V). No se ha podido utilizar una entrada digital porque el voltaje no es suficiente para que el ESP32 lo detecte como un valor alto. Esta solución tiene el pequeño problema (que se solucionará en el futuro) de que en el momento que se pulsa en el vídeoportero el botón que activa la cámara se detecta como si hubiesen timbrado.
 
 ###### Imágenes del montaje
 ![](/images/IMG20230207193813.jpg)
 
 ![](/images/IMG20230207193820.jpg)
 
 ![](/images/IMG20230207193833.jpg)
