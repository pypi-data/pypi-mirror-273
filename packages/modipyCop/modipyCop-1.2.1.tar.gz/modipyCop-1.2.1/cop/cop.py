import os
import time
from typing import Callable

class Cop:
    def __init__(self, path: str):
        self.path = path
        self.modificaciones_previas = None

    def prev_revision(self) -> None:
        self.modificaciones_previas = self._revisar_modificaciones()

    def post_revision(self, print_output: bool = True) -> None:
        modificaciones_actuales = self._revisar_modificaciones()
        archivos_modificados = self._comparar_modificaciones(modificaciones_actuales)
        if print_output:
            self._print(archivos_modificados)

    def _revisar_modificaciones(self) -> dict:
        modificaciones = {}
        if os.path.isfile(self.path):
            tiempo_modificacion = os.path.getmtime(self.path)
            modificaciones[os.path.basename(self.path)] = tiempo_modificacion
        elif os.path.isdir(self.path):
            for archivo in os.listdir(self.path):
                ruta_completa = os.path.join(self.path, archivo)
                if os.path.isfile(ruta_completa):
                    tiempo_modificacion = os.path.getmtime(ruta_completa)
                    modificaciones[archivo] = tiempo_modificacion
        return modificaciones

    def _comparar_modificaciones(self, modificaciones_actuales: dict[str,str]) -> list:
        archivos_modificados = []
        for archivo, tiempo_modificacion in modificaciones_actuales.items():
            if archivo in self.modificaciones_previas and tiempo_modificacion != self.modificaciones_previas[archivo]:
                tiempo_pasado = time.time() - tiempo_modificacion
                archivos_modificados.append((archivo, tiempo_pasado))
        return archivos_modificados

    def _print(self, archivos_modificados: str | list) -> None:
        if os.path.isfile(self.path):
            if len(archivos_modificados) > 0:
                archivo, tiempo = archivos_modificados[0]
                print(f"{archivo} modified {tiempo:.2f} seconds ago.")
            else:
                print(f"No modifications in {self.path}")
        else:
            if len(archivos_modificados) != 0:
                print(f'Modified files in {self.path}:\n')
                for archivo, tiempo in archivos_modificados:
                    print(f"{archivo}, {tiempo:.2f} seconds ago.")
            else:
                print(f"No file was modified in {self.path}")

def decoprator(path: str) -> Callable:
    """
    Decorator that prints if there were any changes in a directory.
    
    :param path: Path to the folder or file that wants to be vigilated.
    """
    c = Cop(path)
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            c.prev_revision()
            result = func(*args, **kwargs)
            c.post_revision()
            return result
        return wrapper
    return decorator