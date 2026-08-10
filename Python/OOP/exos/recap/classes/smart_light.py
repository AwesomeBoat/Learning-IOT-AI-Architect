if __name__ == "__main__":
    from iot_device import IoTDevice
else :
    from classes.iot_device import IoTDevice


class SmartLight(IoTDevice):

    def __init__(self,
                 device_id: str,
                 name: str,
                 ip_address: str,
                 is_online: bool,
                 firmware_version: str, 
                 brightness : int,
                 color : str):
        super().__init__(device_id, name, ip_address, is_online, firmware_version)
        self._brightness = brightness
        self._color = color


    # === Getter | Seter ===
        # brightness
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self,value):
        if not isinstance(value, float):
            try:
                value = float(value)
            except:
                raise ValueError("Brightness must be a float")
        self._brightness = max(0,min(value,100))

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        valid_colors=  ["red","green","blue","white"]
        if value in valid_colors:
            self._color = value
        else: 
            raise ValueError(f"Color must be : {valid_colors}")
        
    # Methods
        
    def set_brightness(self,level):
        self.brightness = level


    def execute_diagnostics(self):
        'Return a diagnostic about light device : online, luminosity and color'
        return f"{self.name} | online : {self.is_online} | brightness : {self.brightness}% | color : {self._color}"

    

if __name__ == "__main__" :
    light = SmartLight("zze","zeze","127.0",False,"1.2",55,"white")
    print(light.execute_diagnostics())