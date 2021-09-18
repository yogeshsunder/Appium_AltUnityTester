import subprocess

from ppadb.client import Client as AdbClient


class AltUnityAndroidPortForwarding(object):

    def __init__(self):
        self.client = AdbClient(host="127.0.0.1", port=5037)

    def forward_port_device(self, local_port=13000, device_port=13000, device_id=""):
        device = self.get_device(device_id)

        device.forward("tcp:" + str(local_port), "tcp:" + str(device_port))

    def remove_forward_port_device(self, port=13000, device_id=""):
        device = self.get_device(device_id)
        device.killforward("tcp:" + str(port))

    def get_device(self, device_id=""):
        if device_id == "":
            devices = self.client.devices()
            if len(devices) == 0:
                raise Exception("No device found")
            return devices[0]
        else:
            return self.client.device(device_id)

    def remove_all_forwards(self):
        self.client.killforward_all()
        

class AltUnityiOSPortForwarding(object):
    @staticmethod
    def forward_port_device(local_port=13000, device_port=13000, device_id=""):
        process = None
        if device_id == "":
            process = subprocess.Popen(['iproxy', str(local_port), str(device_port)])
        else:
            process = subprocess.Popen(['iproxy', str(local_port), str(device_port), device_id])
        return process.pid

    @staticmethod
    def kill_iproxy_process(pid):
        subprocess.Popen(['killall', pid]).wait()

    @staticmethod
    def kill_all_iproxy_process():
        subprocess.Popen(['killall', 'iproxy']).wait()
