class TitanException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class AnyDeviceNoFoundException(TitanException):
    def __init__(self):
        super().__init__("Any device not found.")


class DeviceNoFoundException(TitanException):
    def __init__(self, device_serial: str):
        super().__init__(f"Device with serial {device_serial} not found.")


class PackageNoFoundException(TitanException):
    def __init__(self, device_serial: str, package_name: str):
        super().__init__(f"Package {package_name} not found on device {device_serial}.")


class DeviceMustBeRootedException(TitanException):
    def __init__(self, device_serial: str):
        super().__init__(f"Device with serial {device_serial} must be rooted.")


class AnyFridaNotInstalledException(TitanException):
    def __init__(self):
        super().__init__("Any device frida not installed.")


class FridaNotInstalledException(TitanException):
    def __init__(self, device_serial: str, frida_server_path: str):
        super().__init__(
            f"Frida not installed on device {device_serial} with path {frida_server_path}."
        )
