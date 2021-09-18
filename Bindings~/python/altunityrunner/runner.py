import json
import re
import socket
import subprocess
import time
import multiprocessing

from altunityrunner.altUnityExceptions import *
from deprecated import deprecated
from altunityrunner.commands import *
from altunityrunner.altElement import AltElement
from altunityrunner.player_pref_key_type import PlayerPrefKeyType
BUFFER_SIZE = 1024

class AltrunUnityDriver(object):

    def __init__(self, appium_driver,  platform, TCP_IP='127.0.0.1',TCP_PORT=13000, timeout=60,request_separator=';',request_end='&',device_id="",log_flag=False):
        self.TCP_PORT = TCP_PORT
        self.request_separator=request_separator
        self.request_end=request_end
        self.log_flag=log_flag
        self.appium_driver=None
        if (appium_driver != None):
            self.appium_driver = appium_driver

        while timeout > 0:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((TCP_IP, TCP_PORT))
                self.socket.settimeout(5)
                print("Get server Version")
                GetServerVersion(self.socket, self.request_separator, self.request_end).execute()
                break
            except Exception as e:
                if not self.socket==None:
                    self.stop()
                print(e)
                print('AltUnityServer not running on port ' + str(self.TCP_PORT) +
                      ', retrying (timing out in ' + str(timeout) + ' secs)...')
                timeout -= 5
                time.sleep(5)

        if timeout <= 0:
            raise Exception('Could not connect to AltUnityServer on: '+ TCP_IP +':'+ str(self.TCP_PORT))
        EnableLogging(self.socket,self.request_separator,self.request_end,self.log_flag).execute()

    def stop(self):
        CloseConnection(self.socket,self.request_separator,self.request_end).execute()          

    def call_static_methods(self, type_name, method_name, parameters, type_of_parameters = '',assembly=''):
        return CallStaticMethods(self.socket,self.request_separator,self.request_end,type_name,method_name,parameters,type_of_parameters,assembly).execute()
     
    def get_all_elements(self,camera_name='',enabled=True):
        return GetAllElements(self.socket,self.request_separator,self.request_end,self.appium_driver,camera_name,enabled).execute()

    def find_object(self,by,value,camera_name='',enabled=True):
        return FindObject(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,enabled).execute()
        
    def find_object_which_contains(self,by,value,camera_name='',enabled=True):
        return FindObjectWhichContains(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,enabled).execute()

    def find_objects(self,by,value,camera_name='',enabled=True):
        return FindObjects(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,enabled).execute()
    
    def find_objects_which_contains(self,by,value,camera_name='',enabled=True):
        return FindObjectsWhichContains(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,enabled).execute()
    
    @deprecated(version='1.4.0',reason="Use find_object instead")
    def find_element(self, name,camera_name='',enabled=True):
        return FindElement(self.socket,self.request_separator,self.request_end,self.appium_driver,name,camera_name,enabled).execute()

    @deprecated(version='1.4.0',reason="Use find_object_which_contains instead")
    def find_element_where_name_contains(self, name,camera_name='',enabled=True):
        return FindElementWhereNameContains(self.socket,self.request_separator,self.request_end,self.appium_driver,name,camera_name,enabled).execute()

    @deprecated(version='1.4.0',reason="Use find_objects instead")
    def find_elements(self, name,camera_name='',enabled=True):
        return FindElements(self.socket,self.request_separator,self.request_end,self.appium_driver,name,camera_name,enabled).execute()        

    @deprecated(version='1.4.0',reason="Use find_objects_which_contains instead")
    def find_elements_where_name_contains(self, name,camera_name='',enabled=True):
        return FindElementsWhereNameContains(self.socket,self.request_separator,self.request_end,self.appium_driver,name,camera_name,enabled).execute()

    def get_current_scene(self):
        return GetCurrentScene(self.socket,self.request_separator,self.request_end,self.appium_driver).execute()

    def swipe(self, x_start, y_start, x_end, y_end, duration_in_secs):
        return Swipe(self.socket,self.request_separator,self.request_end,x_start,y_start,x_end,y_end,duration_in_secs).execute()

    def swipe_and_wait(self, x_start, y_start, x_end, y_end, duration_in_secs):
        return SwipeAndWait(self.socket,self.request_separator,self.request_end,x_start,y_start,x_end,y_end,duration_in_secs).execute()
    
    def multipoint_swipe(self, positions, duration_in_secs):
        return MultipointSwipe(self.socket,self.request_separator,self.request_end,positions,duration_in_secs).execute()
    
    def multipoint_swipe_and_wait(self, positions, duration_in_secs):
        return MultipointSwipeAndWait(self.socket,self.request_separator,self.request_end,positions,duration_in_secs).execute()
    
    def tilt(self, x, y, z):
        return Tilt(self.socket,self.request_separator,self.request_end,x,y,z).execute()

    def hold_button(self, x_position, y_position, duration_in_secs):
        return Swipe(self.socket, self.request_separator, self.request_end, x_position, y_position, x_position, y_position, duration_in_secs).execute()

    def hold_button_and_wait(self, x_position, y_position, duration_in_secs):
        return SwipeAndWait(self.socket, self.request_separator, self.request_end, x_position, y_position, x_position, y_position, duration_in_secs).execute()

    def press_key(self, keyName,power=1,duration=1):
        return PressKey(self.socket,self.request_separator,self.request_end,keyName,power,duration).execute()

    def press_key_and_wait(self,keyName,power=1,duration=1):
        return PressKeyAndWait(self.socket,self.request_separator,self.request_end,keyName,power,duration).execute()

    def move_mouse(self, x, y, duration):
        return MoveMouse(self.socket,self.request_separator,self.request_end,x,y,duration).execute()
        
    def move_mouse_and_wait(self, x, y, duration):
        return MoveMouseAndWait(self.socket,self.request_separator,self.request_end,x,y,duration).execute()

    def scroll_mouse(self, speed, duration):
        return ScrollMouse(self.socket,self.request_separator,self.request_end,speed,duration).execute()

    def scroll_mouse_and_wait(self,speed, duration):
        return ScrollMouseAndWait(self.socket,self.request_separator,self.request_end,speed,duration).execute()    

    def set_player_pref_key(self, key_name, value, key_type):
        return SetPlayerPrefKey(self.socket,self.request_separator,self.request_end,key_name,value,key_type).execute()

    def get_player_pref_key(self, key_name, key_type):
        return GetPlayerPrefKey(self.socket,self.request_separator,self.request_end,key_name,key_type).execute()
    
    def delete_player_pref_key(self, key_name):
        return DeletePlayerPrefKey(self.socket,self.request_separator,self.request_end,key_name).execute()

    def delete_player_prefs(self):
        return DeletePlayerPref(self.socket,self.request_separator,self.request_end).execute()

    def load_scene(self, scene_name):
        return LoadScene(self.socket,self.request_separator,self.request_end,scene_name).execute()

    def set_time_scale(self, time_scale):
        return SetTimeScale(self.socket,self.request_separator,self.request_end,time_scale).execute()

    def get_time_scale(self):
        return GetTimeScale(self.socket,self.request_separator,self.request_end).execute()

    def wait_for_current_scene_to_be(self, scene_name, timeout=30, interval=1):
        return WaitForCurrentSceneToBe(self.socket,self.request_separator,self.request_end,self.appium_driver,scene_name,timeout,interval).execute()

    @deprecated(version='1.4.0',reason="Use wait_for_object instead")
    def wait_for_element(self, name,camera_name='', timeout=20, interval=0.5,enabled=True):
        return WaitForElement(self.socket,self.request_separator,self.request_end,self.appium_driver,name,camera_name,timeout,interval,enabled).execute()

    @deprecated(version='1.4.0',reason="Use wait_for_object_which_contains instead")
    def wait_for_element_where_name_contains(self, name,camera_name='', timeout=20, interval=0.5,enabled=True):
        return WaitForElementWhereNameContains(self.socket,self.request_separator,self.request_end,self.appium_driver,name,camera_name,timeout,interval,enabled).execute()

    @deprecated(version='1.4.0',reason="Use wait_for_object_to_not_be_present instead")
    def wait_for_element_to_not_be_present(self, name,camera_name='', timeout=20, interval=0.5,enabled=True):
        return WaitForElementToNotBePresent(self.socket,self.request_separator,self.request_end,self.appium_driver,name,camera_name,timeout,interval,enabled).execute()

    @deprecated(version='1.4.0',reason="Use wait_for_object_with_text instead")
    def wait_for_element_with_text(self, name, text,camera_name='', timeout=20, interval=0.5,enabled=True):
        return WaitForElementWithText(self.socket,self.request_separator,self.request_end,self.appium_driver,name,text,camera_name,timeout,interval,enabled).execute()

    def wait_for_object(self, by,value,camera_name='', timeout=20, interval=0.5,enabled=True):
        return WaitForObject(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,timeout,interval,enabled).execute()

    def wait_for_object_which_contains(self, by,value,camera_name='', timeout=20, interval=0.5,enabled=True):
        return WaitForObjectWhichContains(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,timeout,interval,enabled).execute()
    
    def wait_for_object_to_not_be_present(self, by,value,camera_name='', timeout=20, interval=0.5,enabled=True):
        return WaitForObjectToNotBePresent(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,timeout,interval,enabled).execute()

    def wait_for_object_with_text(self, by,value, text,camera_name='', timeout=20, interval=0.5,enabled=True):
        return WaitForObjectWithText(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,text,camera_name,timeout,interval,enabled).execute()

    def tap_at_coordinates(self,x,y):
        return TapAtCoordinates(self.socket,self.request_separator,self.request_end,self.appium_driver,x,y).execute()

    def tap_custom(self, x, y, count, interval=0.1):
        return TapCustom(self.socket,self.request_separator,self.request_end,self.appium_driver,x,y,count,interval).execute()
    
    @deprecated(version='1.4.0',reason="Use find_object instead")
    def find_element_by_component(self, component_name,assembly_name='',camera_name='',enabled=True):
        return FindElementByComponent(self.socket,self.request_separator,self.request_end,self.appium_driver,component_name,assembly_name,camera_name,enabled).execute()

    @deprecated(version='1.4.0',reason="Use find_objects instead")
    def find_elements_by_component(self, component_name,assembly_name='',camera_name='',enabled=True):
        return FindElementsByComponent(self.socket,self.request_separator,self.request_end,self.appium_driver,component_name,assembly_name,camera_name,enabled).execute()
    
    def get_png_screenshot(self,path):
        GetPNGScreenshot(self.socket,self.request_separator,self.request_end,path).execute()
