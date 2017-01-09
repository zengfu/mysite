import paho.mqtt.client as mqtt



def on_connect(client, userdata, rc):
    client.subscribe("$SYS/#")
    client.subscribe('beat')

def on_message(client, userdata, msg):
    # Do something
    pass

client = mqtt.Client(client_id='web')
client.on_connect = on_connect
client.on_message = on_message

client.connect("www.bananalife.top", 1883, 60)