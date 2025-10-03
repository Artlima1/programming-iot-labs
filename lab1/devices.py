class Device:
    def __init__(self, deviceName, deviceID, lastUpdate, measureTypes, availableServices, servicesDetails):
        self.deviceName = deviceName
        self.deviceID = deviceID
        self.lastUpdate = lastUpdate
        self.sensors = []
        self.services = []
        self.setMeasureTypes(measureTypes)
        self.setServices(servicesDetails, availableServices)

    def setMeasureTypes(self, measureTypes):
        self.sensors = []
        for measureType in measureTypes:
            if(measureType == "Temperature"):
                self.sensors.append(TemperatureSensor())
            elif(measureType == "Humidity"):
                self.sensors.append(HumiditySensor())
            elif(measureType == "Proximity"):
                self.sensors.append(ProximitySensor())

    def getMeasureTypes(self):
        measureTypes = []
        for sensor in self.sensors:
            measureTypes.append(sensor.getType())
        return measureTypes
    
    def setServices(self, servicesDetails, availableServices):
        self.services = []
        for details in servicesDetails:
            if(details["serviceType"] == "MQTT"):
                service = MQTTService(details["topic"])
                service.setAvailable("MQTT" in availableServices)
                self.services.append(service)
            elif(details["serviceType"] == "REST"):
                service = RESTService(details["serviceIP"])
                service.setAvailable("REST" in availableServices)
                self.services.append(service)

    def getServiceTypes(self):
        serviceTypes = []
        for service in self.services:
            serviceTypes.append(service.getType())
        return serviceTypes
    
    def getAllServices(self):
        services = []
        for service in self.services:
            services.append(service)
        return services
    
    def getAvailableServices(self):
        availableServices = []
        for service in self.services:
            if(service.isAvailable()):
                availableServices.append(service)
        return availableServices
    
    def printDevice(self):
        print("Device Name: ", self.deviceName)
        print("Device ID: ", self.deviceID)
        print("Last Update: ", self.lastUpdate)
        print("Sensors: ")
        for sensor in self.sensors:
            print(" - ", sensor.getType())
        print("Services: ")
        for service in self.services:
            print(" - ", service.getType())

    def to_dict(self):
        return {
            "deviceName": self.deviceName,
            "deviceID": self.deviceID,
            "lastUpdate": self.lastUpdate,
            "measureTypes": self.getMeasureTypes(),
            "servicesDetails": [service.to_dict() for service in self.services],
            "availableServices": [service.getType() for service in self.getAvailableServices()]
        }
        

class Sensor():
    def init(self):
        pass

    def getType(self):
        return self.sensorType

class TemperatureSensor(Sensor):
    def __init__(self):
        self.sensorType = "Temperature"

class HumiditySensor(Sensor):
    def __init__(self):
        self.sensorType = "Humidity"

class ProximitySensor(Sensor):
    def __init__(self):
        self.sensorType = "Proximity"


class Service():
    def init(self):
        self.available = False

    def enable(self):
        self.available = True

    def disable(self):  
        self.available = False

    def setAvailable(self, available):
        self.available = available

    def isAvailable(self):
        return self.available

    def getType(self):
        return self.sensorType
    
    def to_dict(self):
        pass

class MQTTService(Service):
    def __init__(self, topicList):
        self.sensorType = "MQTT"
        self.topicList = topicList
    
    def to_dict(self):
        return {
            "serviceType": self.sensorType,
            "topic": self.topicList
        }

class RESTService(Service):
    def __init__(self, serviceIP):
        self.sensorType = "REST"
        self.serviceIP = serviceIP
    
    def to_dict(self):
        return {
            "serviceType": self.sensorType,
            "serviceIP": self.serviceIP
        }

