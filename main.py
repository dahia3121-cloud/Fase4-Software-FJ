
# ============================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# Empresa: Software FJ
# Archivo principal: main.py
# ============================================================

import logging

# Importación de las clases creadas en los demás módulos.
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaGestion
from excepciones import SistemaGestionError


# Se crea el objeto principal que administra el sistema.
sistema = SistemaGestion()


# ------------------------------------------------------------
# FUNCIONES PARA VALIDAR LOS DATOS INGRESADOS POR EL USUARIO
# ------------------------------------------------------------

def leer_texto(mensaje):
    """Solicita un texto y evita que el usuario deje el campo vacío."""
    while True:
        dato = input(mensaje).strip()

        if dato:
            return dato

        print("Error: este campo no puede estar vacío.")


def leer_numero(mensaje, permitir_cero=False):
    """Solicita un número y valida que sea positivo."""
    while True:
        try:
            dato = float(input(mensaje))

            if dato < 0:
                print("Error: el valor no puede ser negativo.")
            elif dato == 0 and not permitir_cero:
                print("Error: el valor debe ser mayor que cero.")
            else:
                return dato

        except ValueError:
            print("Error: debe ingresar un valor numérico.")


def leer_porcentaje(mensaje):
    """Valida que el porcentaje esté entre 0 y 100."""
    while True:
        porcentaje = leer_numero(mensaje, permitir_cero=True)

        if porcentaje <= 100:
            return porcentaje

        print("Error: el porcentaje debe estar entre 0 y 100.")


# ------------------------------------------------------------
# 1. REGISTRAR CLIENTES
# ------------------------------------------------------------

def registrar_cliente():
    print("\n--- REGISTRO DE CLIENTES ---")

    # Solicitamos y validamos la identificación inmediatamente.
    while True:
        identificacion = leer_texto("Identificación: ")

        try:
            Cliente.validar_identificacion(identificacion)
            break
        except SistemaGestionError as error:
            print(f"Error: {error}")

    # Solicitamos y validamos el nombre.
    while True:
        nombre = leer_texto("Nombre completo: ")

        try:
            Cliente.validar_nombre(nombre)
            break
        except SistemaGestionError as error:
            print(f"Error: {error}")

    # Solicitamos y validamos el correo.
    while True:
        correo = leer_texto("Correo electrónico: ")

        try:
            Cliente.validar_correo(correo)
            break
        except SistemaGestionError as error:
            print(f"Error: {error}")

    # Creamos y registramos el cliente.
    cliente = Cliente(identificacion, nombre, correo)
    sistema.registrar_cliente(cliente)

    print("\nCliente registrado correctamente.")


# ------------------------------------------------------------
# 2. REGISTRAR SERVICIOS
# ------------------------------------------------------------

def registrar_servicio():
    print("\n--- REGISTRO DE SERVICIOS ---")

    print("1. Reserva de sala")
    print("2. Alquiler de equipo")
    print("3. Asesoría especializada")

    opcion = leer_texto("Seleccione el tipo de servicio: ")

    if opcion not in ["1", "2", "3"]:
        print("Opción de servicio no válida.")
        return

    id_servicio = leer_texto("Código del servicio: ")
    nombre = leer_texto("Nombre del servicio: ")
    tarifa = leer_numero("Tarifa base: $")

    if opcion == "1":
        servicio = ReservaSala(id_servicio, nombre, tarifa)

    elif opcion == "2":
        mantenimiento = leer_numero(
            "Costo de mantenimiento: $",
            permitir_cero=True
        )

        servicio = AlquilerEquipo(
            id_servicio,
            nombre,
            tarifa,
            costo_mantenimiento=mantenimiento
        )

    else:
        servicio = AsesoriaEspecializada(
            id_servicio,
            nombre,
            tarifa
        )

    sistema.registrar_servicio(servicio)

    print("\nServicio registrado correctamente.")


# ------------------------------------------------------------
# 3. CREAR RESERVAS
# ------------------------------------------------------------

