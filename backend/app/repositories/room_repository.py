from ..models import Room, db


def get_room(room_id):
    return db.session.get(Room, room_id)


def get_all_rooms(status=None):
    query = Room.query

    if status:
        query = query.filter_by(status=status)

    return query.order_by(Room.number).all()


def get_room_by_number(number):
    return Room.query.filter_by(number=number).first()


def create_room(number, room_type, price, capacity, status):
    room = Room(
        number=number,
        type=room_type,
        price_per_night=price,
        capacity=capacity,
        status=status
    )

    db.session.add(room)
    db.session.commit()

    return room


def update_room(room):
    db.session.commit()
    return room


def delete_room(room):
    db.session.delete(room)
    db.session.commit()