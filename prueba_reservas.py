
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo
from reservas import Reserva

from excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError
)


print("\n======================================")
print(" PRUEBAS DEL MODULO DE RESERVAS")
print("======================================")


# Creamos los datos que utilizaremos en las pruebas.
cliente = Cliente(
    "123456789",
    "Camila Torres",
    "camila@gmail.com"
)

sala = ReservaSala(
    "S001",
    "Sala de reuniones",
    50000
)


# PRUEBA 1: Crear una reserva correctamente.
try:
    reserva = Reserva("R001", cliente, sala, 2)
    print("\nPRUEBA 1: CORRECTA - Reserva creada.")
except Exception as error:
    print("\nPRUEBA 1: ERROR:", error)


# PRUEBA 2: Mostrar información de la reserva.
try:
    print("\nPRUEBA 2: CORRECTA")
    print(reserva.mostrar_informacion())
except Exception as error:
    print("\nPRUEBA 2: ERROR:", error)


# PRUEBA 3: Procesar y confirmar la reserva.
try:
    total = reserva.procesar_reserva()
    print("\nPRUEBA 3: CORRECTA - Reserva confirmada.")
    print("Total:", total)
    print("Estado:", reserva.estado)
except Exception as error:
    print("\nPRUEBA 3: ERROR:", error)


# PRUEBA 4: Verificar que el servicio quedó ocupado.
try:
    if not sala.disponible:
        print("\nPRUEBA 4: CORRECTA - Servicio no disponible.")
    else:
        print("\nPRUEBA 4: ERROR - El servicio sigue disponible.")
except Exception as error:
    print("\nPRUEBA 4: ERROR:", error)


# PRUEBA 5: Intentar procesar nuevamente la reserva.
try:
    reserva.procesar_reserva()
    print("\nPRUEBA 5: ERROR - Permitió procesar dos veces.")
except OperacionNoPermitidaError as error:
    print("\nPRUEBA 5: CORRECTA -", error)


# PRUEBA 6: Cancelar la reserva.
try:
    resultado = reserva.cancelar_reserva()
    print("\nPRUEBA 6: CORRECTA -", resultado)
    print("Estado:", reserva.estado)
except Exception as error:
    print("\nPRUEBA 6: ERROR:", error)


# PRUEBA 7: Comprobar que el servicio quedó disponible.
try:
    if sala.disponible:
        print("\nPRUEBA 7: CORRECTA - Servicio liberado.")
    else:
        print("\nPRUEBA 7: ERROR - Servicio continúa ocupado.")
except Exception as error:
    print("\nPRUEBA 7: ERROR:", error)


# PRUEBA 8: Intentar crear una reserva con duración negativa.
try:
    reserva_error = Reserva("R002", cliente, sala, -3)
    print("\nPRUEBA 8: ERROR - Aceptó duración negativa.")
except ReservaInvalidaError as error:
    print("\nPRUEBA 8: CORRECTA -", error)


# PRUEBA 9: Intentar cancelar dos veces la misma reserva.
try:
    reserva.cancelar_reserva()
    print("\nPRUEBA 9: ERROR - Permitió cancelar dos veces.")
except OperacionNoPermitidaError as error:
    print("\nPRUEBA 9: CORRECTA -", error)


# PRUEBA 10: Procesar una reserva con un servicio no disponible.
try:
    equipo = AlquilerEquipo(
        "E001",
        "Computador",
        30000,
        disponible=False
    )

    reserva_error = Reserva(
        "R003",
        cliente,
        equipo,
        2
    )

    reserva_error.procesar_reserva()

    print("\nPRUEBA 10: ERROR - Aceptó servicio no disponible.")

except ReservaInvalidaError as error:
    print("\nPRUEBA 10: CORRECTA - Error controlado.")
    print("Detalle:", error)
    print("Causa original:", error.__cause__)


print("\n======================================")
print(" FINALIZARON LAS PRUEBAS")
print("======================================")
