import subprocess

class Device:
    def __init__(self, adb_instance=None):
        self.adb_instance = adb_instance
        self.is_connected = False
        self.device = self.adb_instance.device

    def device_connected(func):
        def wrapper(self, *args, **kwargs):
            if not self.is_connected:
                print("¡Error! El dispositivo no está conectado.")
            else:
                return func(self, *args, **kwargs)
        return wrapper

  
    def get_model(self):
        resultado = subprocess.run(f'adb -s {self.device} shell getprop ro.product.model', capture_output=True, text=True, shell=True)
        return resultado.stdout.strip()


    def get_brand(self):
        resultado = subprocess.run(f'adb -s {self.device} shell getprop ro.product.brand', capture_output=True, text=True, shell=True)
        return resultado.stdout.strip()

 
    def get_name(self):
        resultado = subprocess.run(f'adb -s {self.device} shell getprop ro.product.device', capture_output=True, text=True, shell=True)
        return resultado.stdout.strip()


    def get_android_version(self):
        resultado = subprocess.run(f'adb -s {self.device} shell getprop ro.build.version.release', capture_output=True, text=True, shell=True)
        return resultado.stdout.strip()

    def get_screen_resolution(self):
        print(self.device)
        resultado = subprocess.run(f'adb -s {self.device} shell wm size', capture_output=True, text=True, shell=True)
        return resultado.stdout.strip()


