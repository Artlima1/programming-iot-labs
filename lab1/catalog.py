from devices import Device
import json
from datetime import datetime
from jsonschema import validate, ValidationError


class Catalog:
    DEVICE_SCHEMA = {
        "type": "object",
        "required": ["deviceID", "deviceName", "measureType", "availableServices", "servicesDetails"],
        "properties": {
            "deviceID": {"type": "integer"},
            "deviceName": {"type": "string"},
            "lastUpdate": {"type": "string"},
            "measureType": {"type": "array", "items": {"type": "string"}},
            "availableServices": {"type": "array", "items": {"type": "string"}},
            "servicesDetails": {"type": "array", "items": {"type": "object"}}
        }
    }

    def __init__(self):
        self.deviceList = []

    def loadFromJson(self, jsonFileName):
        self.deviceList = []
        data = json.load(open(jsonFileName))
        for deviceData in data["devicesList"]:
            try:
                validate(instance=deviceData, schema=self.DEVICE_SCHEMA)
                self.insertDevice(deviceData)
            except ValidationError as e:
                print(f"Validation error for device: {e.message}")

    def insertDevice(self, deviceData):
        device = self.getByID(deviceData["deviceID"])
        if(device is None):
            device = Device(
                deviceData["deviceName"],
                deviceData["deviceID"],
                deviceData["lastUpdate"],
                deviceData["measureType"],
                deviceData["availableServices"],
                deviceData["servicesDetails"]
            )
            self.deviceList.append(device)
        else:
            device.setName(deviceData["deviceName"])
            device.setLastUpdate(datetime.now().strftime("%Y-%m-%d %H:%M"))
            device.setMeasureTypes(deviceData["measureType"])
            device.setServices(deviceData["servicesDetails"], deviceData["availableServices"])

    def insertFromJon(self, jsonFileName):
        try:
            data = json.load(open(jsonFileName))
            validate(instance=data, schema=self.DEVICE_SCHEMA)
            self.insertDevice(data)
        except ValidationError as e:
            print(f"Validation error: {e.message}")
        except Exception as e:
            print("Invalid Json File", e)

    def getByID(self, deviceID):
        for device in self.deviceList:
            if(device.deviceID == deviceID):
                return device
        return None
    
    def getByName(self, deviceName):
        for device in self.deviceList:
            if(device.getName() == deviceName):
                return device
        return None

    def getByMeasureType(self, measureType):
        devices = []
        for device in self.deviceList:
            if(measureType in device.getMeasureTypes()):
                devices.append(device)
        return devices

    def getDevicesByServiceType(self, serviceType):
        devices = []
        for device in self.deviceList:
            if(serviceType in device.getServiceTypes()):
                devices.append(device)
        return devices

    def searchByID(self, id):
        device = self.getByID(id)
        if(device is not None):
            device.printDevice()
        else:
            print("Device not found")

    def searchByName(self, name):
        device = self.getByName(name)
        if(device is not None):
            device.printDevice()
        else:
            print("Device not found")

    def searchByMeasureType(self, measureType):
        devices = self.getByMeasureType(measureType)
        if(len(devices) > 0):
            for device in devices:
                device.printDevice()
        else:
            print("No devices found")


    def printAll(self):
        for device in self.deviceList:
            device.printDevice()
            print("---------------")

    def saveToJson(self, jsonFileName):
        data = {
            "devicesList": [device.to_dict() for device in self.deviceList]
        }
        with open(jsonFileName, 'w') as outfile:
            json.dump(data, outfile, indent=4)
    

