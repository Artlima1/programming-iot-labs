from devices import Device
import json
from datetime import datetime


class Catalog:
    def __init__(self):
        self.deviceList = []

    def loadFromJson(self, jsonFileName):
        self.deviceList = []
        data = json.load(open(jsonFileName))
        for deviceData in data["devicesList"]:
            self.insertDevice(deviceData)

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
            device.name = deviceData["deviceName"]
            device.setSensors(deviceData["measureType"])
            device.setServices(deviceData["servicesDetails"], deviceData["availableServices"])
            device.lastUpdate = datetime.now().strftime("%Y-%m-%d %H:%M")

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
    

