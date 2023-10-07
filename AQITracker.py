import serial, time
from time import localtime, strftime

# datadog imports
from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_payload import MetricsPayload
from datadog_api_client.v1.model.point import Point
from datadog_api_client.v1.model.series import Series

port = serial.Serial("/dev/serial0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.5)

def sendDataDog(data, name, tag):
    body = MetricsPayload(
    series=[
        Series(
            metric=name,
            type="gauge",
            points=[Point([time.now().timestamp(), data])],
            tags=[tag],
        )
    ])

    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.submit_metrics(body=body)
        print(response)

def main():
    
    try:
        data = port.read(32);
        if ord(data[0]) == 66 and ord(data[1]) == 77:
            suma = 0
            for a in range(30):
                suma += ord(data[a])
            if suma == ord(data[30])*256+ord(data[31]):
                PM25 = int(ord(data[6])*256+ord(data[7]))
                PM10 = int((ord(data[8])*256+ord(data[9]))/0.75)
                print('PM2.5: {} ug/m3'.format(PM25))
                print('PM10: {} ug/m3'.format(PM10))
                sendDataDog(min, "ProjectRoom_PM25", "env:AQITracker")

    except Exception as ex:
        print(ex)