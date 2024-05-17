# Septentrio GPS



**Source Code**: [https://gitlab.com/roxautomation/components/septentrio-gps](https://gitlab.com/roxautomation/components/septentrio-gps)


## Usage

get docker image (use tag for version)

    registry.gitlab.com/roxautomation/components/septentrio-gps:latest


## Environment Variables

Configuration is defined in `config.py`
Set these environment variables to configure MQTT and GPS settings:

### MQTT
- **MQTT_HOST**: MQTT server host (default: `"localhost"`).
- **MQTT_PORT**: MQTT server port (default: `1883`).
- **MQTT_POSITION_TOPIC**: MQTT topic for GPS positions (default: `"/gps/position"`).
- **MQTT_DIRECTION_TOPIC**: MQTT topic for GPS directions (default: `"/gps/direction"`).

### GPS
- **GPS_PORT**: Serial port for GPS (default: `"/dev/gps_nmea"`).
- **GPS_BAUD**: Baud rate for GPS serial communication (default: `115200`).
- **GPS_REF**: gps reference point, provide lat,lon, example: `GPS_REF="51.123,6.456"`

**Example launch with custom parameters**

    docker run \
    -e MQTT_HOST=192.168.1.100 \
    -e MQTT_PORT=8883 \
    -e GPS_PORT=/dev/ttyS0 \
    registry.gitlab.com/roxautomation/components/septentrio-gps:latest





### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code.


**Online documentation**: [https://roxautomation.gitlab.io/components/septentrio-gps/](https://roxautomation.gitlab.io/components/septentrio-gps/)

## Development

There should be mqtt broker available on the host system. If not, there is a docker image for that:

    docker run -d --name mosquitto --restart unless-stopped -p 1883:1883 registry.gitlab.com/roxautomation/images/mosquitto:latest

* Open in VSCode devcontainer. Virtual com port is located at `/tty/tty_nmea_rx`
* Pre-recorded nmea stream can be sent to com port with `replay_data.py` in `integration/data` folder.


## TODO

Current setup works, but it can always be made better.

* add tests
* Use uart ports instead of usb. This will make system more robust.
