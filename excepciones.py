

# ==========================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: excepciones.py
# DESCRIPCIÓN: Excepciones personalizadas del sistema
# ==========================================================

# Clase base para todos los errores del sistema.
class SistemaGestionError(Exception):
    """Excepción general del sistema Software FJ."""
    pass


# Error relacionado con datos incorrectos de clientes.
class ClienteInvalidoError(SistemaGestionError):
    pass


# Error cuando un cliente ya se encuentra registrado.
class ClienteDuplicadoError(SistemaGestionError):
    pass


# Error cuando faltan datos obligatorios.
class ParametroFaltanteError(SistemaGestionError):
    pass


# Error cuando los datos de un servicio son incorrectos.
class ServicioInvalidoError(SistemaGestionError):
    pass


# Error cuando un servicio no está disponible.
class ServicioNoDisponibleError(SistemaGestionError):
    pass


# Error cuando una reserva presenta datos incorrectos.
class ReservaInvalidaError(SistemaGestionError):
    pass


# Error cuando se intenta realizar una operación no permitida.
class OperacionNoPermitidaError(SistemaGestionError):
    pass


# Error cuando un cálculo produce un resultado inconsistente.
class CalculoInconsistenteError(SistemaGestionError):
    pass

