import threading

import adbutils

from titandevice.android.device import AndroidDevice


class AndroidDeviceManager(object):
    __instance: 'AndroidDeviceManager' = None
    __lock = threading.Lock()
    __all_devices: list[AndroidDevice] = None

    def __new__(cls, *args, **kwargs):
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = super(AndroidDeviceManager, cls).__new__(cls)
        return cls.__instance

    def get_all_devices(self) -> list[AndroidDevice]:
        if self.__all_devices is None:
            self.__all_devices = [
                AndroidDevice(device.serial)
                for device in adbutils.adb.device_list()
            ]
            if len(self.__all_devices) == 0:
                from titandevice._titian_exception import AnyDeviceNoFoundException
                raise AnyDeviceNoFoundException()
        return self.__all_devices

    def get_device(self, device_serial: str) -> AndroidDevice:
        for device in self.get_all_devices():
            if device.device_serial == device_serial:
                return device
        from titandevice._titian_exception import DeviceNoFoundException
        raise DeviceNoFoundException(device_serial)
