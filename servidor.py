import paho.mqtt.client as mqtt
from tkinter import *

import time
import json
localizacoes=[1000]
localizacoes = [0 for i in range(1000)]
timestamp=[1000]
timestamp = [0 for i in range(1000)]
data=[1000]
data = [0 for i in range(1000)]
contador=0
localizacoes[1]="40.605732,-8.662133"
localizacoes[2]="40.645732,-8.672133"
def funcao():
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
        print(msg.payload.decode('utf-8'))
        try:
            topic=msg.topic
            x=json.loads(msg.payload.decode('utf-8'))
            j=(x["uplink_message"]["decoded_payload"]["i"])
            #j.reverse()
            print(j)
            j=int.from_bytes(j, byteorder='big', signed=False)
            lon=-(j&0xffffffff)/(1e6)
            lat=((j>>32)&0xffffffff)/(1e6)
            hora=str((j>>64)&0x3ffff)
            hora=hora.zfill(6)
            datax=str((j>>82)&0x3ffff)
            
            id_autocarro=(j>>101)
            print("id:",id_autocarro,"lat:",lat,"lon",lon)
            localizacoes[id_autocarro]=str(lat)+","+str(lon)
            horax=int(hora[0:2])+1
            timestamp[id_autocarro]=str(horax)+":"+hora[2:4]+":"+hora[4:]
            data[id_autocarro]=datax[0:2]+"/"+datax[2:4]+"/"+datax[4:]
            print("data bonitinha",data[id_autocarro])
            print("hora bonitinha:",timestamp[id_autocarro])
            locations[id_autocarro-1].config(text=str(lat)+","+str(lon))
            horas[id_autocarro-1].config(text=timestamp[id_autocarro])
            datas[id_autocarro-1].config(text=data[id_autocarro])
        
        except:
            print("Erro do ttn, vai-se la saber qual")
        
    def on_message_app(client,userdata,msg):
        try:
            m=str(msg.payload.decode("utf-8"))
            print("mensagem recebida:",m)
            x=m.split("/",1)
            mensagem=str(localizacoes[int(x[0])])+','+str(timestamp[int(x[0])])
            client_app.publish(x[1],mensagem)
            print(mensagem)
            telemovel_uuid.config(text=str(x[1]))
            telemovel_pedido.config(text=str(x[0]))
        except:
            print("Erro do null")

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

        #time.sleep(40)
        #client.loop_stop()
        #client.disconnect()
        client_app.loop_start()
        client_ttn.loop_start()
janela =Tk()
janela.geometry("600x400")
funcao()
janela.title("Where'smyBUS Server")

autocarro=[]
for x in range(1,6):
    print(x)
    j=Label(janela,text="Autocarro"+str(x))
    j.grid(column=0,row=x+2,padx=10,pady=10)
    autocarro.append(j)

locations=[]
localizacao=Label(janela,text="Localização")
localizacao.grid(column=1,row=0,padx=5,pady=5)
for x in range(1,6):
    print(x)
    j=Label(janela,text="---")
    j.grid(column=1,row=x+2,padx=10,pady=10)
    locations.append(j)

horas=[]
hora=Label(janela,text="Hora")
hora.grid(column=2,row=0,padx=5,pady=5)
for x in range(1,6):
    print(x)
    j=Label(janela,text="---")
    j.grid(column=2,row=x+2,padx=10,pady=10)
    horas.append(j)

datas=[]
data_label=Label(janela,text="Data")
data_label.grid(column=3,row=0,padx=5,pady=5)
for x in range(1,6):
    print(x)
    j=Label(janela,text="---")
    j.grid(column=3,row=x+2,padx=10,pady=10)
    datas.append(j)

telemovel_titulo=Label(janela,text="UUID último utilizador")
telemovel_titulo.grid(column=0,row=8,padx=5,pady=10)
telemovel_uuid=Label(janela,text="---")
telemovel_uuid.grid(column=0,row=9,padx=10,pady=10)
telemovel_pedido_x=Label(janela,text="Autocarro pedido")
telemovel_pedido_x.grid(column=1,row=8,padx=5,pady=10)
telemovel_pedido=Label(janela,text="---")
telemovel_pedido.grid(column=1,row=9,padx=10,pady=10)


janela.mainloop()