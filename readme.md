# PyXiaomiYi

To use the API you must setup the camera as described in *Initial Settings* (Wifi connection and file creation).
You can then use the API. Some examples are shown in *API*.

## Initial settings

##### Wifi
Access to the camera through Wifi:
- *SSID:* YDXJ\_[last 7 digits of SN]
- *Default pass:* 1234567890
- *Securtiy:* WPA2-Personal
- *Camera IP:* 192.168.42.1

```Shell
# Connect to the Wifi of the camera (or use an interface)
# 0000000 should be replaced with the numbers corresponding to your camera
nmcli dev wifi con YDXJ_0000000 password 1234567890
```

##### Telnet/Shell
To have access to the shell in the _Xiami Yi_, you must have a `enable_info_display.script` file at the root of the SD card.
Then you can access the camera shell through telnet

```shell
# Create file on the SD_card
touch $SD_PATH/enable_info_display.script

# Turn on the camera...
# Connect to Wifi...

# Access the shell (login is 'root')
telnet 198.168.42.1 23
```

## API



## Thanks to:

This work is build up from: \\
https://github.com/deltaflyer4747/Xiaomi_Yi \\
https://gist.github.com/franga2000/1be2aa18cb3409e57af149883c06e34a
