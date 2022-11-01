#!/usr/bin/env python3

import argparse
import json
import random
import requests
import sys
import time
import yaml
import xml.etree.ElementTree as ET

from paho.mqtt import client as mqtt_client

DISCOVERY_PREFIX = 'homeassistant'
ID = '163682'
PREFIX = 'intellinet_smart_pdu_163682'
MAX_PORTS = 8


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Synchronize PDU state with MQTT')
    parser.add_argument('--pdu-hostname', default='pdu',
                        help='pdu hostname')
    parser.add_argument('--mqtt-hostname', default='homeassistant',
                        help='mqtt broker hostname')
    parser.add_argument('--mqtt-port', default=1883,
                        help='mqtt broker port')
    parser.add_argument('--mqtt-user',
                        help='mqtt username')
    parser.add_argument('--mqtt-password',
                        help='mqtt password')
    return parser.parse_args()


def connect_mqtt(broker, port, username, password):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect, return code %d\n', rc)
            sys.exit(1)

    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client, pdu_hostname):
    base_topic = '{}/{}'.format(DISCOVERY_PREFIX, 'switch')
    prefix = '{}/{}_port'.format(base_topic, PREFIX)
    def on_message(client, userdata, message):
        # check topic for command_topic
        if message.topic.startswith(prefix) and message.topic.endswith('/set'):
            port = int(message.topic.replace(prefix, '').replace('/set', ''))
            status = message.payload.decode()
            set_port_status(client, pdu_hostname, port, status)

    client.subscribe(base_topic + '/#')
    client.on_message = on_message


def publish_discovery_payload(client, entity_class, unique_id, payload):
    base_topic = '{}/{}'.format(DISCOVERY_PREFIX, entity_class)
    entity_topic = '{}/{}'.format(base_topic, unique_id)
    discovery_payload = {
        '~': entity_topic,
        'object_id': unique_id,
        'unique_id': unique_id,
        'state_topic': '~/state',
    }
    # overwrite entity-specific parameters
    discovery_payload.update(payload)

    topic = '{}/config'.format(entity_topic)
    message = json.dumps(discovery_payload)
    publish_message(client, topic, message)


def publish_message(client, topic, message):
    result = client.publish(topic, message)[0]
    if result != 0:
        print('Failed to publish message to topic {}'.format(topic))


def load_port_labels():
    # init defaults
    port_labels = [{'name': 'Port {}'.format(i+1)} for i in range(MAX_PORTS)]
    try:
        with open('ports.yaml') as fd:
            port_labels = yaml.safe_load(fd)
    except:
        pass
    return port_labels


def register_device(client):
    # Entities
    entity_class = 'switch'
    port_labels = load_port_labels()
    for i in range(MAX_PORTS):
        unique_id = '{}_port{}'.format(PREFIX, i+1)
        payload = {
            'name': port_labels[i]['name'],
            'command_topic': '~/set',
            'device': {
                'ids': [ ID ]
            }
        }
        publish_discovery_payload(client, entity_class, unique_id, payload)

    # Device
    entity_class = 'sensor'
    unique_id = '{}_status'.format(PREFIX)
    payload = {
        'name': 'Intellinet Smart PDU 163682',
        'device': {
            'ids': [ ID ],
            'manufacturer': 'Intellinet',
            'model': 'Smart PDU 163682',
            'name': 'Technikschrank-PDU',
            'sw_version': '1.0.2',
        }
    }
    publish_discovery_payload(client, entity_class, unique_id, payload)


def publish_port_status(client, pdu_hostname, num=0):
    base_topic = '{}/{}'.format(DISCOVERY_PREFIX, 'switch')
    status = get_port_status(pdu_hostname)
    for i in range(MAX_PORTS):
        # if num is given send only status of particular port
        if num and num != i+1:
            continue
        unique_id = '{}_port{}'.format(PREFIX, i+1)

        topic = '{}/{}/state'.format(base_topic, unique_id)
        message = status[i]
        publish_message(client, topic, message)


def get_port_status(hostname):
    url = 'http://{}/status.xml'.format(hostname)
    r = requests.get(url)
    if r.status_code != 200:
        return

    status = []
    root = ET.fromstring(r.text)
    for child in root:
        if child.tag.startswith('outletStat'):
            s = child.text.upper()
            status.append(s)
    return status


def set_port_status(client, hostname, port, status):
    if status.lower() == 'on':
        op = '0'
    if status.lower() == 'off':
        op = '1'
    outlet = str(port - 1)
    url = 'http://{}/control_outlet.htm?outlet{}=1&op={}&submit=Apply'.format(
        hostname, outlet, op)
    r = requests.get(url)
    if r.status_code == 200:
        publish_port_status(client, hostname, num=port)


def main():
    args = parse_arguments()
    client = connect_mqtt(args.mqtt_hostname,
                          args.mqtt_port,
                          args.mqtt_user,
                          args.mqtt_password)
    register_device(client)
    subscribe(client, args.pdu_hostname)
    client.loop_start()
    while True:
        publish_port_status(client, args.pdu_hostname)
        time.sleep(30)


if __name__ == '__main__':
    main()
