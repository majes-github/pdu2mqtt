# pdu2mqtt Home Assistant add-on

![pdu2mqtt Logo](logo.png)

This add-on allows to control [Intellinet's Smart PDU 163682](https://intellinetnetwork.eu/products/intellinet-en-19-intelligent-8-port-pdu-163682) via MQTT. pdu2qtt registers itself to Home Assistant via MQTT.

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fmajes-github%2Fpdu2mqtt)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg

## Configuration

The following configuration parameters apply:

| Parameter  | Default Value  | Type | Notes |
|---|---|---|---|
| pdu_hostname | pdu  | String | IP address or FQDN of PDU |
| mqtt_hostname | core-mosquitto | String | IP address or FQDN of MQTT broker
| mqtt_port | (optional) | Integer | MQTT broker port number (if not 1883) |
| mqtt_user | (optional) | String | Username for MQTT authentication |
| mqtt_password | (optional) | String | Password for MQTT authentication |
| port1 | Port 1 | String | Label for Home Assistant entity of socket #1 |
| ... | ... | ... | ... |
| port8 | Port 8 | String | Label for Home Assistant entity of socket #8 |
