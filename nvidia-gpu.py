# -*- coding: utf-8 -*-
#!"C:\Program Files (x86)\PRTG Network Monitor\python\python.exe"

'''
Requests Python HTTP library is only required when using the "HTTP Push Data Advanced" sensor type The Request Python HTTP library needs to be installed with pip.  With most Python 3.x distributions this is a simple process using pip, but if you are running the "HTTP Push Data Advanced" sensor on a remote probe using the PRTG Python binary, you will need to follow specific instructions to install Python libraries with pip.

The following process should be followed to add pip to the PRTG Python distribution and install required python libraries:
1. Download https://bootstrap.pypa.io/get-pip.py into PRTGs python directory
2. cd C:\Program Files (x86)\PRTG Network Monitor\python\
3. python.exe get-pip.py
4. cd Scripts
5. pip install -r requests.txt
'''

# Libs & Modules
import logging
import time
import csv
import os
import sys
import requests

# Owned
__description__ = "PRTG NVIDIA GPU Sensor"
__author__ = "Rich Bocchinfuso"
__copyright__ = "Copyright 2021, PRTG NVIDIA GPU Sensor."
__credits__ = ["Rich Bocchinfuso"]

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Rich Bocchinfuso"
__email__ = "rbocchinfuso@gmail.com"
__status__ = "Beta"


# Global variables
log_file = 'nvidia-gpu.log'
gpu_output = 'nvidia-smi_output.csv'
xml_payload = 'nvidia-gpu_prtg_payload.xml'

# Sensor type configuration
'''
- Options are "http" for "HTTP Push Data Advanced" sensor or "pysas" for "Python Script Advanced" sensor
    - "pysas", "Python Script Advanced" sensor is a PULL sensor which runs on a Windows PRTG remote probe.
    - "http", "HTTP Push Data Advanced" sensor is a PUSH sensor that can run on any system (Windows, Linux, etc.) that satisfies the Python requirements.
- Windows systems with the PRTG probe installed can used use the "http" or "pysas" sensor type, but Linux systems must use the "http" sensor type.
- Linux, Unix, etc. systems will only support the "HTTP Push Data Advanced" sensor.
- Setting the sensor_type to "test" will allow you to run the code locally and will not communicate with the PRTG probe.
'''
# Valid sensor_type optins are 'pysas', 'http', or 'test'
sensor_type = 'test'
# Only required if the sensor_type = 'http'
# The is host running the probe that you are pushing data to
http_advanced_sensor_probe_host = 'host.domain.foo'
# The port you configured when adding the "HTTP Push Data Advanced" sensor
http_advanced_sensor_port = '5050'
# The token generated when you added the "HTTP Push Data Advanced" sensor or the token you manually entered when when adding the "HTTP Push Data Advanced" sensor
http_advanced_sensor_token = 'foo'
http_rest_post_url = 'http://{}:{}/{}'.format(
    http_advanced_sensor_probe_host, http_advanced_sensor_port, http_advanced_sensor_token)


# Configure logging
logging.basicConfig(
    filename=log_file,
    filemode='w',
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)


