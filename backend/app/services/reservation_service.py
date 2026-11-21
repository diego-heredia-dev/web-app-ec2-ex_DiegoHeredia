from datetime import date

from ..models import Reservation
from ..repositories import reservation_repository
from . import BusinessRuleError


def create_reservation(room_id, guest_id, check_in, check_out, guests_count):
    if check_out <= check_in:
        raise BusinessRuleError(
            "La fecha de salida debe ser posterior a la fecha de ingreso."
        )

    if check_in < date.today():
        raise BusinessRuleError(
            "No se pueden realizar reservas para fechas pasadas."
        )

    room = reservation_repository.get_room(room_id)
    if room is None:
        raise ValueError("Habitación no encontrada")

    guest = reservation_repository.get_guest(guest_id)
    if guest is None:
        raise ValueError("Huésped no encontrado")

    if guests_count <= 0 or guests_count > room.capacity:
        raise BusinessRuleError(
            "La cantidad de huéspedes supera la capacidad de la habitación."
        )
    
    if room.status != "available":
        raise BusinessRuleError(
            "La habitación no está disponible para reservas."
        )

    if reservation_repository.has_overlapping_reservation(
        room_id, check_in, check_out
    ):
        raise BusinessRuleError(
            "La habitación ya tiene una reserva para esas fechas."
        )

    nights = (check_out - check_in).days
    total_price = nights * room.price_per_night

    reservation = Reservation(
        room=room,
        guest=guest,
        check_in=check_in,
        check_out=check_out,
        guests_count=guests_count,
        status="confirmed",
        total_price=total_price,
    )

    return reservation_repository.save_reservation(reservation)