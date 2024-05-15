import time
from umqtt.simple import MQTTClient
import network
import ujson
import random


class SignalsMonitoring:
    def __init__(self, wifi_ssid, wifi_password, mqtt_broker, mqtt_user, mqtt_password, central, uart):
        # Configuración inicial
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = 1883
        self.mqtt_user = mqtt_user
        self.mqtt_password = mqtt_password
        self.RX_publish = central
        self.serial=uart
        self.data={"command": "", "state": ""}

    def config_wifi(self):
        # Connect to WiFi
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(self.wifi_ssid, self.wifi_password)

        # Wait until connected to WiFi
        while not wifi.isconnected():
            time.sleep(1)
            
        print("Connected to WiFi")
        
        time.sleep(2)
        mac = wifi.config('mac')
        self.TX_subscribe = "Mod_alpha_"+mac.hex()
        #print("MAC Address:", mac)
        return self.TX_subscribe

    def connect_broker(self):
        self.mqtt_client = MQTTClient("client_id", self.mqtt_broker, self.mqtt_port, self.mqtt_user, self.mqtt_password)
        self.mqtt_client.connect()
        self.mqtt_client.set_callback(self.sub_cb)
        self.mqtt_client.subscribe(self.TX_subscribe)
#         self.pub_cb(self.RX_publish, self.TX_subscribe,  "WakeUp")

    def send_json(self, msg):
        json_data = ujson.dumps(msg )
        self.serial.write(bytes(json_data + '\n', 'utf-8'))
                

    def main(self):
        self.config_wifi()
        self.connect_broker()
        print("Connected to MQTT broker")

        # Bucle principal para esperar mensajes
        while True:
            try:
                self.mqtt_client.check_msg()
                # Puedes agregar cualquier otra lógica aquí que necesites realizar de manera continua
            except OSError as e:
                # Maneja cualquier error de conexión MQTT aquí
                print("MQTT connection error:", e)
            time.sleep(1)

    def sub_cb(self, topic, msg):
        try:
            if isinstance(msg, bytes):
                msg_str = msg.decode("utf-8")
            elif isinstance(msg, str):
                msg_str = msg
            else:
                print("The message is neither a valid string nor a byte sequence")
                return

            # Print the received JSON
            msg_str_corregido = msg_str.replace("'", '"')
            _msg = ujson.loads(msg_str_corregido)
            

            # Print the value of the "destine" field
            if "destiny" in _msg:
                print(" 'origin': ", _msg["origin"])
                print(" 'destiny': ",_msg["destiny"])
                print(" 'command': ",_msg["command"])
#                 print(" 'arg1': ",_msg["arg1"])
                if _msg["command"] == "Status":
                    print("*************************************")
                    self.pub_cb(_msg["origin"], _msg["destiny"], "OK", _msg["command"])
                    time.sleep(1)
                if _msg["command"] == "Request":
                    print("-------------------------------------")
                    # Llamar a pub_cb
                if _msg["command"] == "setBoardAvailable":
                    self.data["command"]=_msg["command"]
                    self.data["state"]=_msg["arg1"]
                    self.send_json(self.data)
#                     self.pub_cb(_msg["origin"], _msg["destiny"], "OK", _msg["command"])
                    
                if _msg["command"] == "setMachineReady":
                    self.data["command"]=_msg["command"]
                    self.data["state"]=_msg["arg1"]
                    self.send_json(self.data)
#                     self.pub_cb(_msg["origin"], _msg["destiny"], "OK", _msg["command"])
                    
                if _msg["command"] == "setNotGood":
                    self.data["command"]=_msg["command"]
                    self.data["state"]=_msg["arg1"]
                    self.send_json(self.data)
#                     self.pub_cb(_msg["origin"], _msg["destiny"], "OK", _msg["command"])
                    
                if _msg["command"] == "statusModule":
                    self.data["command"]=_msg["command"]
                    self.data["state"]=_msg["arg1"]
                    self.send_json(self.data)
                    print("99999999"+str(_msg["arg1"]))
#                     self.pub_cb(_msg["origin"], _msg["destiny"], "OK", _msg["command"])
                    
                if _msg["command"] == "testConection":
                    self.data["command"]=_msg["command"]
                    self.data["state"]=_msg["arg1"]
                    self.send_json(self.data)
#                     self.pub_cb(_msg["origin"], _msg["destiny"], _msg["command"]+"_OK", "")
                    self.pub_cb(_msg["origin"], _msg["destiny"], "OK", _msg["command"])
                    
                if _msg["command"] == "setModuleActivate":
                    print(_msg["command"])
                    print(_msg["arg1"])
                    self.data["command"]=_msg["command"]
                    self.data["state"]=_msg["arg1"]
                    self.send_json(self.data)
                    self.pub_cb(_msg["origin"], _msg["destiny"], "OK", _msg["command"])
                if _msg["command"] == "setConveyorTestMode":
                    print(_msg["command"])
                    print(_msg["arg1"])
                    self.data["command"]=_msg["command"]
                    self.data["state"]=_msg["arg1"]
                    self.send_json(self.data)
                    self.pub_cb(_msg["origin"], _msg["destiny"], "OK", _msg["command"])
                if _msg["command"] == "OK":
                    print(_msg["command"])
                    print(_msg["arg1"])
        
                if _msg["command"] == "Birth":
                    print(_msg["command"])
                    print(_msg["arg1"])
                if _msg["command"] == "lastWill":
                    print(_msg["command"])
                    print(_msg["arg1"])
                                                
                if _msg["command"] == "test":
                    print(_msg["command"])
                    print(_msg["arg1"])
                    self.data["command"]=_msg["command"]
                    self.data["state"]=_msg["arg1"]
                    self.send_json(self.data)
                                          
            else:
                print("The  field is not present in the received JSON")
                print(_msg)

        except Exception as e:
            print("Error loading JSON:", e) 

    def pub_cb(self, topic, topic_subscribe,  msg,arg1):
        message_dict = {
            "origin": topic_subscribe,
            "destiny": topic,
            "command": msg,
            "arg1": arg1,
            "arg2": "",
            "arg3": ""
        }
        message_json = ujson.dumps(message_dict)
        self.mqtt_client.publish(topic, message_json)
        self.mqtt_client.check_msg()




