import subprocess
import re, os
import json,time
from PIL import Image
import io
from .modules.deviceInfo import Device

class ADB (Device):
    def __init__(self, device=None) -> None:
        self.device = device
        super().__init__(self)
        self.is_waiting = False
        self.keyboard_events = self._load_keyboard_events()

    def _load_keyboard_events(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), "modules", "keyboard_events.json")
            with open(file_path, "r") as f:
                data = json.load(f)
                return data
            
        except FileNotFoundError:
            print("El archivo 'keyboard_events.json' no se encontró en la ruta:", file_path)
            return {}
        

    @Device.device_connected
    def openLink(self, link):
        comando_abrir_enlace = f'adb -s {self.device} shell am start -a android.intent.action.VIEW -d {link}'
        subprocess.run(comando_abrir_enlace, shell=True)

    def openEmulator(self, name):
        comando_abrir_emulador = f'emulator -avd {name}'
        subprocess.Popen(comando_abrir_emulador, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

    def closeEmulator(self):
        subprocess.run('adb emu kill', shell=True)

    def listEmulators(self):
        comando_listar_emuladores = 'emulator -list-avds'
        resultado = subprocess.run(comando_listar_emuladores, capture_output=True, text=True, shell=True)
        emuladores = resultado.stdout.splitlines()

        return emuladores[1:]

    def connect(self, device_name):
        dispositivos_conectados = self.devices()
        if device_name in dispositivos_conectados:
            self.device = device_name
            self.is_connected = True
            print(f"Connected to {self.device}.")
        else:
            print(f"El dispositivo {device_name} no existe.")

    def disconnect(self):
        self.device = None
        self.is_connected = False

    def devices(self):
        resultado = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        salida = resultado.stdout
        dispositivos = re.findall(r'(\S+)\s+device\b', salida)
        return dispositivos
    
    @Device.device_connected
    def tap(self, x, y):
        comando_seleccionar_compartir = f'adb -s {self.device} shell input tap {x} {y}'
        subprocess.run(comando_seleccionar_compartir, shell=True)

    @Device.device_connected
    def keyEvent(self, event):
        comando_pulsar_tecla = f'adb -s {self.device} shell input keyevent {event}'
        subprocess.run(comando_pulsar_tecla, shell=True)

    @Device.device_connected
    def type_text(self, text):
        escaped_text = text.replace(" ", "%s").replace("\\", "\\\\").replace("\"", "\\\"").replace("'", "\\'")
        comando_escribir_texto = f'adb -s {self.device} shell input text "{escaped_text}"'
        subprocess.run(comando_escribir_texto, shell=True)

    @Device.device_connected
    def run_command(self, command):
        subprocess.run(command, shell=True)
    
    @Device.device_connected
    def shakeDevice(self):
        comando_shake = f'adb -s {self.device} shell input keyevent KEYCODE_APP_SWITCH'
        subprocess.run(comando_shake, shell=True)

    @Device.device_connected
    def take_screenshot(self, output_path=None):
        comando_screenshot = f'adb -s {self.device} exec-out screencap -p'
        resultado = subprocess.run(comando_screenshot, capture_output=True)
        if resultado.returncode == 0:
            imagen_bytes = resultado.stdout
            imagen_pillow = Image.open(io.BytesIO(imagen_bytes))

            if output_path is not None:
                imagen_pillow.save(output_path)
                print(f"Captura de pantalla guardada en {output_path}")

            return imagen_pillow
        else:
            print("Error al tomar la captura de pantalla.")
            return None
    
    def wait(self,timer):
        self.is_waiting = True
        time.sleep(timer)
        self.is_waiting = False

    def show_keyboard_events(self):
        try:
            print("Lista de eventos del teclado:")
            print("-" * 30)
            for event, description in self.keyboard_events.items():
                print(f"{event}: {description}")
            print("-" * 30)
        except FileNotFoundError:
            print("El archivo 'keyboard_events.json' no se encontró.")