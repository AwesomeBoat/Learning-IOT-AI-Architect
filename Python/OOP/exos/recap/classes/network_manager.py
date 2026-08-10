if __name__ == "__name__":

    from iot_device import IoTDevice

else :
    from classes.iot_device import IoTDevice


from random import randint

class NetworkManager:

    def __init__(self) -> None:
        self._devices = {}

    
    @property
    def devices(self):
        return self._devices


    # Methods
    def add_device(self, device):
        'Add a device to the network manager'
        print(device.__class__.__name__)
        print(isinstance(device, IoTDevice))
        
        match str(device.__class__.__name__):
            case "SecurityCamera":
                self.devices[device.device_id] = device
            case "SmartLight":
                self.devices[device.device_id] = device
            case "Thermostat":
                self.devices[device.device_id] = device
            case _:
                raise TypeError("Device must be an IoT Device")

    def remove_device(self,device_id):
        if not device_id in self.devices :
            raise ValueError(f"{device_id} is not in the devices list")

        del self.devices[device_id]
        print(f"{device_id} removed from network manager")
        
    def get_device(self,device_id):
        if not device_id in self.devices:
            print(f"{device_id} is not part of the system")
        else:
            return self.devices[device_id]
        
    def ping_all(self):
        for device in self.devices :

            ping_success = randint(0,1) # Random as we can't ping them for now
            print(50*"-")
            if ping_success: 
                print(f"Device {self.devices[device].name} is Online")
            else :
                print(f"Device {self.devices[device].name} is Offline")

    def run_global_diagnostics(self):
        print(f"Network have {len(self.devices)} devices")
        print(50*"=")
        print("\n")
        for device_key in self.devices:
            print(self.devices[device_key].execute_diagnostics())
            print(50*"-")

