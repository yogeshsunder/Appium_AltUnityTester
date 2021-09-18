from altunityrunner.commands.command_returning_alt_elements import CommandReturningAltElements
from altunityrunner.altUnityExceptions import WaitTimeOutException
from altunityrunner.commands.FindObjects.find_object import FindObject
import time
class WaitForObject(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver, by,value,camera_name, timeout, interval,enabled):
        super(WaitForObject, self).__init__(socket,request_separator,request_end,appium_driver)
        self.by=by
        self.value=value
        self.camera_name=camera_name
        self.timeout=timeout
        self.interval=interval
        self.enabled=enabled
    
    def execute(self):
        t = 0
        alt_element = None
        while (t <= self.timeout):
            try:
                alt_element = FindObject(self.socket,self.request_separator,self.request_end,self.appium_driver,self.by,self.value,self.camera_name,self.enabled).execute()
                break
            except Exception:
                print('Waiting for element ' + self.value + '...')
                time.sleep(self.interval)
                t += self.interval
        if t>=self.timeout:
            raise WaitTimeOutException('Element ' + self.value + ' not found after ' + str(self.timeout) + ' seconds')
        return alt_element