from ..repositories import room_repository
from . import NotFoundError, BusinessRuleError, ConflictError

ROOM_TYPES = ("single", "double", "family", "suite")
ROOM_STATUSES = ("available", "maintenance")


def list_rooms(status=None):
    return room_repository.get_all_rooms(status)


def get_room(room_id):
    room = room_repository.get_room(room_id)

    if room is None:
        raise NotFoundError("Habitación no encontrada")

    return room


def create_room(number, room_type, price, capacity, status):
    if room_type not in ROOM_TYPES:
        raise BusinessRuleError(
            f"Tipo inválido. Usa: {', '.join(ROOM_TYPES)}"
        )

    if status not in ROOM_STATUSES:
        raise BusinessRuleError(
            f"Estado inválido. Usa: {', '.join(ROOM_STATUSES)}"
        )

    if room_repository.get_room_by_number(number):
        raise ConflictError(
            "Ya existe una habitación con ese número"
        )

    return room_repository.create_room(
        number, room_type, price, capacity, status
    )


def update_room(room_id, data):
    room = get_room(room_id)

    if "type" in data:
        if data["type"] not in ROOM_TYPES:
            raise BusinessRuleError(
                f"Tipo inválido. Usa: {', '.join(ROOM_TYPES)}"
            )
        room.type = data["type"]

    if "status" in data:
        if data["status"] not in ROOM_STATUSES:
            raise BusinessRuleError(
                f"Estado inválido. Usa: {', '.join(ROOM_STATUSES)}"
            )
        room.status = data["status"]

    if "price_per_night" in data:
        room.price_per_night = data["price_per_night"]

    if "capacity" in data:
        room.capacity = data["capacity"]

    return room_repository.update_room(room)


def delete_room(room_id):
    room = get_room(room_id)

    if room.reservations:
        raise BusinessRuleError(
            "La habitación tiene reservas registradas"
        )

    room_repository.delete_room(room)