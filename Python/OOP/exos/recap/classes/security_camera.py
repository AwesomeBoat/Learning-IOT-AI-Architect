if __name__ == "__main__":

    from iot_device import IoTDevice
else:
    from classes.iot_device import IoTDevice

class SecurityCamera(IoTDevice):

    def __init__(self,
                 device_id: str,
                 name: str,
                 ip_address: str,
                 is_online: bool,
                 firmware_version: str,
                 is_recording : bool,
                 storage_max_mb : float):
        super().__init__(device_id, name, ip_address, is_online, firmware_version)
        self._is_recording = is_recording
        self._storage_used_mb = 0
        self._storage_max_mb = storage_max_mb

    
    @property
    def is_recording(self):
        return self._is_recording
    
    @is_recording.setter
    def is_recording(self,value):
        self._is_recording = value

    @property
    def storage_used_mb(self):
        return self._storage_used_mb
    
    @property
    def storage_max_mb(self):
        return self._storage_max_mb

    # Methods


    def toggle_recording(self):
        if self.is_recording == False:
            self.is_recording = True
            print(f"{self.name} is now recording")
        else:
            self.is_recording = False
            print(f"{self.name} stopped recording")

    def execute_diagnostics(self):
        return f"{self.name} | Storage left {self.storage_max_mb - self.storage_used_mb} mb | Recording {self.is_recording}"
    


