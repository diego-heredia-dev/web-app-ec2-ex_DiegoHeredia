from ..models import Reservation, Room, Guest, db


def get_room(room_id):
    return db.session.get(Room, room_id)


def get_guest(guest_id):
    return db.session.get(Guest, guest_id)


def get_reservation(reservation_id):
    return db.session.get(Reservation, reservation_id)


def has_overlapping_reservation(room_id, check_in, check_out):
    return Reservation.query.filter(
        Reservation.room_id == room_id,
        Reservation.status.in_(["confirmed", "checked_in"]),
        Reservation.check_in < check_out,
        Reservation.check_out > check_in
    ).first() is not None


def save_reservation(reservation):
    db.session.add(reservation)
    db.session.commit()
    return reservation