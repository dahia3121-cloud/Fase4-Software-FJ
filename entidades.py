
# ==========================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: entidades.py
# DESCRIPCIÓN: Clase abstracta EntidadGeneral y clase Cliente
# CONCEPTOS: Abstracción, herencia y encapsulación
# ==========================================================

# Importamos las herramientas para crear clases abstractas.
from abc import ABC, abstractmethod

# Importamos las excepciones personalizadas.
from excepciones import (
    ClienteInvalidoError,
    ParametroFaltanteError
)


# ==========================================================
# 1. CLASE ABSTRACTA: ENTIDAD GENERAL
# ==========================================================

class EntidadGeneral(ABC):
    """
    Clase abstracta que representa las entidades generales
    del sistema Software FJ.

    Define los métodos que deben implementar las clases
    que hereden de ella.
    """

    @abstractmethod
    def obtener_identificador(self):
        """Devuelve el identificador de la entidad."""
        pass

    @abstractmethod
    def describir_entidad(self):
        """Devuelve una descripción de la entidad."""
        pass


# ==========================================================
# 2. CLASE CLIENTE
# ==========================================================

class Cliente(EntidadGeneral):
    """
    Representa un cliente de Software FJ.

    Hereda de EntidadGeneral y utiliza encapsulación
    para proteger sus datos personales.
    """

    def __init__(self, identificacion, nombre, correo):

        # Validamos los datos antes de almacenarlos.
        self.validar_identificacion(identificacion)
        self.validar_nombre(nombre)
        self.validar_correo(correo)

        # Atributos privados para aplicar encapsulación.
        self.__identificacion = identificacion.strip()
        self.__nombre = nombre.strip()
        self.__correo = correo.strip().lower()

    # ======================================================
    # 3. MÉTODOS DE VALIDACIÓN
    # ======================================================

    @staticmethod
    def validar_identificacion(identificacion):
        """Comprueba que la identificación sea válida."""

        if identificacion is None:
            raise ParametroFaltanteError(
                "La identificación es obligatoria."
            )

        if not isinstance(identificacion, str):
            raise ClienteInvalidoError(
                "La identificación debe ingresarse como texto."
            )

        identificacion = identificacion.strip()

        if not identificacion:
            raise ClienteInvalidoError(
                "La identificación no puede estar vacía."
            )

        if not identificacion.isdigit():
            raise ClienteInvalidoError(
                "La identificación debe contener solamente números."
            )

    @staticmethod
    def validar_nombre(nombre):
        """Comprueba que el nombre del cliente sea válido."""

        if nombre is None:
            raise ParametroFaltanteError(
                "El nombre del cliente es obligatorio."
            )

        if not isinstance(nombre, str):
            raise ClienteInvalidoError(
                "El nombre debe ser texto."
            )

        nombre = nombre.strip()

        if not nombre:
            raise ClienteInvalidoError(
                "El nombre no puede estar vacío."
            )

        if not all(caracter.isalpha() or caracter.isspace()
                   or caracter in "-'" for caracter in nombre):
            raise ClienteInvalidoError(
                "El nombre no debe contener números ni símbolos inválidos."
            )

    @staticmethod
    def validar_correo(correo):
        """Comprueba que el correo tenga una estructura válida."""

        if correo is None:
            raise ParametroFaltanteError(
                "El correo electrónico es obligatorio."
            )

        if not isinstance(correo, str):
            raise ClienteInvalidoError(
                "El correo debe ingresarse como texto."
            )

        correo = correo.strip()

        partes = correo.split("@")

        if len(partes) != 2:
            raise ClienteInvalidoError(
                "El correo debe contener un único símbolo @."
            )

        usuario, dominio = partes

        if not usuario or not dominio:
            raise ClienteInvalidoError(
                "El correo debe tener usuario y dominio."
            )

        if "." not in dominio:
            raise ClienteInvalidoError(
                "El dominio del correo debe contener un punto."
            )

        if dominio.startswith(".") or dominio.endswith("."):
            raise ClienteInvalidoError(
                "El dominio del correo no tiene un formato válido."
            )

    # ======================================================
    # 4. PROPIEDADES PARA PROTEGER LOS ATRIBUTOS
    # ======================================================

    @property
    def identificacion(self):
        """Permite consultar la identificación."""
        return self.__identificacion

    @property
    def nombre(self):
        """Permite consultar el nombre."""
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Permite modificar el nombre después de validarlo."""

        self.validar_nombre(nuevo_nombre)
        self.__nombre = nuevo_nombre.strip()

    @property
    def correo(self):
        """Permite consultar el correo electrónico."""
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo):
        """Permite modificar el correo después de validarlo."""

        self.validar_correo(nuevo_correo)
        self.__correo = nuevo_correo.strip().lower()

    # ======================================================
    # 5. IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS
    # ======================================================

    def obtener_identificador(self):
        """Devuelve la identificación del cliente."""
        return self.__identificacion

    def describir_entidad(self):
        """Devuelve la información general del cliente."""

        return (
            f"Cliente: {self.__nombre} | "
            f"Identificación: {self.__identificacion} | "
            f"Correo: {self.__correo}"
        )
