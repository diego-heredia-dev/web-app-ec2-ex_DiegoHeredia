from flask import Blueprint, jsonify, request

from ..views.room_view import room_to_dict, rooms_to_list
from ..services import BusinessRuleError
from ..services import room_service

room_bp = Blueprint("rooms", __name__, url_prefix="/api/rooms")


@room_bp.get("")
def list_rooms():
    status = request.args.get("status")

    rooms = room_service.list_rooms(status)

    return jsonify(rooms_to_list(rooms))


@room_bp.get("/<int:room_id>")
def get_room(room_id):
    room = room_service.get_room(room_id)

    return jsonify(room_to_dict(room))


@room_bp.post("")
def create_room():
    data = request.get_json(silent=True) or {}

    missing = [
        f for f in ("number", "type", "price_per_night", "capacity")
        if data.get(f) in (None, "")
    ]

    if missing:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400

    try:
        price = float(data["price_per_night"])
        capacity = int(data["capacity"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "price_per_night y capacity deben ser números"
        }), 400

    room = room_service.create_room(
        str(data["number"]).strip(),
        data["type"],
        price,
        capacity,
        data.get("status", "available")
    )

    return jsonify(room_to_dict(room)), 201


@room_bp.put("/<int:room_id>")
def update_room(room_id):
    data = request.get_json(silent=True) or {}

    try:
        if "price_per_night" in data:
            data["price_per_night"] = float(data["price_per_night"])

        if "capacity" in data:
            data["capacity"] = int(data["capacity"])

    except (TypeError, ValueError):
        return jsonify({
            "error": "price_per_night y capacity deben ser números"
        }), 400

    room = room_service.update_room(room_id, data)

    return jsonify(room_to_dict(room))


@room_bp.delete("/<int:room_id>")
def delete_room(room_id):
    room_service.delete_room(room_id)

    return "", 204