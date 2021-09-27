# PRTG NVIDIA GPU Sensor

## Summary

This NVIDIA GPU sensor is written in Python and uses the PRTG "Python Advanced Script" or "HTTP Push Data Advanced" sensor to collect NVIDIA GPU telemetry data.

_Note: If you have any questions or comments you can always use GitHub discussions, or DM me on the twitter @rbocchinfuso._

## Features

- Supports for Python Script Advanced sensor (pull sensor) and HTTP Push Data Advanced sensor (push sensor)
- Support for Windows systems using the Python Script Advanced sensor (pull sensor) and HTTP Push Data Advanced sensor (push sensor)
- Support for Linux (or other OS with Python 3.x distribution support) using the HTTP Push Data Advanced sensor (push sensor)
- Supports single of multi GPU systems
- Collects the following metrics:
  - GPU Performance State
  - GPU Temperature
  - GPU Utilization
  - GPU Memory Utilization
  - GPU Total Memory
  - GPU Used Memory
  - GPU Free Memory

## Requirements

- nvidia-smi binary
  - The ```nvidia-smi``` binary is typically installed with your NVIDIA GPU display drivers.
    - E.g., on Windows the nvidia-smi.exe binary is typically located in "C:\Windows\System32"
  - Copy the ```nvidia-smi``` binary to the root of your system (e.g. C:\)
    - Other locations will work, for simplicity I use the ```os.system``` call to run the nvidia-smi binary and os.system will have issues when the paths contains spaces.

### Python Script Advanced sensor run mode

- Windows PRTG Probe Host
  - PRTG probe needs to be installed on the system where you will run the sensor.
  - Uses Python 3.7.7 32-bit interpreter installed by PRTG Probe. Typically located at ```C:\Program Files (x86)\PRTG Network Monitor\python\python.exe```

### HTTP Push Data Advanced sensor run mode

- Any host capable of running a Python 3.x distribution
- Requests Python library


  ```text
  Requests Python HTTP library is only required when using the "HTTP Push Data Advanced" sensor type The Request Python HTTP library needs to be installed with pip.  With most Python 3.x distributions this is a simple process using pip, but if you are running the "HTTP Push Data Advanced" sensor on a remote probe using the PRTG Python binary, you will need to follow specific instructions to install Python libraries with pip.

  The following process should be followed to add pip to the PRTG Python distribution and install required python libraries:
  1. Download https://bootstrap.pypa.io/get-pip.py into PRTGs python directory
  2. cd C:\Program Files (x86)\PRTG Network Monitor\python\
  3. python.exe get-pip.py
  4. cd Scripts
  5. pip install -r requests.txt
  ```

_Note: If you are using the Python Script Advanced sensor on windows and want to avoid installing pip, be sure to comment out ```import requests``` in nvidia-gpu.py. If you set the ```sensor-type = "pyssas"``` and do not install pip and the HTTP Requests library (requests) or comment out ```import requests``` the script will through an exception._

- Scheduled job to run HTTP Push Data Advanced sensor.  This can be done using the native OS scheduler such as the Windows job scheduler or cron.
  Example cron job

  ```bash
  */3 * * * * nvidia-gpu.py >/dev/null 2>&1
  ```

## Usage

- Download code from GitHub

  ```bash
  git clone https://github.com/CC-Digital-Innovation/prtg-nvidia-gpu-sensor.git
  ```

  _Note: If you don't have Git installed you can also just grab the zip:
  [https://github.com/CC-Digital-Innovation/prtg-nvidia-gpu-sensor/archive/master.zip](https://github.com/CC-Digital-Innovation/prtg-nvidia-gpu-sensor/archive/master.zip)_

- Copy nvidia-gpu.py to the "Custom Sensor" director on the PRTG Probe.  This location is likely "C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python"

- Add "Python Script Advanced" sensor to prove.
  - Be sure to select "nvidia-gpu.py" as the script when adding the sensor.

- Sensor type options
  - Options are ```http``` for "HTTP Push Data Advanced" sensor or ```pysas``` for "Python Script Advanced" sensor
    - ```pysas```, "Python Script Advanced" sensor is a PULL sensor which runs on a Windows PRTG remote probe.
    - ```http```, "HTTP Push Data Advanced" sensor is a PUSH sensor that can run on any system (Windows, Linux, etc.) that satisfies the Python requirements.
  - Windows systems with the PRTG probe installed can used use the "http" or ```pysas``` sensor type, but Linux systems must use the ```http``` sensor type.
  - Linux, Unix, etc. systems will only support the "HTTP Push Data Advanced" sensor.
  - Setting the sensor_type to "test" will allow you to run the code locally and will not communicate with the PRTG probe.

### Configuration variables
_Modify settings in the nvidia-gpy.py script_
```python
# Sensor type configuration

# Valid sensor_type optins are 'pysas', 'http', or 'test'
sensor_type = 'pysas'
# Only required if the sensor_type = 'http'
# The is host running the probe that you are pushing data to
http_advanced_sensor_probe_host = 'host.domain.foo'
# The port you configured when adding the "HTTP Push Data Advanced" sensor
http_advanced_sensor_port = '5050'
# The token generated when you added the "HTTP Push Data Advanced" sensor or the token you manually entered when when adding the "HTTP Push Data Advanced" sensor
http_advanced_sensor_token = 'token'
http_rest_post_url = 'http://{}:{}/{}'.format(
    http_advanced_sensor_probe_host, http_advanced_sensor_port, http_advanced_sensor_token)
```

## Compatibility

### Windows based probe with PRTG Python (3.7.7 32-bit) Python distribution

- Python Script Advanced Sensor type (```sensor_type = "pysas"```)

### Windows, Linus or any host OS with a Python 3.x distribution and nvidia_smi binary

- HTTP Push Data Advanced sensor type (```sensor_type = "http"```)

_Note: This code was built and tested on Windows 10 using the PRTG Python 3.7.7 32-bit interpreter.

## Disclaimer

The code provided in this project is an open source example and should not be treated as an officially supported product. Use at your own risk. If you encounter any problems, please log an [issue](https://github.com/CC-Digital-Innovation/prtg-nvidia-gpu-sensor/issues).

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request ツ

## History

- See [CHANGELOG.md](https://github.com/CC-Digital-Innovation/prtg-nvidia-gpu-sensor/blob/main/CHANGELOG.md)

## Credits

Rich Bocchinfuso <<rbocchinfuso@gmail.com>>

## License

MIT License

Copyright (c) [2021] [Richard J. Bocchinfuso]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