def crear_reserva():
    print("\n--- CREACIÓN DE RESERVAS ---")

    id_reserva = leer_texto("Código de la reserva: ")
    identificacion = leer_texto("Identificación del cliente: ")
    id_servicio = leer_texto("Código del servicio: ")

    duracion = leer_numero("Duración del servicio: ")

    impuesto = leer_porcentaje("Porcentaje de impuesto (0 a 100): ")
    descuento = leer_porcentaje("Porcentaje de descuento (0 a 100): ")

    sistema.crear_reserva(
        id_reserva,
        identificacion,
        id_servicio,
        duracion,
        impuesto,
        descuento
    )

    print("\nReserva creada correctamente.")


# ------------------------------------------------------------
# 4. PROCESAR RESERVAS
# ------------------------------------------------------------

def procesar_reserva():
    print("\n--- PROCESAMIENTO DE RESERVAS ---")

    id_reserva = leer_texto("Código de la reserva: ")

    # Procesamos la reserva y calculamos el costo.
    sistema.procesar_reserva(id_reserva)

    # Recuperamos la reserva para consultar su desglose.
    reserva = sistema.obtener_reserva(id_reserva)

    print("\nReserva procesada correctamente.")

    # Mostramos el detalle de todos los valores calculados.
    print(reserva.mostrar_desglose())


# ------------------------------------------------------------
# 5. CANCELAR RESERVAS
# ------------------------------------------------------------

def cancelar_reserva():
    print("\n--- CANCELACIÓN DE RESERVAS ---")

    id_reserva = leer_texto("Código de la reserva: ")

    sistema.cancelar_reserva(id_reserva)

    print("\nReserva cancelada correctamente.")


# ------------------------------------------------------------
# 6. CONSULTAR CLIENTES
# ------------------------------------------------------------

def consultar_clientes():
    print("\n--- LISTADO DE CLIENTES ---")
    print(sistema.mostrar_clientes())


# ------------------------------------------------------------
# 7. CONSULTAR SERVICIOS
# ------------------------------------------------------------

def consultar_servicios():
    print("\n--- LISTADO DE SERVICIOS ---")
    print(sistema.mostrar_servicios())


# ------------------------------------------------------------
# 8. CONSULTAR RESERVAS
# ------------------------------------------------------------

def consultar_reservas():
    print("\n--- LISTADO DE RESERVAS ---")

    # Mostramos la información que devuelve el sistema.
    print(sistema.mostrar_reservas())


# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------

def mostrar_menu():
    print("\n==============================================")
    print("       SOFTWARE FJ - SISTEMA DE GESTIÓN")
    print("==============================================")
    print("1. Registrar clientes")
    print("2. Registrar servicios")
    print("3. Crear reservas")
    print("4. Procesar reservas")
    print("5. Cancelar reservas")
    print("6. Consultar clientes")
    print("7. Consultar servicios")
    print("8. Consultar reservas")
    print("0. Salir")
    print("==============================================")


# ------------------------------------------------------------
# FUNCIÓN PRINCIPAL: CONTROLA LA EJECUCIÓN DEL PROGRAMA
# ------------------------------------------------------------

def main():

    print("Bienvenido al Sistema Integral de Gestión de Software FJ.")

    while True:

        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        try:

            if opcion == "1":
                registrar_cliente()

            elif opcion == "2":
                registrar_servicio()

            elif opcion == "3":
                crear_reserva()

            elif opcion == "4":
                procesar_reserva()

            elif opcion == "5":
                cancelar_reserva()

            elif opcion == "6":
                consultar_clientes()

            elif opcion == "7":
                consultar_servicios()

            elif opcion == "8":
                consultar_reservas()

            elif opcion == "0":
                print("\nGracias por utilizar el sistema. ¡Hasta pronto!")
                break

            else:
                print("\nOpción no válida. Intente nuevamente.")

        except SistemaGestionError as error:
            print("\nNo se pudo completar la operación.")
            print("Detalle:", error)

            logging.error("Error controlado en el menú: %s", error)

        except Exception as error:
            print("\nSe presentó un error inesperado.")
            print("Detalle:", error)

            logging.exception("Error inesperado en el programa.")


# ------------------------------------------------------------
# PUNTO DE ENTRADA DEL PROGRAMA
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
