# smoid Library 

This library focused to control conection to MQTT servers, the posibility install realy fast. 
Now, in PyPi

the version available is 0.0.1, and the way to install is:

Go to your Thonny IDE, and select the option to manage packages.
 
write `smoid` and install the package.

# How to use
code 

```python
from smoid import SignalsMonitoring

import machine
import utime
import ujson
import _thread

central="CentralModule2"
SSID = "YOUR_SSID"
PASSWORD = "YOUR_PASSWORD"
MQTT_server = "server ip"
MQTT_user = "user"
MQTT_password = "password"

uart = machine.UART(1, baudrate=115200, tx=machine.Pin(17), rx=machine.Pin(16))

def esp32_send_data(data):
    uart.write(data)

def esp32_receive_data():
    if uart.any():
        return uart.read()
    else:
        return None
MAX_RECONNECT_ATTEMPTS = 6

def mqtt_b(conection):
    reconnect_attempts = 0
    while True:
        try:
            conection.mqtt_client.check_msg()
            reconnect_attempts = 0
        except OSError as e:
            print("MQTT connection error:", e)
            reconnect_attempts += 1
            if reconnect_attempts >= MAX_RECONNECT_ATTEMPTS:
                print("Max reconnect attempts reached, resetting device...")
                machine.reset()
            else:
                print("Attempting to reconnect...")
                utime.sleep(5)
def serial(conection,name_device):
    while True:
        data = recibir_json(conection, name_device)

            
def main():
    conection = SignalsMonitoring(SSID, PASSWORD, MQTT_server, MQTT_user, MQTT_password, central, uart)  
    name_device = conection.config_wifi()
    conection.connect_broker()
    print("Connected to MQTT broker")

    
    conection.pub_cb(central, name_device, "set_BufferConveyor_Conveyor_Module", "")
    _thread.start_new_thread(mqtt_b, (conection,))
    while True:

        received_data = esp32_receive_data()
        if received_data:
            try:
                received_data = received_data.replace(b"'", b'"')

                lines = received_data.split(b'\n')
                lines = [line.strip() for line in lines if line.strip()]
                for line in lines:
                    try:
                        data = ujson.loads(line)
                        print("Parsed JSON:", data)
                        
                        
                        del data["command"]
                        del data["status"]
                        conection.pub_cb(central, name_device, "OK",data)
                            
                    except ValueError:
                        print("Error parsing JSON:", line)
                
            except OSError as e:
                print("MQTT connection error:", e)
        utime.sleep(1)

if __name__ == "__main__":
    main()

```




