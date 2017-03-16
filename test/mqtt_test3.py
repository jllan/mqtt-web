# File Name:mqtt_chat_client.py
# Python Version:3.5.1

import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)
    client.publish(topic, json.dumps('成功订阅话题{}'.format(topic)))


def on_message(client, userdata, msg):
    # print(msg.topic+":"+str(msg.payload.decode()))
    # print(msg.topic+":"+msg.payload.decode())
    payload = json.loads(msg.payload.decode())
    print(payload)
    # print(payload.get("user") + ": " + payload.get("say"))


if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
    topic = input('请输入要订阅的话题：')
    client.on_connect = on_connect
    client.on_message = on_message

    HOST = "127.0.0.1"

    client.connect(HOST, 1883, 60)
    #client.loop_forever()



    client.loop_start()

    while True:
        user = input("请输入用户名：")
        client.user_data_set(user)
        topic = input('请输入要发布到的话题：')
        content = input("请输入发布到话题{}内容：".format(topic))

        if str:
            client.publish(topic, json.dumps({"user": user, "say": content}))
