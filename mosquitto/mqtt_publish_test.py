import time
from random import uniform

import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


def main():
    client = mqtt.Client("TemperatureInsidePublishTest")
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    # mqttc.on_log = on_log
    client.connect("127.0.0.1", 1883, 60)

    while True:
        random_number = uniform(20.0, 21.0)
        topic = "sensors/smart-garden"
        """Message syntax
            <measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]

        Example:
            myMeasurement,tag1=value1,tag2=value2 fieldKey="fieldValue" 1556813561098000000
            
            measurementName,tagKey=tagValue fieldKey="fieldValue" 1465839830100400200
            --------------- --------------- --------------------- -------------------
                   |               |                  |                    |
              Measurement       Tag set           Field set            Timestamp
              
        Link:
            https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/#
        """
        message = f"temperature,device_id=MKR\ IoT\ Carrier celsius={random_number}"
        client.publish(topic, message)
        print(f"Just published on topic {topic}: {message}")
        time.sleep(1)


if __name__ == '__main__':
    main()
