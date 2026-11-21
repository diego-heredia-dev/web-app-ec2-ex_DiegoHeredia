const API = `${location.protocol}//${location.hostname}:8000/api`;

async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, options);

  if (response.status === 204) {
    return null;
  }

  const body = await response.json();

  if (!response.ok) {
    throw new Error(body.error || "Ocurrió un error en el servidor");
  }

  return body;
}

function jsonOptions(method, data) {
  return {
    method,
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  };
}

export function listRooms() {
  return request("/rooms");
}

export function createRoom(data) {
  return request("/rooms", jsonOptions("POST", data));
}

export function updateRoom(id, data) {
  return request(`/rooms/${id}`, jsonOptions("PUT", data));
}

export function deleteRoom(id) {
  return request(`/rooms/${id}`, { method: "DELETE" });
}

export function listGuests() {
  return request("/guests");
}

export function createGuest(data) {
  return request("/guests", jsonOptions("POST", data));
}

export function deleteGuest(id) {
  return request(`/guests/${id}`, { method: "DELETE" });
}

export function listReservations(status = "") {
  const query = status ? `?status=${encodeURIComponent(status)}` : "";
  return request(`/reservations${query}`);
}

export function createReservation(data) {
  return request("/reservations", jsonOptions("POST", data));
}

export function updateReservation(id, action) {
  return request(`/reservations/${id}/${action}`, { method: "PATCH" });
}