def log_variables():
    try:
        logging.debug('Log file: {}'.format(log_file))
        logging.debug('nvidia_smi output file: {}'.format(gpu_output))
        logging.debug('XML payload file: {}'.format(xml_payload))
        logging.debug('Sensor type: {}'.format(sensor_type))
        logging.debug('HTTP Push Data Advanced sensor port: {}'.format(
            http_advanced_sensor_port))
        logging.debug('HTTP Push Data Advanced sensor token: {}'.format(
            http_advanced_sensor_token))
        logging.debug('HTTP REST Post URL: {}'.format(http_rest_post_url))
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def check_sensor_type(sensor_type):
    try:
        if (sensor_type == 'pysas' or sensor_type == 'http' or sensor_type == 'test'):
            logging.debug(
                'Sensor type "{}" is a valid sensor type'.format(sensor_type))
        else:
            logging.debug(
                'Sensor type "{}" is an invalid sensor type'.format(sensor_type))
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def nvidia_smi(gpu_output):
    try:
        # Check for nvidia-smi csv output file and remove it if is exists
        if os.path.exists(gpu_output):
            os.remove(gpu_output)
        # Run nvidia-smi to get GPU data
        cmd = 'c:\\nvidia-smi.exe --query-gpu=timestamp,name,pci.bus_id,driver_version,pstate,pcie.link.gen.max,pcie.link.gen.current,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used --format=csv > ' + gpu_output
        logging.debug(cmd)
        os.system(cmd)
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def get_metrics(gpu_output, xml_payload):
    try:
        gpu_index = 0
        # Open and parse the CSV file
        with open(gpu_output, 'r') as data:
            for line in csv.DictReader(data):
                line = {x.translate({32: None}): y
                        for x, y in line.items()}
                logging.debug(line)

                # GPU index
                gpu_index += 1

                pstate_channel = ('GPU #' + str(gpu_index) +
                                  ' - Performance State')
                logging.debug(pstate_channel)
                pstate = line.get('pstate').strip().strip("P")
                logging.debug(pstate)
                update_xml_payload(
                    xml_payload, pstate_channel, pstate, 'Custom')

                temp_channel = ('GPU #' + str(gpu_index) + ' - Temperature')
                logging.debug(temp_channel)
                temperature = line.get('temperature.gpu').strip()
                logging.debug(temperature)
                update_xml_payload(xml_payload, temp_channel,
                                   temperature, 'Temperature')

                gpu_util = ('GPU #' + str(gpu_index) + ' - Utilization')
                logging.debug(gpu_util)
                utilization = line.get(
                    'utilization.gpu[%]').strip().split(" ", 1)
                logging.debug(utilization)
                update_xml_payload(xml_payload, gpu_util,
                                   utilization[0], 'Percent')

                gpu_mem_util = ('GPU #' + str(gpu_index) +
                                ' - Mem Utilization')
                logging.debug(gpu_mem_util)
                mem_utilization = line.get(
                    'utilization.memory[%]').strip().split(" ", 1)
                logging.debug(mem_utilization)
                update_xml_payload(xml_payload, gpu_mem_util,
                                   mem_utilization[0], 'Percent')

                gpu_mem_tot = ('GPU #' + str(gpu_index) + ' - Mem Total')
                logging.debug(gpu_mem_tot)
                mem_total = line.get('memory.total[MiB]').strip().split(" ", 1)
                logging.debug(mem_total)
                update_xml_payload(xml_payload, gpu_mem_tot,
                                   mem_total[0], 'MegaByte')

                gpu_mem_free = ('GPU #' + str(gpu_index) + ' - Mem Free')
                logging.debug(gpu_mem_free)
                mem_free = line.get('memory.free[MiB]').strip().split(" ", 1)
                logging.debug(mem_free)
                update_xml_payload(xml_payload, gpu_mem_free,
                                   mem_free[0], 'MegaByte')

                gpu_mem_used = ('GPU #' + str(gpu_index) + ' - Mem Used')
                logging.debug(gpu_mem_used)
                mem_used = line.get('memory.used[MiB]').strip().split(" ", 1)
                logging.debug(mem_used)
                update_xml_payload(xml_payload, gpu_mem_used,
                                   mem_used[0], 'MegaByte')
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def update_xml_payload(file_name, channel, value, unit):
    try:
        result_header = ("<result>")
        # logging.debug(result.header)
        channel = ("<channel>" + channel + "</channel>")
        logging.debug(channel)
        value = ("<value>" + str(value) + "</value>")
        logging.debug(value)
        unit = ("<unit>" + unit + "</unit>")
        logging.debug(unit)
        result_footer = ("</result>")
        # logging.debug(result_footer)
        data = [result_header, channel, value, unit, result_footer]
        logging.debug(data)
        log_metrics(file_name, data)
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def log_metrics(file_name, values):
    try:
        # Open the file in append & read mode ('a+')
        with open(file_name, "a+") as file_object:
            appendEOL = False
            # Move read cursor to the start of file.
            file_object.seek(0)
            # Check if file is not empty
            data = file_object.read(100)
            if len(data) > 0:
                appendEOL = True
            # Iterate over each string in the list
            for line in values:
                # If file is not empty then append '\n' before first line for
                # other lines always append '\n' before appending line
                if appendEOL == True:
                    file_object.write("\n")
                else:
                    appendEOL = True
                # Append element at the end of file
                file_object.write(line)
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def xml_header(file_name):
    try:
        prtg_header = ("<prtg>")
        with open(file_name, 'w') as file:
            file.write("{}".format(prtg_header))
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def xml_footer(file_name):
    try:
        prtg_footer = ("</prtg>")
        with open(file_name, 'a') as file:
            file.write("\n" "{}".format(prtg_footer))
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def python_advanced_sensor(file_name):
    try:
        xml_payload = open(file_name)
        lines = xml_payload.readlines()
        for line in lines:
            print(line)
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def http_push_advanced_sensor(file_name, http_rest_post_url):
    try:
        with open(file_name, 'r') as file:
            xml_payload = file.read().replace('\n', '')
            logging.debug(xml_payload)
        # set what your server accepts
        headers = {'Content-Type': 'application/xml'}
        print(requests.post(http_rest_post_url,
              data=xml_payload, headers=headers).text)
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


def main():
    try:
        log_variables()
        check_sensor_type(sensor_type)
        nvidia_smi(gpu_output)
        xml_header(xml_payload)
        get_metrics(gpu_output, xml_payload)
        xml_footer(xml_payload)
        if sensor_type == 'pysas':
            python_advanced_sensor(xml_payload)
        elif sensor_type == 'http':
            http_push_advanced_sensor(xml_payload, http_rest_post_url)
        elif sensor_type == 'test':
            logging.debug(
                'Sensor type is "{}", dry run executed locally, with no communication with the PRTG probe.'.format(sensor_type))
        else:
            logging.debug('Sensor type "{}" is invalid'.format(sensor_type))
    except Exception as e:
        logging.exception(e, exc_info=True)
        raise


if __name__ == "__main__":
    main()
