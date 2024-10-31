import threading


from mqtt import mqtt_thread
from api import run

if __name__ == '__main__':
    thread_api = threading.Thread(target=run)
    thread_mqtt = threading.Thread(target=mqtt_thread)
    thread_api.start()
    thread_mqtt.start()
