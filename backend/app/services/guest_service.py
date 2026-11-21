from ..repositories import guest_repository
from . import NotFoundError, ConflictError


def list_guests():
    return guest_repository.get_all_guests()


def get_guest(guest_id):
    guest = guest_repository.get_guest(guest_id)

    if guest is None:
        raise NotFoundError("Huésped no encontrado")

    return guest


def create_guest(full_name, email, document):
    if guest_repository.get_guest_by_email(email):
        raise ConflictError("Ya existe un huésped con ese email")

    return guest_repository.create_guest(full_name, email, document)


def delete_guest(guest_id):
    guest = get_guest(guest_id)

    if guest.reservations:
        raise ConflictError("El huésped tiene reservas registradas")

    guest_repository.delete_guest(guest)