


# ==========================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: servicios.py
# DESCRIPCIÓN: Clase abstracta Servicio y servicios especializados
# CONCEPTOS: Abstracción, herencia, polimorfismo, encapsulación
# ==========================================================

# Importamos las herramientas para crear clases abstractas.
from abc import abstractmethod
import math

# Importamos la clase abstracta general.
from entidades import EntidadGeneral

# Importamos las excepciones personalizadas.
from excepciones import (
    ParametroFaltanteError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError
)


# ==========================================================
# 1. CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(EntidadGeneral):
    """
    Clase abstracta que representa los servicios ofrecidos
    por Software FJ.

    Hereda de EntidadGeneral y define las operaciones comunes
    que deben utilizar los servicios especializados.
    """

    def __init__(self, id_servicio, nombre, tarifa_base, disponible=True):

        # Validamos que los datos obligatorios estén completos.
        if id_servicio is None or nombre is None or tarifa_base is None:
            raise ParametroFaltanteError(
                "Todos los datos del servicio son obligatorios."
            )

        # Validamos el identificador.
        if not isinstance(id_servicio, str) or not id_servicio.strip():
            raise ServicioInvalidoError(
                "El identificador del servicio no es válido."
            )

        # Validamos el nombre.
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError(
                "El nombre del servicio no es válido."
            )

        # Validamos la tarifa.
        if (
            isinstance(tarifa_base, bool)
            or not isinstance(tarifa_base, (int, float))
            or not math.isfinite(tarifa_base)
            or tarifa_base < 0
        ):
            raise ServicioInvalidoError(
                "La tarifa debe ser un número válido igual o mayor que cero."
            )

        # Validamos la disponibilidad.
        if not isinstance(disponible, bool):
            raise ServicioInvalidoError(
                "La disponibilidad debe ser verdadera o falsa."
            )

        # Aplicamos encapsulación mediante atributos privados.
        self.__id_servicio = id_servicio.strip()
        self.__nombre = nombre.strip()
        self.__tarifa_base = float(tarifa_base)
        self.__disponible = disponible

    # ------------------------------------------------------
    # PROPIEDADES PARA CONSULTAR LOS ATRIBUTOS PRIVADOS
    # ------------------------------------------------------

    @property
    def id_servicio(self):
        return self.__id_servicio

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa_base(self):
        return self.__tarifa_base

    @property
    def disponible(self):
        return self.__disponible

    # ------------------------------------------------------
    # CAMBIAR LA DISPONIBILIDAD DEL SERVICIO
    # ------------------------------------------------------

    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):
            raise ServicioInvalidoError(
                "El estado debe ser verdadero o falso."
            )

        self.__disponible = estado

    # ------------------------------------------------------
    # IMPLEMENTACIÓN DE MÉTODOS DE ENTIDADGENERAL
    # ------------------------------------------------------

    def obtener_identificador(self):
        """Devuelve el identificador del servicio."""
        return self.__id_servicio

    def describir_entidad(self):
        """Devuelve la descripción general del servicio."""

        return (
            f"Servicio: {self.__nombre} | "
            f"Identificador: {self.__id_servicio} | "
            f"Tarifa base: ${self.__tarifa_base:,.2f}"
        )

    # ------------------------------------------------------
    # VALIDACIÓN GENERAL DE PARÁMETROS
    # ------------------------------------------------------

    def validar_parametros(self, duracion, impuesto=0, descuento=0):
        """
        Comprueba que los datos necesarios para calcular
        el costo del servicio sean válidos.
        """

        # Verificamos que el servicio esté disponible.
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                "El servicio seleccionado no está disponible."
            )

        # Validamos la duración.
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):
            raise CalculoInconsistenteError(
                "La duración debe ser un número válido mayor que cero."
            )

        # Validamos el impuesto y el descuento.
        for valor, nombre in [
            (impuesto, "El impuesto"),
            (descuento, "El descuento")
        ]:
            if (
                isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                or not math.isfinite(valor)
                or not 0 <= valor <= 100
            ):
                raise CalculoInconsistenteError(
                    f"{nombre} debe ser un número entre 0 y 100."
                )

        return True

    # ------------------------------------------------------
    # MÉTODO PARA CALCULAR EL DESGLOSE DEL COSTO
    # ------------------------------------------------------

    def _calcular_desglose(
        self, duracion, impuesto, descuento, costo_adicional=0
    ):

        # Validamos los parámetros antes de realizar el cálculo.
        self.validar_parametros(duracion, impuesto, descuento)

        # Validamos los costos adicionales.
        if (
            isinstance(costo_adicional, bool)
            or not isinstance(costo_adicional, (int, float))
            or not math.isfinite(costo_adicional)
            or costo_adicional < 0
        ):
            raise CalculoInconsistenteError(
                "El costo adicional debe ser un número válido igual o mayor que cero."
            )

        # Calculamos el costo del servicio según su duración.
        subtotal_servicio = self.__tarifa_base * duracion

        # Sumamos los costos adicionales, si existen.
        subtotal = subtotal_servicio + costo_adicional

        # Aplicamos primero el descuento.
        valor_descuento = subtotal * (descuento / 100)
        base_imponible = subtotal - valor_descuento

        # Aplicamos el impuesto sobre el valor después del descuento.
        valor_impuesto = base_imponible * (impuesto / 100)

        # Calculamos el total que debe pagar el cliente.
        total = base_imponible + valor_impuesto

        # Verificamos que el resultado sea válido.
        if not all(
            math.isfinite(valor)
            for valor in [
                subtotal_servicio,
                subtotal,
                valor_descuento,
                base_imponible,
                valor_impuesto,
                total
            ]
        ):
            raise CalculoInconsistenteError(
                "El cálculo produjo un resultado no válido."
            )

        # Retornamos los valores organizados.
        return {
            "tarifa_base": round(self.__tarifa_base, 2),
            "duracion": duracion,
            "subtotal_servicio": round(subtotal_servicio, 2),
            "costo_adicional": round(costo_adicional, 2),
            "subtotal": round(subtotal, 2),
            "porcentaje_descuento": descuento,
            "valor_descuento": round(valor_descuento, 2),
            "base_imponible": round(base_imponible, 2),
            "porcentaje_impuesto": impuesto,
            "valor_impuesto": round(valor_impuesto, 2),
            "total": round(total, 2)
        }

    # ------------------------------------------------------
    # MÉTODO PÚBLICO PARA OBTENER EL DESGLOSE
    # ------------------------------------------------------

    def calcular_desglose(self, duracion, impuesto=0, descuento=0):
        """
        Calcula y devuelve el detalle del costo.

        Los servicios especializados pueden sobrescribir
        este método cuando necesiten cálculos adicionales.
        """

        return self._calcular_desglose(
            duracion, impuesto, descuento
        )

    # ------------------------------------------------------
    # MÉTODO PARA OBTENER ÚNICAMENTE EL TOTAL
    # ------------------------------------------------------

    def _calcular_total(
        self, duracion, impuesto, descuento, costo_adicional=0
    ):

        desglose = self._calcular_desglose(
            duracion, impuesto, descuento, costo_adicional
        )

        return desglose["total"]

    # ------------------------------------------------------
    # MÉTODO ABSTRACTO PARA EL CÁLCULO DEL COSTO
    # ------------------------------------------------------

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """
        Cada servicio especializado debe implementar
        su propia forma de calcular el costo.
        """
        pass


