
from servicios import (
    Servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

from excepciones import (
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError
)


print("\n======================================")
print(" PRUEBAS DEL MODULO DE SERVICIOS")
print("======================================")

# PRUEBA 1: Crear una reserva de sala.
try:
    sala = ReservaSala("S001", "Sala de reuniones", 50000)
    print("\nPRUEBA 1: CORRECTA - Sala creada.")
    print(sala.describir_entidad())
except Exception as error:
    print("PRUEBA 1: ERROR:", error)


# PRUEBA 2: Calcular el alquiler de una sala.
try:
    total = sala.calcular_costo(2)
    print("\nPRUEBA 2: CORRECTA - Costo de sala:", total)
except Exception as error:
    print("PRUEBA 2: ERROR:", error)


# PRUEBA 3: Crear un alquiler de equipo.
try:
    equipo = AlquilerEquipo("E001", "Computador", 30000)
    print("\nPRUEBA 3: CORRECTA - Equipo creado.")
except Exception as error:
    print("PRUEBA 3: ERROR:", error)


# PRUEBA 4: Calcular el alquiler de un equipo.
try:
    total = equipo.calcular_costo(2)
    print("\nPRUEBA 4: CORRECTA - Costo del equipo:", total)
except Exception as error:
    print("PRUEBA 4: ERROR:", error)


# PRUEBA 5: Crear una asesoría especializada.
try:
    asesoria = AsesoriaEspecializada(
        "A001", "Asesoría tecnológica", 80000
    )
    print("\nPRUEBA 5: CORRECTA - Asesoría creada.")
except Exception as error:
    print("PRUEBA 5: ERROR:", error)


# PRUEBA 6: Calcular una asesoría con impuesto y descuento.
try:
    total = asesoria.calcular_costo(2, 19, 10)
    print("\nPRUEBA 6: CORRECTA - Costo de asesoría:", total)
except Exception as error:
    print("PRUEBA 6: ERROR:", error)


# PRUEBA 7: Intentar crear un servicio con tarifa negativa.
try:
    sala_error = ReservaSala("S002", "Sala pequeña", -50000)
    print("\nPRUEBA 7: ERROR - Aceptó una tarifa negativa.")
except ServicioInvalidoError as error:
    print("\nPRUEBA 7: CORRECTA -", error)


# PRUEBA 8: Intentar calcular una duración negativa.
try:
    sala.calcular_costo(-2)
    print("\nPRUEBA 8: ERROR - Aceptó duración negativa.")
except CalculoInconsistenteError as error:
    print("\nPRUEBA 8: CORRECTA -", error)


# PRUEBA 9: Intentar calcular un servicio no disponible.
try:
    sala.cambiar_disponibilidad(False)
    sala.calcular_costo(2)
    print("\nPRUEBA 9: ERROR - Aceptó servicio no disponible.")
except ServicioNoDisponibleError as error:
    print("\nPRUEBA 9: CORRECTA -", error)


# PRUEBA 10: Intentar crear directamente la clase abstracta.
try:
    servicio = Servicio("X001", "Servicio general", 50000)
    print("\nPRUEBA 10: ERROR - Permitió crear clase abstracta.")
except TypeError:
    print("\nPRUEBA 10: CORRECTA - No permite instanciar Servicio.")


print("\n======================================")
print(" FINALIZARON LAS PRUEBAS")
print("======================================")
