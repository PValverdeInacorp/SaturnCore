from abc import ABC, abstractmethod
from apps.correos.domain.entities.correo import Correo


class ProveedorCorreo(ABC):
    @abstractmethod
    def enviar(self, correo: Correo) -> dict:
        pass