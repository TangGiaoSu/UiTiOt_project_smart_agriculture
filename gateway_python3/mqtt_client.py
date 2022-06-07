import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json


class TopPic:
    def __init__(self) -> None:
        self.__topic_subscribe = []
        self.__topic_publish = {}


    def __del__(self) -> None:
        self.__topic_publish.clear()
        self.__topic_subscribe.clear()
    

    @property
    def topic_subscribe(self) -> list:
        return self.__topic_subscribe


    @property
    def topic_publish(self) -> dict:
        return self.__topic_publish


    @topic_subscribe.setter
    def topic_subscribe(self, list_topic: list) -> None:
        self.__topic_subscribe = list_topic
    

    @topic_publish.setter
    def topic_publish(self, dict_topic: dict) -> None:
        self.__topic_publish = dict_topic




class MQTTClient:
    def __init__(self, server_name: str, port: int = 1883) -> None:
        self.__server_name = server_name
        self.__port = port
        self.__client = mqtt.Client()


    def set_callbacks(self, on_connect, on_message) -> None:
        self.__client.on_connect = on_connect
        self.__client.on_message = on_message


    async def connect_to_broker_forever(self) -> None:
        self.__client.connect(self.__server_name, self.__port, 60)
        self.__client.loop_forever()


    def publish(self, topic: str, value: str | int | float) -> None:
        try:
            dictionary = {}
            key = topic.split("/")[-1]
            dictionary[key] = value
            json_object = json.dumps(dictionary)

            publish.single(topic, json_object, hostname=self.__server_name, port=self.__port)
            print("Publish", json_object, "to", self.__server_name)
        except Exception as e:
            print("PUBLISH ERROR!", str(e))


