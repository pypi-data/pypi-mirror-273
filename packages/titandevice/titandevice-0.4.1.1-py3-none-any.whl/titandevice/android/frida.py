import os.path
import subprocess

from adbutils import adb_path

from titandevice import FridaNotInstalledException
from titandevice.utils import get_file_name_from_path


class AndroidFrida:

    @staticmethod
    def __check_is_installed(func):

        def wrapper(self, *args, **kwargs):
            if not self.__android_device.file_exists(self.__frida_server_full_path):
                raise FridaNotInstalledException(
                    self.__android_device.device_serial, self.__frida_server_full_path
                )
            return func(self, *args, **kwargs)

        return wrapper

    def __init__(self, android_device, frida_server_executable_file_path):
        from titandevice.android.device import AndroidDevice
        self.__android_device: AndroidDevice = android_device
        self.__frida_server_full_path = frida_server_executable_file_path
        self.__frida_server_path = os.path.abspath(frida_server_executable_file_path)
        self.__frida_server_name = get_file_name_from_path(
            frida_server_executable_file_path
        )
        self.__version = self.__get_version()
        self.__is_running = self.__check_if_running()

    @property
    def is_running(self):
        return self.__is_running

    @property
    def version(self):
        return self.__version

    @property
    def frida_server_name(self):
        return self.__frida_server_name

    @property
    def frida_server_path(self):
        return self.__frida_server_path

    @property
    def frida_server_full_path(self):
        return self.__frida_server_full_path

    def __check_if_running(self):
        return self.__android_device.get_pid(self.__frida_server_name) != -1

    @__check_is_installed
    def __get_version(self):
        return self.__android_device.shell(
            f"su -c {self.__frida_server_full_path} --version"
        ).strip()

    def dict(self):
        return {
            'frida_server_name': self.__frida_server_name,
            'frida_server_path': self.__frida_server_full_path,
            'is_running': self.__is_running,
            'version': self.__version
        }

    @__check_is_installed
    def start(self):
        if not self.__is_running:
            subprocess.Popen(
                [adb_path(), '-s', self.__android_device.device_serial, 'shell',
                 'nohup',
                 'su -c', self.__frida_server_full_path, '&']
            )
        self.__is_running = self.__check_if_running()
        return self.__is_running

    @__check_is_installed
    def stop(self):
        if self.is_running:
            self.__android_device.kill_process(
                self.__android_device.get_pid(self.__frida_server_name)
            )
        self.__is_running = self.__check_if_running()
        return not self.__is_running

    def uninstall(self):
        self.__android_device.remove_file(self.__frida_server_full_path)
        return not self.__android_device.file_exists(self.__frida_server_full_path)
