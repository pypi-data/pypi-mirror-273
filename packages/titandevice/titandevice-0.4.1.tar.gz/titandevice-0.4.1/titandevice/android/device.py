from adbutils import adb

from titandevice._titian_exception import DeviceMustBeRootedException
from titandevice.android.package_manager import AndroidPackageManager


class AndroidDevice:

    def __init__(self, device_serial: str):
        self.__adb_device = adb.device(device_serial)
        self.device_serial = device_serial
        self.device_ip = self.__adb_device.wlan_ip()
        self.device_is_root = self.__is_root()
        self.device_device = self.__adb_device.prop.device
        self.device_model = self.__adb_device.prop.model
        self.device_product = self.__adb_device.prop.name
        self.__package_manager = AndroidPackageManager(self.__adb_device)

    def get_package_manager(self) -> AndroidPackageManager:
        return self.__package_manager

    def get_frida_manager(
            self, frida_server_file_name_prefix, frida_server_install_path
    ):
        if not self.device_is_root:
            raise DeviceMustBeRootedException(self.device_serial)
        from titandevice.android.frida_manager import AndroidFridaManager
        return AndroidFridaManager(
            self, frida_server_file_name_prefix, frida_server_install_path
        )

    def __is_root(self):
        return self.file_exists("/system/xbin/su") or self.file_exists(
            "/system/bin/su"
        )

    def file_exists(self, path: str) -> bool:
        return 'No such file or directory' not in self.__adb_device.shell(
            f"ls {path}"
        ).strip()

    def remove_file(self, path: str):
        self.shell(f"rm {path}")

    def get_pid(self, target: str) -> int:
        result = self.shell(f"ps -A | grep {target}")
        if result == "":
            return -1
        return int(result.split()[1])

    def get_all_files(self, path: str) -> list[str]:
        return self.shell(f"ls {path}").strip().split()

    def shell(self, cmd: str) -> str:
        if self.device_is_root:
            return self.__adb_device.shell(f"su -c {cmd}")
        return self.__adb_device.shell(cmd)

    def kill_process(self, pid: int):
        self.shell(f"kill -9 {pid}")

    #
    # def __dict__(self):
    #     return {
    #         'serial': self.device_serial,
    #         'product': self._adb_device.prop.name,
    #         'model': self._adb_device.prop.device_model,
    #         'device': self._adb_device.prop.device_device,
    #         'is_root': self.device_is_root,
    #         "ip": self.ip
    #     }
    #
    # def reboot(self):
    #     self._adb_device.reboot()
    #
    # def wlan_ip(self):
    #     return self._adb_device.wlan_ip()
    #
    # def push(self, local_path: str, remote_path: str):
    #     self._adb_device.push(local_path, remote_path)
    def dict(self):
        return {
            'serial': self.device_serial,
            'product': self.device_product,
            'model': self.device_model,
            'device': self.device_device,
            'is_root': self.device_is_root,
            "ip": self.device_ip
        }

    def push(self, source, destination):

        if self.file_exists(destination):
            self.remove_file(destination)
        self.__adb_device.push(source, destination)

    def rename(self, old_name, new_name):
        self.shell(f"mv {old_name} {new_name}")