# ==========================================================
# 2. CLASE RESERVA DE SALA
# ==========================================================

class ReservaSala(Servicio):
    """Representa el servicio de alquiler de salas."""

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        # El costo depende de las horas de utilización.
        return self._calcular_total(
            duracion, impuesto, descuento
        )

    def describir_entidad(self):
        """Describe específicamente el servicio de sala."""

        return (
            f"Tipo: Reserva de sala | "
            f"Nombre: {self.nombre} | "
            f"Identificador: {self.id_servicio} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )


# ==========================================================
# 3. CLASE ALQUILER DE EQUIPO
# ==========================================================

class AlquilerEquipo(Servicio):
    """Representa el alquiler de equipos tecnológicos."""

    def __init__(
        self,
        id_servicio,
        nombre,
        tarifa_base,
        disponible=True,
        costo_mantenimiento=15000
    ):

        # Inicializamos los atributos de la clase padre.
        super().__init__(
            id_servicio, nombre, tarifa_base, disponible
        )

        # Validamos el costo de mantenimiento.
        if (
            isinstance(costo_mantenimiento, bool)
            or not isinstance(costo_mantenimiento, (int, float))
            or not math.isfinite(costo_mantenimiento)
            or costo_mantenimiento < 0
        ):
            raise ServicioInvalidoError(
                "El costo de mantenimiento debe ser un número válido igual o mayor que cero."
            )

        self.__costo_mantenimiento = float(costo_mantenimiento)

    @property
    def costo_mantenimiento(self):
        return self.__costo_mantenimiento

    def validar_parametros(self, duracion, impuesto=0, descuento=0):
        """
        Valida los parámetros generales y el mantenimiento
        correspondiente al alquiler del equipo.
        """

        super().validar_parametros(duracion, impuesto, descuento)

        if (
            not math.isfinite(self.__costo_mantenimiento)
            or self.__costo_mantenimiento < 0
        ):
            raise CalculoInconsistenteError(
                "El costo de mantenimiento no es válido."
            )

        return True

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        # Al alquiler se le agrega el costo de mantenimiento.
        return self._calcular_total(
            duracion,
            impuesto,
            descuento,
            self.__costo_mantenimiento
        )

    def calcular_desglose(self, duracion, impuesto=0, descuento=0):

        # Retornamos el desglose incluyendo el mantenimiento.
        return self._calcular_desglose(
            duracion,
            impuesto,
            descuento,
            self.__costo_mantenimiento
        )

    def describir_entidad(self):
        """Describe específicamente el alquiler de equipo."""

        return (
            f"Tipo: Alquiler de equipo | "
            f"Nombre: {self.nombre} | "
            f"Identificador: {self.id_servicio} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Mantenimiento: ${self.__costo_mantenimiento:,.2f}"
        )


# ==========================================================
# 4. CLASE ASESORÍA ESPECIALIZADA
# ==========================================================

class AsesoriaEspecializada(Servicio):
    """Representa los servicios de asesoría profesional."""

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        # El costo depende de las horas de asesoría.
        return self._calcular_total(
            duracion, impuesto, descuento
        )

    def describir_entidad(self):
        """Describe específicamente el servicio de asesoría."""

        return (
            f"Tipo: Asesoría especializada | "
            f"Nombre: {self.nombre} | "
            f"Identificador: {self.id_servicio} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )
