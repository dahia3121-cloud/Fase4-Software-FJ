
# Importamos logging para registrar eventos y errores.
import logging

# Importamos las clases que administrará el sistema.
from entidades import Cliente
from servicios import Servicio
from reservas import Reserva

# Importamos las excepciones personalizadas.
from excepciones import (
    ClienteInvalidoError,
    ClienteDuplicadoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)


# Configuramos el registro de eventos y errores.
# Los registros se guardan en sistema_eventos.log.
logging.basicConfig(
    filename="sistema_eventos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


# ==========================================================
# CLASE SISTEMA DE GESTIÓN
# ==========================================================

class SistemaGestion:
    """
    Administra los clientes, servicios y reservas
    de la empresa Software FJ.
    """

    def __init__(self):

        # Listas privadas para almacenar los objetos.
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        logger.info("Se inició el sistema de gestión de Software FJ.")

    # ------------------------------------------------------
    # REGISTRAR CLIENTES
    # ------------------------------------------------------

    def registrar_cliente(self, cliente):

        # Verificamos que el objeto sea un Cliente.
        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError(
                "Solo se pueden registrar objetos de tipo Cliente."
            )

        # Evitamos registrar dos veces la misma identificación.
        for cliente_registrado in self.__clientes:
            if (
                cliente_registrado.identificacion
                == cliente.identificacion
            ):
                raise ClienteDuplicadoError(
                    "Ya existe un cliente con esa identificación."
                )

        # Guardamos el cliente en la lista.
        self.__clientes.append(cliente)

        logger.info(
            "Cliente registrado: %s - %s.",
            cliente.identificacion,
            cliente.nombre
        )

        return "Cliente registrado correctamente."

    # ------------------------------------------------------
    # REGISTRAR SERVICIOS
    # ------------------------------------------------------

    def registrar_servicio(self, servicio):

        # Verificamos que el objeto sea un Servicio.
        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError(
                "Solo se pueden registrar objetos de tipo Servicio."
            )

        # Evitamos identificadores de servicio repetidos.
        for servicio_registrado in self.__servicios:
            if (
                servicio_registrado.id_servicio
                == servicio.id_servicio
            ):
                raise ServicioInvalidoError(
                    "Ya existe un servicio con ese identificador."
                )

        # Guardamos el servicio en la lista.
        self.__servicios.append(servicio)

        logger.info(
            "Servicio registrado: %s - %s.",
            servicio.id_servicio,
            servicio.nombre
        )

        return "Servicio registrado correctamente."

    # ------------------------------------------------------
    # CREAR RESERVAS
    # ------------------------------------------------------

    def crear_reserva(
        self,
        id_reserva,
        identificacion_cliente,
        id_servicio,
        duracion,
        impuesto=0,
        descuento=0
    ):

        # Buscamos el cliente mediante su identificación.
        cliente_encontrado = None

        for cliente in self.__clientes:
            if cliente.identificacion == identificacion_cliente:
                cliente_encontrado = cliente
                break

        # Verificamos que el cliente esté registrado.
        if cliente_encontrado is None:
            raise ReservaInvalidaError(
                "No existe un cliente registrado con esa identificación."
            )

        # Buscamos el servicio mediante su identificador.
        servicio_encontrado = None

        for servicio in self.__servicios:
            if servicio.id_servicio == id_servicio:
                servicio_encontrado = servicio
                break

        # Verificamos que el servicio esté registrado.
        if servicio_encontrado is None:
            raise ReservaInvalidaError(
                "No existe un servicio registrado con ese identificador."
            )

        # Evitamos identificadores de reserva repetidos.
        for reserva in self.__reservas:
            if reserva.id_reserva == id_reserva:
                raise ReservaInvalidaError(
                    "Ya existe una reserva con ese identificador."
                )

        # Creamos la reserva con los objetos encontrados.
        nueva_reserva = Reserva(
            id_reserva,
            cliente_encontrado,
            servicio_encontrado,
            duracion,
            impuesto,
            descuento
        )

        # Guardamos la reserva.
        self.__reservas.append(nueva_reserva)

        logger.info(
            "Reserva %s creada para el cliente %s.",
            id_reserva,
            identificacion_cliente
        )

        return nueva_reserva

    # ------------------------------------------------------
    # PROCESAR RESERVAS
    # ------------------------------------------------------

    def procesar_reserva(self, id_reserva):

        # Buscamos la reserva solicitada.
        reserva_encontrada = self.obtener_reserva(id_reserva)

        try:
            # Procesamos la reserva.
            total = reserva_encontrada.procesar_reserva()

        except Exception:
            # Registramos el error y permitimos que se controle
            # en el nivel superior de la aplicación.
            logger.exception(
                "No se pudo procesar la reserva %s.",
                id_reserva
            )
            raise

        else:
            logger.info(
                "El sistema confirmó la reserva %s.",
                id_reserva
            )

            return total

    # ------------------------------------------------------
    # CANCELAR RESERVAS
    # ------------------------------------------------------

    def cancelar_reserva(self, id_reserva):

        # Buscamos la reserva.
        reserva_encontrada = self.obtener_reserva(id_reserva)

        # Cancelamos la reserva.
        resultado = reserva_encontrada.cancelar_reserva()

        logger.info(
            "El sistema canceló la reserva %s.",
            id_reserva
        )

        return resultado

    # ------------------------------------------------------
    # CONSULTAR UNA RESERVA
    # ------------------------------------------------------

    def obtener_reserva(self, id_reserva):

        # Buscamos la reserva por su identificador.
        for reserva in self.__reservas:
            if reserva.id_reserva == id_reserva:
                return reserva

        # Si no existe, informamos el error.
        raise ReservaInvalidaError(
            "No se encontró la reserva solicitada."
        )

    # ------------------------------------------------------
    # CONSULTAR LISTAS DE REGISTROS
    # ------------------------------------------------------

    def listar_clientes(self):

        # Devolvemos una copia para proteger la lista interna.
        return self.__clientes.copy()

    def listar_servicios(self):

        return self.__servicios.copy()

    def listar_reservas(self):

        return self.__reservas.copy()

    # ------------------------------------------------------
    # MOSTRAR LOS REGISTROS DEL SISTEMA
    # ------------------------------------------------------

    
    # ------------------------------------------------------
    # MOSTRAR LOS REGISTROS DEL SISTEMA
    # ------------------------------------------------------

    def mostrar_clientes(self):

        if not self.__clientes:
            return "No hay clientes registrados."

        resultado = "\n========== LISTA DE CLIENTES ==========\n"

        for cliente in self.__clientes:
            resultado += cliente.describir_entidad() + "\n"

        return resultado

    def mostrar_servicios(self):

        if not self.__servicios:
            return "No hay servicios registrados."

        resultado = "\n========== LISTA DE SERVICIOS ==========\n"

        for servicio in self.__servicios:
            estado = (
                "Disponible"
                if servicio.disponible
                else "No disponible"
            )

            resultado += (
                servicio.describir_entidad()
                + f" | Estado: {estado}\n"
            )

        return resultado

    def mostrar_reservas(self):

        if not self.__reservas:
            return "No hay reservas registradas."

        resultado = "\n========== LISTA DE RESERVAS ==========\n"

        for reserva in self.__reservas:
            resultado += reserva.mostrar_informacion() + "\n"

        return resultado
