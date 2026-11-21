

# Importamos logging para registrar eventos y errores.
import logging

# Importamos la clase Cliente.
from entidades import Cliente

# Importamos la clase Servicio.
from servicios import Servicio

# Importamos las excepciones personalizadas.
from excepciones import (
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError
)


# Creamos un registro para los eventos de este módulo.
logger = logging.getLogger(__name__)


# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva:
    """
    Representa una reserva realizada por un cliente
    para utilizar uno de los servicios de Software FJ.
    """

    def __init__(
        self,
        id_reserva,
        cliente,
        servicio,
        duracion,
        impuesto=0,
        descuento=0
    ):

        # Validamos que los datos obligatorios estén completos.
        if (
            id_reserva is None
            or cliente is None
            or servicio is None
            or duracion is None
        ):
            raise ParametroFaltanteError(
                "Todos los datos de la reserva son obligatorios."
            )

        # Validamos el identificador de la reserva.
        if not isinstance(id_reserva, str) or not id_reserva.strip():
            raise ReservaInvalidaError(
                "El identificador de la reserva no es válido."
            )

        # Verificamos que el cliente sea un objeto Cliente.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "La reserva debe estar asociada a un cliente válido."
            )

        # Verificamos que el servicio sea un objeto Servicio.
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "La reserva debe estar asociada a un servicio válido."
            )

        # Validamos la duración.
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise ReservaInvalidaError(
                "La duración debe ser un número mayor que cero."
            )

        # Validamos el impuesto y el descuento.
        for valor, nombre in [
            (impuesto, "El impuesto"),
            (descuento, "El descuento")
        ]:
            if (
                isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                or not 0 <= valor <= 100
            ):
                raise ReservaInvalidaError(
                    f"{nombre} debe estar entre 0 y 100."
                )

        # Guardamos los datos de la reserva.
        self.__id_reserva = id_reserva.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__impuesto = impuesto
        self.__descuento = descuento

        # Toda reserva comienza pendiente.
        self.__estado = "Pendiente"

        # El costo y su desglose se calculan al procesar la reserva.
        self.__total = None
        self.__desglose = None

        logger.info(
            "Se creó la reserva %s para el cliente %s.",
            self.__id_reserva,
            self.__cliente.nombre
        )

    # ------------------------------------------------------
    # PROPIEDADES PARA CONSULTAR LOS ATRIBUTOS PRIVADOS
    # ------------------------------------------------------

    @property
    def id_reserva(self):
        return self.__id_reserva

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def total(self):
        return self.__total

    # ------------------------------------------------------
    # MÉTODO PARA PROCESAR LA RESERVA
    # ------------------------------------------------------

    def procesar_reserva(self):
        """
        Calcula el costo y confirma la reserva si el servicio
        se encuentra disponible.
        """

        # Evitamos procesar una reserva que ya fue confirmada
        # o cancelada.
        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden procesar reservas pendientes."
            )

        try:
            # Solicitamos al servicio el desglose completo.
            # El polimorfismo permite que cada tipo de servicio
            # aplique su propio cálculo.
            desglose = self.__servicio.calcular_desglose(
                self.__duracion,
                self.__impuesto,
                self.__descuento
            )

            # Obtenemos el total del desglose.
            total = desglose["total"]

        except Exception as error:

            # Registramos el error ocurrido.
            logger.exception(
                "Error al procesar la reserva %s.",
                self.__id_reserva
            )

            # Lanzamos una excepción propia conservando
            # el error original como causa.
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from error

        else:
            # Si el cálculo fue exitoso, guardamos el desglose.
            self.__desglose = desglose

            # Guardamos el total calculado.
            self.__total = total

            # Marcamos el servicio como no disponible.
            self.__servicio.cambiar_disponibilidad(False)

            # Cambiamos el estado de la reserva.
            self.__estado = "Confirmada"

            # Registramos la confirmación.
            logger.info(
                "Reserva %s confirmada. Total: $%.2f.",
                self.__id_reserva,
                self.__total
            )

            return self.__total

        finally:
            # Este bloque se ejecuta tanto si hay error
            # como si la operación termina correctamente.
            logger.info(
                "Finalizó el intento de procesamiento de la reserva %s.",
                self.__id_reserva
            )

    # ------------------------------------------------------
    # MÉTODO PARA MOSTRAR EL DESGLOSE DEL COSTO
    # ------------------------------------------------------

    def mostrar_desglose(self):
        """
        Muestra los valores que componen el costo de la reserva.
        """

        # Verificamos que la reserva ya haya sido procesada.
        if self.__desglose is None:
            return (
                "\nEl desglose no está disponible. "
                "Primero debe procesar la reserva."
            )

        # Obtenemos los valores calculados.
        detalle = self.__desglose

        # Construimos el desglose para mostrarlo en la terminal.
        resultado = (
            "\n========== DETALLE DEL CÁLCULO ==========\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Tarifa por hora: ${detalle['tarifa_base']:,.2f}\n"
            f"Duración: {detalle['duracion']} horas\n"
            f"Subtotal del servicio: "
            f"${detalle['subtotal_servicio']:,.2f}\n"
        )

        # Mostramos el costo adicional cuando exista.
        if detalle["costo_adicional"] > 0:
            resultado += (
                f"Costo de mantenimiento: "
                f"${detalle['costo_adicional']:,.2f}\n"
            )

        # Agregamos los demás valores del cálculo.
        resultado += (
            f"Subtotal: ${detalle['subtotal']:,.2f}\n"
            f"Descuento "
            f"({detalle['porcentaje_descuento']:g}%): "
            f"-${detalle['valor_descuento']:,.2f}\n"
            f"Base después del descuento: "
            f"${detalle['base_imponible']:,.2f}\n"
            f"Impuesto "
            f"({detalle['porcentaje_impuesto']:g}%): "
            f"${detalle['valor_impuesto']:,.2f}\n"
            "=========================================\n"
            f"TOTAL A PAGAR: ${detalle['total']:,.2f}\n"
            "========================================="
        )

        return resultado

    # ------------------------------------------------------
    # MÉTODO PARA CANCELAR LA RESERVA
    # ------------------------------------------------------

    def cancelar_reserva(self):

        # No se puede cancelar una reserva que ya fue cancelada.
        if self.__estado == "Cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada."
            )

        # Si estaba confirmada, liberamos el servicio.
        if self.__estado == "Confirmada":
            self.__servicio.cambiar_disponibilidad(True)

        # Actualizamos el estado.
        self.__estado = "Cancelada"

        logger.info(
            "La reserva %s fue cancelada.",
            self.__id_reserva
        )

        return "La reserva fue cancelada correctamente."

    # ------------------------------------------------------
    # MÉTODO PARA MOSTRAR LA INFORMACIÓN DE LA RESERVA
    # ------------------------------------------------------

    def mostrar_informacion(self):

        # Mostramos el total únicamente si ya fue calculado.
        if self.__total is None:
            costo = "Pendiente de cálculo"
        else:
            costo = f"${self.__total:,.2f}"

        return (
            "\n========== INFORMACIÓN DE LA RESERVA ==========\n"
            f"Identificador: {self.__id_reserva}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Identificación: {self.__cliente.identificacion}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Duración: {self.__duracion} horas\n"
            f"Estado: {self.__estado}\n"
            f"Total: {costo}\n"
            "================================================"
        )
