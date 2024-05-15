import click

from titandevice import PackageNoFoundException
from titandevice.android._frida_manager import _AndroidFridaManager
from titandevice.android.device_manager import AndroidDeviceManager

package_name = 'com.sina.weibo'
device_serial = '19301FDF6006EP'
frida_version = '16.2.1'
input_frida_server_paths = [
    '/home/mark/workspace/tools/frida-server/frida-server-16.2.1-android-arm64',
    '/home/mark/workspace/tools/frida-server/frida-server-16.1.11-android-arm64',
    '/home/mark/workspace/tools/frida-server/frida-server-16.2.0-android-arm64'
]
if __name__ == '__main__':
    try:
        device_manager = AndroidDeviceManager()
        # devices = device_manager.get_all_devices()
        # device_serial = questionary.select(
        #     message='请选择一个设备:',
        #     choices=[device.device_serial for device in devices]
        # ).ask()
        device = device_manager.get_device(device_serial)
        click.echo(
            f'您选择的设备是: {device.dict()}'
        )
        package_manager = device.get_package_manager()
        # installed_packages = package_manager.get_installed_packages()
        # click.echo('已安装的包:')
        # for package in installed_packages:
        #     click.echo(f'{package}')
        # package_name = 'com.almatar'
        package_info = package_manager.get_package_info(package_name)
        click.echo(f'包信息: {package_info}')
        # is_ok = package_manager.uninstall_package(package_name)
        # click.echo(f'卸载结果: {is_ok}')
        # is_ok = package_manager.start(package_name)
        # click.echo(f'启动结果: {is_ok}')
        # is_ok = package_manager.stop(package_name)
        # click.echo(f'停止结果: {is_ok}')
        frida_manager: _AndroidFridaManager = device.get_frida_manager(
            "frida-server", "/data/local/tmp/"
        )
        frida_devices = frida_manager.get_all_frida()
        click.echo('Frida列表:')
        #     is_ok = frida.start()
        #     click.echo(f'启动结果: {is_ok}')
        #     is_ok = frida.stop()
        #     click.echo(f'停止结果: {is_ok}')
        # for input_frida_server_path in input_frida_server_paths:
        #     is_ok = frida_manager.install_frida(input_frida_server_path)
        #     click.echo(f'安装结果: {is_ok}')
    except PackageNoFoundException as e:
        click.echo(f'包未找到: {e} 开始安装...')
        is_ok = AndroidDeviceManager().get_device(
            '19301FDF6006EP'
        ).get_package_manager().install_package(
            '/home/mark/workspace/stability_laboratory/weibo/apks/14.4.1.apk'
        )
        click.echo(f'安装结果: {is_ok}')
