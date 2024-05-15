import apkutils2
from adbutils import AdbDevice, RunningAppInfo
from titandevice._titian_exception import *


class AndroidPackageManager:
    __adb_device: AdbDevice

    def __init__(self, adb_device):
        self.__adb_device = adb_device

    def get_installed_packages(self) -> list[str]:
        return self.__adb_device.list_packages()

    def get_package_info(self, package_name):
        if not self.is_package_installed(package_name):
            raise PackageNoFoundException(self.__adb_device.serial, package_name)
        return self.__adb_device.app_info(package_name)

    def is_package_installed(self, package_name: str) -> bool:
        return package_name in self.get_installed_packages()

    def uninstall_package(self, package_name) -> bool:
        self.__adb_device.uninstall(package_name)
        return not self.is_package_installed(package_name)

    def install_package(self, local_package_path: str, uninstall=True, no_launch=True):
        apk = apkutils2.APK(local_package_path)
        package_name = apk.manifest.package_name

        self.__adb_device.install(
            local_package_path, uninstall=uninstall, nolaunch=no_launch, silent=True
        )
        return self.is_package_installed(package_name)

    def get_current_app(self) -> RunningAppInfo:
        return self.__adb_device.app_current()

    def start(self, package_name):
        self.__adb_device.app_start(package_name)
        return self.get_current_app().package == package_name

    def stop(self, package_name):
        self.__adb_device.app_stop(package_name)
        return self.get_current_app().package != package_name
