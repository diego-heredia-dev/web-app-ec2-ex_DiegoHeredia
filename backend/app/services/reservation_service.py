from datetime import date

from ..repositories import reservation_repository
from . import BusinessRuleError, NotFoundError


def create_reservation(room_id, guest_id, check_in, check_out, guests_count):

    # 1. Fechas válidas
    if check_out <= check_in:
        raise BusinessRuleError(
            "La fecha de salida debe ser posterior a la fecha de ingreso."
        )

    # 2. Reservas futuras
    if check_in < date.today():
        raise BusinessRuleError(
            "No se pueden realizar reservas para fechas pasadas."
        )

    room = reservation_repository.get_room(room_id)

    if room is None:
        raise NotFoundError("Habitación no encontrada")

    guest = reservation_repository.get_guest(guest_id)

    if guest is None:
        raise NotFoundError("Huésped no encontrado")

    # 3. Capacidad de habitación
    if guests_count <= 0 or guests_count > room.capacity:
        raise BusinessRuleError(
            "La cantidad de huéspedes supera la capacidad de la habitación."
        )

    # 4. Habitaciones en mantenimiento
    if room.status != "available":
        raise BusinessRuleError(
            "La habitación no está disponible para reservas."
        )

    # 5. Disponibilidad de habitación
    if reservation_repository.has_overlapping_reservation(
        room_id, check_in, check_out
    ):
        raise BusinessRuleError(
            "La habitación ya tiene una reserva para esas fechas."
        )

    nights = (check_out - check_in).days
    total_price = nights * room.price_per_night

    return reservation_repository.create_reservation(
        room,
        guest,
        check_in,
        check_out,
        guests_count,
        total_price
    )


def list_reservations(status=None, guest_id=None):
    return reservation_repository.get_all_reservations(status, guest_id)


def get_reservation(reservation_id):
    reservation = reservation_repository.get_reservation(reservation_id)

    if reservation is None:
        raise NotFoundError("Reserva no encontrada")

    return reservation


def cancel_reservation(reservation_id):
    reservation = get_reservation(reservation_id)

    return reservation_repository.update_reservation_status(
        reservation, "cancelled"
    )


def check_in_reservation(reservation_id):
    reservation = get_reservation(reservation_id)

    return reservation_repository.update_reservation_status(
        reservation, "checked_in"
    )


def check_out_reservation(reservation_id):
    reservation = get_reservation(reservation_id)

    return reservation_repository.update_reservation_status(
        reservation, "checked_out"
    )