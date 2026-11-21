
# ==========================================================
# PRUEBAS DEL ARCHIVO ENTIDADES.PY
# ==========================================================

from entidades import EntidadGeneral, Cliente

from excepciones import (
    ClienteInvalidoError,
    ParametroFaltanteError
)

print("\n======================================")
print(" PRUEBAS DE ENTIDADES - SOFTWARE FJ")
print("======================================")

# PRUEBA 1: Crear un cliente correctamente.
try:
    cliente1 = Cliente(
        "1001",
        "Ana Gomez",
        "ana@correo.com"
    )

    print("\nPRUEBA 1 CORRECTA:")
    print(cliente1.describir_entidad())

except Exception as error:
    print("PRUEBA 1 FALLIDA:", error)


# PRUEBA 2: Comprobar que el nombre no acepte números.
try:
    cliente2 = Cliente(
        "1002",
        "Luis123",
        "luis@correo.com"
    )

except ClienteInvalidoError as error:
    print("\nPRUEBA 2 CORRECTA:", error)


# PRUEBA 3: Comprobar correo inválido.
try:
    cliente3 = Cliente(
        "1003",
        "Carlos Ruiz",
        "carlossincorreo.com"
    )

except ClienteInvalidoError as error:
    print("\nPRUEBA 3 CORRECTA:", error)


# PRUEBA 4: Comprobar identificación inválida.
try:
    cliente4 = Cliente(
        "ABC123",
        "Maria Torres",
        "maria@correo.com"
    )

except ClienteInvalidoError as error:
    print("\nPRUEBA 4 CORRECTA:", error)


# PRUEBA 5: Modificar el correo correctamente.
try:
    cliente1.correo = "ana.nuevo@correo.com"

    print("\nPRUEBA 5 CORRECTA:")
    print("Nuevo correo:", cliente1.correo)

except ClienteInvalidoError as error:
    print("PRUEBA 5 FALLIDA:", error)


# PRUEBA 6: Intentar modificar el correo con datos inválidos.
try:
    cliente1.correo = "correo_incorrecto"

except ClienteInvalidoError as error:
    print("\nPRUEBA 6 CORRECTA:", error)


# PRUEBA 7: Comprobar que la clase abstracta no se instancie.
try:
    entidad = EntidadGeneral()

except TypeError:
    print("\nPRUEBA 7 CORRECTA:")
    print("No es posible crear objetos de una clase abstracta.")


# PRUEBA 8: Comprobar un parámetro faltante.
try:
    cliente5 = Cliente(
        None,
        "Pedro Ramirez",
        "pedro@correo.com"
    )

except ParametroFaltanteError as error:
    print("\nPRUEBA 8 CORRECTA:", error)


print("\n======================================")
print(" FINALIZACIÓN DE LAS PRUEBAS")
print("======================================")
