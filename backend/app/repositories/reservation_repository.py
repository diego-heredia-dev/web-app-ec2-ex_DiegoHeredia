from ..models import Reservation, Room, Guest, db


def get_room(room_id):
    return db.session.get(Room, room_id)


def get_guest(guest_id):
    return db.session.get(Guest, guest_id)


def get_reservation(reservation_id):
    return db.session.get(Reservation, reservation_id)


def get_all_reservations(status=None, guest_id=None):
    query = Reservation.query

    if status:
        query = query.filter_by(status=status)

    if guest_id:
        query = query.filter_by(guest_id=guest_id)

    return query.order_by(Reservation.check_in).all()


def has_overlapping_reservation(room_id, check_in, check_out):
    return Reservation.query.filter(
        Reservation.room_id == room_id,
        Reservation.status.in_(["confirmed", "checked_in"]),
        Reservation.check_in < check_out,
        Reservation.check_out > check_in
    ).first() is not None


def create_reservation(room, guest, check_in, check_out, guests_count, total_price):
    reservation = Reservation(
        room=room,
        guest=guest,
        check_in=check_in,
        check_out=check_out,
        guests_count=guests_count,
        status="confirmed",
        total_price=total_price,
    )

    db.session.add(reservation)
    db.session.commit()

    return reservation


def update_reservation_status(reservation, status):
    reservation.status = status
    db.session.commit()
    return reservation