#!/usr/bin/with-contenv bashio

# label configuration
{
    echo "- name: $(bashio::config 'port1')"
    echo "- name: $(bashio::config 'port2')"
    echo "- name: $(bashio::config 'port3')"
    echo "- name: $(bashio::config 'port4')"
    echo "- name: $(bashio::config 'port5')"
    echo "- name: $(bashio::config 'port6')"
    echo "- name: $(bashio::config 'port7')"
    echo "- name: $(bashio::config 'port8')"
} > /data/ports.yaml

# mandatory cmdline args
args=""
args="$args --pdu-hostname $(bashio::config 'pdu_hostname')"
args="$args --mqtt-hostname $(bashio::config 'mqtt_hostname')"

# optional cmdline args
if bashio::config.has_value 'mqtt_port'; then
    args="$args --mqtt-port $(bashio::config 'mqtt_port')"
fi
if bashio::config.has_value 'mqtt_user'; then
    args="$args --mqtt-user $(bashio::config 'mqtt_user')"
fi
if bashio::config.has_value 'mqtt_password'; then
    args="$args --mqtt-password $(bashio::config 'mqtt_password')"
fi

cmd="python3 /main.py $args"
echo "Running: $cmd"
$cmd
