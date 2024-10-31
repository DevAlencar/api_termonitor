from time import sleep
import sqlite3
import paho.mqtt.client as mqtt

# Configuração inicial
broker_url = "a25833zo7tzuak-ats.iot.us-east-1.amazonaws.com"
broker_port = 8883  # Porta padrão para MQTTS

ca_cert = "./certs/AmazonRootCA1.pem"
client_cert = "./certs/b450e05ca1bed0f488c9ce5fabf2a3c803071e542cd6ef4e42297fa43f837d37-certificate.pem.crt"
client_key = "./certs/b450e05ca1bed0f488c9ce5fabf2a3c803071e542cd6ef4e42297fa43f837d37-private.pem.key"
data = []

# Funções de callback para MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("temperatura")

def on_message(client, userdata, msg):
    try:
        data.append([float(x) for x in msg.payload.decode("utf-8").strip().split()])
    except ValueError:
        print("ERROR")

# Configuração do cliente MQTT
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.tls_set(ca_cert, certfile=client_cert, keyfile=client_key)

mqttc.connect(broker_url, broker_port)

# Função principal para rodar em uma thread
def mqtt_thread():
    conn = sqlite3.connect('data.sqlite')
    cursor = conn.cursor()
    while True:
        mqttc.loop_start()

        try:
            env_value = data[0][0]
            obj_value = data.pop()
            obj_value = obj_value[1]
            print('valores inseridos: ')
            print(obj_value)
            print(env_value)
            data.clear()
        except IndexError:
            print("Nenhum dado novo")
            env_value = None
            obj_value = None

        if env_value is not None and obj_value is not None:
            cursor.execute('''
            INSERT INTO sensors (obj_value, env_value)
            VALUES (?, ?)
            ''', (obj_value, env_value))
            conn.commit()

        sleep(5.0)


