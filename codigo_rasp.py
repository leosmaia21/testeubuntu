import paho.mqtt.client as mqtt

import time
import json
localizacoes=[1000]
localizacoes = [0 for i in range(1000)]

def on_log_ttn(client,userdata,level,buf):
    print("log ttn: "+buf)

def on_log_app(client,userdata,level,buf):
    print("log app: "+buf)
    
def on_connect_ttn(client,userdata,flags,rc):
    if rc==0:
        print("ttn conectado")
    else:
        print ("bad connection returned code=",rc)

def on_connect_app(client,userdata,flags,rc):
    if rc==0:
        print("app conectado")
    else:
        print ("bad connection returned code=",rc)

def on_message_ttn(client,userdata,msg):
    #print(msg.payload.decode('utf-8'))
    topic=msg.topic
    x=json.loads(msg.payload.decode('utf-8'))
    j=int(x["uplink_message"]["decoded_payload"]["mensagem"])
    print(j)
    lon=-(j&0xffffffff)/(1e6)
    lat=((j>>32)&0xffffffff)/(1e6)
    id_autocarro=(j>>101)
    print("id:",id_autocarro,"lat:",lat,"lon",lon)
    localizacoes[id_autocarro]=str(lat)+","+str(lon)
    
    
def on_message_app(client,userdata,msg):
    m=str(msg.payload.decode("utf-8"))
    print("mensagem recebida:",m)
    x=m.split("/",1)
    client_app.publish(x[1],str(localizacoes[int(x[0])]))
    print(str(localizacoes[int(x[0])]))

broker_ttn="eu1.cloud.thethings.network"
broker_app="broker.hivemq.com"
client_app=mqtt.Client("leonardo",1883)
client_ttn=mqtt.Client("leo",1883)
client_ttn.on_connect=on_connect_ttn
client_app.on_connect=on_connect_app
client_ttn.on_log=on_log_ttn
client_app.on_log=on_log_app
client_ttn.on_message=on_message_ttn
client_app.on_message=on_message_app
client_ttn.username_pw_set("wheresmybus@ttn","NNSXS.MH4VPZOFIG4OWO6WFDMVIKPOZ725NB37IXYCNXI.RWYJWRJ5JMP62YXHQB37EQNGBWX4WJ2EVBEUPBX3HAE5E4UIVEJQ")
client_app.connect(broker_app)
client_ttn.connect(broker_ttn)
time.sleep(1)
client_app.subscribe("home/wheresmybus/app")
client_ttn.subscribe("v3/wheresmybus@ttn/devices/+/up")
client_app.loop_start()
client_ttn.loop_forever()
#time.sleep(40)«
#client.loop_stop()
#client.disconnect()

