from datetime import date

from flask import Blueprint, jsonify, request

from ..models import Guest, Reservation, Room, db
from ..views.reservation_view import reservation_to_dict, reservations_to_list
from ..services import BusinessRuleError
from ..services.reservation_service import create_reservation as create_reservation_service

reservation_bp = Blueprint("reservations", __name__, url_prefix="/api/reservations")


@reservation_bp.get("")
def list_reservations():
    query = Reservation.query
    status = request.args.get("status")
    guest_id = request.args.get("guest_id", type=int)
    if status:
        query = query.filter_by(status=status)
    if guest_id:
        query = query.filter_by(guest_id=guest_id)
    reservations = query.order_by(Reservation.check_in).all()
    return jsonify(reservations_to_list(reservations))


@reservation_bp.get("/<int:reservation_id>")
def get_reservation(reservation_id):
    reservation = db.session.get(Reservation, reservation_id)
    if reservation is None:
        return jsonify({"error": "Reserva no encontrada"}), 404
    return jsonify(reservation_to_dict(reservation))


@reservation_bp.post("")
def create_reservation():
    data = request.get_json(silent=True) or {}

    missing = [
        f for f in ("room_id", "guest_id", "check_in", "check_out", "guests_count")
        if data.get(f) in (None, "")
    ]

    if missing:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400

    try:
        check_in = date.fromisoformat(data["check_in"])
        check_out = date.fromisoformat(data["check_out"])
        room_id = int(data["room_id"])
        guest_id = int(data["guest_id"])
        guests_count = int(data["guests_count"])

    except (TypeError, ValueError):
        return jsonify({
            "error": "Datos inválidos. Verifique las fechas y los valores numéricos."
        }), 400

    try:
        reservation = create_reservation_service(
            room_id,
            guest_id,
            check_in,
            check_out,
            guests_count
        )

    except BusinessRuleError as error:
        return jsonify({"error": str(error)}), 422

    except ValueError as error:
        return jsonify({"error": str(error)}), 404

    return jsonify(reservation_to_dict(reservation)), 201

@reservation_bp.patch("/<int:reservation_id>/cancel")
def cancel_reservation(reservation_id):
    reservation = db.session.get(Reservation, reservation_id)
    if reservation is None:
        return jsonify({"error": "Reserva no encontrada"}), 404

    reservation.status = "cancelled"
    db.session.commit()
    return jsonify(reservation_to_dict(reservation))


@reservation_bp.patch("/<int:reservation_id>/check-in")
def check_in_reservation(reservation_id):
    reservation = db.session.get(Reservation, reservation_id)
    if reservation is None:
        return jsonify({"error": "Reserva no encontrada"}), 404

    reservation.status = "checked_in"
    db.session.commit()
    return jsonify(reservation_to_dict(reservation))


@reservation_bp.patch("/<int:reservation_id>/check-out")
def check_out_reservation(reservation_id):
    reservation = db.session.get(Reservation, reservation_id)
    if reservation is None:
        return jsonify({"error": "Reserva no encontrada"}), 404

    reservation.status = "checked_out"
    db.session.commit()
    return jsonify(reservation_to_dict(reservation))
