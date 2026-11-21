
# Importamos las clases necesarias.
from sistema import SistemaGestion
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo

# Importamos las excepciones que vamos a comprobar.
from excepciones import (
    ClienteDuplicadoError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError
)


print("\n======================================")
print(" PRUEBAS DEL MODULO SISTEMA")
print("======================================")


# Creamos una instancia del sistema.
sistema = SistemaGestion()


# PRUEBA 1: Registrar un cliente.
try:
    cliente = Cliente(
        "123456789",
        "Camila Torres",
        "camila@gmail.com"
    )

    resultado = sistema.registrar_cliente(cliente)

    print("\nPRUEBA 1: CORRECTA -", resultado)

except Exception as error:
    print("\nPRUEBA 1: ERROR:", error)


# PRUEBA 2: Intentar registrar un cliente duplicado.
try:
    cliente_duplicado = Cliente(
        "123456789",
        "Carlos Perez",
        "carlos@gmail.com"
    )

    sistema.registrar_cliente(cliente_duplicado)

    print("\nPRUEBA 2: ERROR - Aceptó identificación duplicada.")

except ClienteDuplicadoError as error:
    print("\nPRUEBA 2: CORRECTA -", error)


# PRUEBA 3: Registrar un servicio.
try:
    sala = ReservaSala(
        "S001",
        "Sala de reuniones",
        50000
    )

    resultado = sistema.registrar_servicio(sala)

    print("\nPRUEBA 3: CORRECTA -", resultado)

except Exception as error:
    print("\nPRUEBA 3: ERROR:", error)


# PRUEBA 4: Intentar registrar un servicio duplicado.
try:
    sala_duplicada = ReservaSala(
        "S001",
        "Otra sala",
        60000
    )

    sistema.registrar_servicio(sala_duplicada)

    print("\nPRUEBA 4: ERROR - Aceptó servicio duplicado.")

except ServicioInvalidoError as error:
    print("\nPRUEBA 4: CORRECTA -", error)


# PRUEBA 5: Crear una reserva.
try:
    reserva = sistema.crear_reserva(
        "R001",
        "123456789",
        "S001",
        2
    )

    print("\nPRUEBA 5: CORRECTA - Reserva creada.")
    print(reserva.mostrar_informacion())

except Exception as error:
    print("\nPRUEBA 5: ERROR:", error)


# PRUEBA 6: Intentar crear una reserva con un cliente inexistente.
try:
    sistema.crear_reserva(
        "R002",
        "999999999",
        "S001",
        2
    )

    print("\nPRUEBA 6: ERROR - Aceptó un cliente inexistente.")

except ReservaInvalidaError as error:
    print("\nPRUEBA 6: CORRECTA -", error)


# PRUEBA 7: Procesar la reserva.
try:
    total = sistema.procesar_reserva("R001")

    print("\nPRUEBA 7: CORRECTA - Reserva procesada.")
    print("Total:", total)

except Exception as error:
    print("\nPRUEBA 7: ERROR:", error)


# PRUEBA 8: Consultar los registros del sistema.
try:
    print("\nPRUEBA 8: CORRECTA - Consulta de registros.")

    print("Cantidad de clientes:", len(sistema.listar_clientes()))
    print("Cantidad de servicios:", len(sistema.listar_servicios()))
    print("Cantidad de reservas:", len(sistema.listar_reservas()))

except Exception as error:
    print("\nPRUEBA 8: ERROR:", error)


# PRUEBA 9: Cancelar la reserva.
try:
    resultado = sistema.cancelar_reserva("R001")

    print("\nPRUEBA 9: CORRECTA -", resultado)

except Exception as error:
    print("\nPRUEBA 9: ERROR:", error)


# PRUEBA 10: Intentar crear una reserva con un servicio inexistente.
try:
    sistema.crear_reserva(
        "R003",
        "123456789",
        "S999",
        2
    )

    print("\nPRUEBA 10: ERROR - Aceptó un servicio inexistente.")

except ReservaInvalidaError as error:
    print("\nPRUEBA 10: CORRECTA -", error)


# PRUEBA 11: Intentar registrar un objeto que no sea Cliente.
try:
    sistema.registrar_cliente("Camila Torres")

    print("\nPRUEBA 11: ERROR - Aceptó un dato que no es Cliente.")

except ClienteInvalidoError as error:
    print("\nPRUEBA 11: CORRECTA -", error)


# PRUEBA 12: Mostrar los registros.
try:
    print("\nPRUEBA 12: CORRECTA - Información del sistema.")

    print(sistema.mostrar_clientes())
    print(sistema.mostrar_servicios())
    print(sistema.mostrar_reservas())

except Exception as error:
    print("\nPRUEBA 12: ERROR:", error)


print("\n======================================")
print(" FINALIZARON LAS PRUEBAS")
print("======================================")
