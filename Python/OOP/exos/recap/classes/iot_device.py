from abc import ABC, abstractmethod 

class IoTDevice(ABC):

    def __init__(self, 
                 device_id : str, 
                 name : str, 
                 ip_address : str, 
                 is_online : bool, 
                 firmware_version : str):
        
        self._device_id = device_id
        self._name = name
        self._ip_address = ip_address
        self._is_online = is_online
        self._firmware_version = firmware_version

    
    # === Getter | Setter ===
        
        # Device_id
    
    @property
    def device_id(self):
        return self._device_id
    
    @device_id.setter
    def device_id(self, val):
        if not isinstance(val, str):
            raise ValueError("Device ID must be a string.")
               
        if not val.strip():
            raise ValueError("Device ID must not be empty. ")
        
        self._device_id = val


        # Name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise ValueError("Device name must be a string.")

        if not val.strip():
            raise ValueError("Device name must not be empty.")
    
        self._name = val

        # ip_address

    @property
    def ip_address(self):
        return self._ip_address
    
    @ip_address.setter
    def ip_address(self, val):
        if not isinstance(val, str):
            raise ValueError("Ip_address name must be a string.")

        if not val.strip():
            raise ValueError("Ip_address name must not be empty.")
    
        self._ip_address = val

    # is_online
        
    @property
    def is_online(self):
        return self._is_online
    
    @is_online.setter
    def is_online(self, val):
        if not isinstance(val, bool):
            raise ValueError("Is_online must be a boolean.")
        self._is_online = val

    # firware version
        
    @property
    def firmware_version(self):
        return self._firmware_version
    
    @firmware_version.setter
    def firmware_version(self, val):
        if not isinstance(val, str):
            raise ValueError("Firmware version must be a string")
        
        if not val.strip():
            raise ValueError("Firmware_version must not be empty.")
    
        self._firmware_version = val
        
    # Methods
    @abstractmethod
    def execute_diagnostics(self):
        pass








