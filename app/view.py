import paho.mqtt.client as mqtt
import json
import datetime
from flask import request, render_template, flash, redirect, url_for, jsonify
from app.models import Sub, SubForm, Pub, PubForm
from flask import Flask
import config
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object(config)
db = MongoEngine(app)

MESSAGE = ''

# @app.route('/')
# def index():
#     print('hah')
#     # return 'hahh'
#     return render_template('pub.html')

@app.route('/sub', methods=['GET', 'POST'])
def subscription():
    if request.method == 'GET':
        global MESSAGE
        print(type(MESSAGE))
        # MESSAGE['receive_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        print('收到消息', MESSAGE)
        sub_form = SubForm()
        # sub_msg = Sub.objects.order_by('-time')
        if MESSAGE:
            flash(MESSAGE)
        return render_template('sub.html', msg=MESSAGE, form=sub_form)
    else:
        sub_form = SubForm(request.form)
        if sub_form.validate():
            global topic
            address = sub_form.address.data
            topic = sub_form.topic.data
            qoc = sub_form.qoc.data
            client_id = sub_form.client_id.data
            user_name = sub_form.user_name.data
            password = sub_form.password.data
            # print(address, topic, qoc, client_id, user_name, password)
            sub_msg = Sub(address = sub_form.address.data,
                       topic = sub_form.topic.data,
                       # content = sub_form.content.data,
                       qoc = sub_form.qoc.data,
                       client_id = sub_form.client_id.data,
                       user_name = sub_form.user_name.data,
                       password = sub_form.password.data,
                       create_time=datetime.datetime.now())
            sub_msg.save()
            start_connect(address)
            flash('发表成功')
            return redirect(url_for('subscription'))

def start_connect(address):
    client.on_connect = on_connect
    client.on_message = on_message
    # HOST = "127.0.0.1"
    client.connect(address, 1883, 60)
    # client.loop_forever()
    client.loop_start()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)
    client.publish(topic, json.dumps('成功订阅话题{}'.format(topic)))


def on_message(client, userdata, msg):
    #print(msg.topic+":"+str(msg.payload.decode()))
    #print(msg.topic+":"+msg.payload.decode())
    payload = json.loads(msg.payload.decode())
    # print(payload.get("user") + ": " + payload.get("say"))
    print(payload)
    global MESSAGE
    print(type(MESSAGE))
    MESSAGE = payload


@app.route('/')
@app.route('/pub', methods=['GET', 'POST'])
def publication():
    client = mqtt.Client()
    client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    HOST = "127.0.0.1"
    client.connect(HOST, 1883, 60)
    if request.method == 'GET':
        pub_form = PubForm()
        pub_msgs = Pub.objects.order_by('-time')
        return render_template('pub.html', msgs=pub_msgs, form=pub_form)
    else:
        pub_form = PubForm(request.form)
        if pub_form.validate():
            address = pub_form.address.data
            topic = pub_form.topic.data
            content = pub_form.content.data
            qoc = pub_form.qoc.data
            client_id = pub_form.client_id.data
            user_name = pub_form.user_name.data
            password = pub_form.password.data
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            # print(address, topic, content, qoc, client_id, user_name, password)
            pub_msg = Pub(address = address,
                       topic = topic,
                       content = content,
                       qoc = qoc,
                       client_id = client_id,
                       user_name = user_name,
                       password = password,
                       create_time = create_time)
            pub_msg.save()
            # client.publish(topic, pub_msg)
            client.publish(topic, json.dumps({"user_name": user_name, "topic":topic, "content": content, "create_time": create_time}))
            flash('发布成功')
            return redirect(url_for('publication'))
        else:
            flash('输入信息有误，请重新输入')
            return redirect(url_for('publication'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    client = mqtt.Client()

    app.run(debug=True, port=8888)