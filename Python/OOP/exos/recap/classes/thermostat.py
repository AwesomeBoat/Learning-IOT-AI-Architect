
if __name__ == "__main__":
    from iot_device import IoTDevice
else :
    from classes.iot_device import IoTDevice


class Thermostat(IoTDevice):

    def __init__(self,
                 device_id: str,
                 name: str,
                 ip_address: str,
                 is_online: bool,
                 firmware_version: str,
                 target_temp : float,
                 ):
        super().__init__(device_id, name, ip_address, is_online, firmware_version)
        self._target_temp = target_temp
        self._current_temp = 0.0

    # === Getter | setter ===
        
        # target_temp
    
    @property
    def target_temp(self):
        return self._target_temp
    
    @target_temp.setter
    def target_temp(self, val):
        if not isinstance (val, float):
            try:
                val = float(val)
            except:
                raise ValueError("Target_temp must be a float.")
        self._target_temp = min(30.0,max(val,10.0))

    @property
    def current_temp(self):
        return self._current_temp
    
        


    # Methods

    def adjust_temperature(self, delta):
        new_target = self.target_temp + float(delta)
        self.target_temp = new_target
        print(f"{self.name} New temperature target : {self.target_temp}°C")
        
    def execute_diagnostics(self):
        return f"{self.name} | Temperature {self.current_temp} => {self.target_temp}"

