#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name: nano-mqtt-bridge.py
    Author: Cristian Livella
    Date created: 30/01/2021
    Date last modified: 30/01/2021
    License: MIT
"""

import asyncio
import websockets
import json
import time
import paho.mqtt.client as mqtt

WS_HOST = "127.0.0.1"
WS_PORT = "7078"
MQTT_HOST = "127.0.0.1"
MQTT_USERNAME = "user"
MQTT_PASSWORD = "password"
MQTT_CLIENT = "nano-mqtt-bridge"

async def main():
    async with websockets.connect(f"ws://{WS_HOST}:{WS_PORT}") as websocket:
        await websocket.send(json.dumps({"action": "subscribe", "topic": "confirmation", "ack": True}))
        await websocket.recv()
        while True:
            rec = json.loads(await websocket.recv())
            topic = rec.get("topic", None)
            if topic and topic == "confirmation" and rec["message"]["block"]["subtype"] == "send":
                message = rec["message"]
                client.publish("nano/" + message["account"] + "/send", payload=json.dumps({"amount": int(message["amount"]), "hash": message["hash"], "recipient": message["block"]["link_as_account"]}), qos=1)
                client.publish("nano/" + message["block"]["link_as_account"] + "/receive", payload=json.dumps({"amount": int(message["amount"]), "hash": message["hash"], "sender": message["account"]}), qos=1)


client = mqtt.Client(MQTT_CLIENT)
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.connect_async(MQTT_HOST)
client.loop_start()

while True:
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except:
        pass
    time.sleep(5)
