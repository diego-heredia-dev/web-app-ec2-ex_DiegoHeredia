// URL del backend: mismo host desde donde se abrió la página, puerto 8000.
// Funciona igual en localhost y en la IP pública de la EC2.
import {
  listRooms,
  createRoom,
  updateRoom,
  deleteRoom as deleteRoomAPI,
  listGuests,
  createGuest,
  deleteGuest as deleteGuestAPI,
  listReservations,
  createReservation,
  updateReservation
} from "./api.js";

const ROOM_TYPES = { single: "Simple", double: "Doble", family: "Familiar", suite: "Suite" };
const STATUS_LABELS = {
  available: "Disponible", maintenance: "Mantenimiento",
  confirmed: "Confirmada", checked_in: "Hospedado", checked_out: "Finalizada", cancelled: "Cancelada",
};

// ---------- utilidades ----------
function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function showMessage(text, isError) {
  const msg = document.getElementById("msg");
  msg.textContent = text;
  msg.className = isError
    ? "notification notification--error"
    : "notification";
  msg.hidden = false;
  clearTimeout(showMessage.timer);
  showMessage.timer = setTimeout(() => { msg.hidden = true; }, 4000);
}

// ---------- pestañas ----------
document.querySelectorAll(".tabs__button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tabs__button").forEach((b) => {
      b.classList.remove("tabs__button--active");
    });

    button.classList.add("tabs__button--active");

    document.querySelectorAll(".page-section").forEach((section) => {
      section.hidden = true;
    });

    document.getElementById("tab-" + button.dataset.tab).hidden = false;
  });
});

// ---------- habitaciones ----------
async function loadRooms() {
  try {
    const rooms = await listRooms();
    const body = document.getElementById("rooms-body");
    if (rooms.length === 0) {
      body.innerHTML = '<tr><td colspan="6" class="empty-state">No hay habitaciones</td></tr>';
    } else {
      body.innerHTML = rooms.map((r) => `
        <tr>
          <td>${esc(r.number)}</td>
          <td>${esc(ROOM_TYPES[r.type] || r.type)}</td>
          <td>Bs ${esc(r.price_per_night)}</td>
          <td>${esc(r.capacity)}</td>
          <td><span class="status-badge status-badge--${esc(r.status)}">${esc(STATUS_LABELS[r.status])}</span></td>
          <td>
            <button class="button button--small button--secondary" onclick="toggleMaintenance(${r.id}, '${esc(r.status)}')">
              ${r.status === "maintenance" ? "Habilitar" : "Mantenimiento"}
            </button>
            <button class="button button--small button--danger" onclick="deleteRoom(${r.id})">Eliminar</button>
          </td>
        </tr>`).join("");
    }
    // también llena el select del formulario de reservas
    document.getElementById("reservation-room").innerHTML = rooms
      .map((r) => `<option value="${r.id}">${esc(r.number)} · ${esc(ROOM_TYPES[r.type])} · Bs ${esc(r.price_per_night)}</option>`)
      .join("");
  } catch (error) {
    showMessage("No se pudo conectar con el servidor", true);
  }
}

document.getElementById("room-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));
  data.price_per_night = Number(data.price_per_night);
  data.capacity = Number(data.capacity);

  let body;

  try {
    body = await createRoom(data);
  } catch (error) {
    showMessage(error.message, true);
    return;
  }

  form.reset();
  showMessage("Habitación " + body.number + " creada");
  loadRooms();
});

async function toggleMaintenance(id, status) {
  try {
    await updateRoom(id, {
      status: status === "maintenance" ? "available" : "maintenance"
    });
  } catch (error) {
    showMessage(error.message, true);
    return;
  }
  loadRooms();
}

async function deleteRoom(id) {
  if (!confirm("¿Eliminar la habitación?")) return;

  try {
    await deleteRoomAPI(id);
  } catch (error) {
    showMessage(error.message, true);
    return;
  }
  showMessage("Habitación eliminada");
  loadRooms();
}

// ---------- huéspedes ----------
async function loadGuests() {
  try {
    const guests = await listGuests();
    const body = document.getElementById("guests-body");
    if (guests.length === 0) {
      body.innerHTML = '<tr><td colspan="4" class="empty-state">No hay huéspedes</td></tr>';
    } else {
      body.innerHTML = guests.map((g) => `
        <tr>
          <td>${esc(g.full_name)}</td>
          <td>${esc(g.email)}</td>
          <td>${esc(g.document)}</td>
          <td><button class="button button--small button--danger" onclick="deleteGuest(${g.id})">Eliminar</button></td>
        </tr>`).join("");
    }
    document.getElementById("reservation-guest").innerHTML = guests
      .map((g) => `<option value="${g.id}">${esc(g.full_name)}</option>`)
      .join("");
  } catch (error) {
    showMessage("No se pudo conectar con el servidor", true);
  }
}

document.getElementById("guest-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));

  let body;

  try {
    body = await createGuest(data);
  } catch (error) {
    showMessage(error.message, true);
    return;
  }

  form.reset();
  showMessage("Huésped " + body.full_name + " registrado");
  loadGuests();
});

async function deleteGuest(id) {
  if (!confirm("¿Eliminar el huésped?")) return;
  try {
    await deleteGuestAPI(id);
  } catch (error) {
    showMessage(error.message, true);
    return;
  }
  showMessage("Huésped eliminado");
  loadGuests();
}

// ---------- reservas ----------
async function loadReservations() {
  try {
    const status = document.getElementById("reservation-filter").value;
    const reservations = await listReservations(status);
    const body = document.getElementById("reservations-body");
    if (reservations.length === 0) {
      body.innerHTML = '<tr><td colspan="10" class="empty-state">No hay reservas</td></tr>';
      return;
    }
    body.innerHTML = reservations.map((r) => `
      <tr>
        <td>${r.id}</td>
        <td>${esc(r.room_number)}</td>
        <td>${esc(r.guest_name)}</td>
        <td>${esc(r.check_in)}</td>
        <td>${esc(r.check_out)}</td>
        <td>${esc(r.nights)}</td>
        <td>${esc(r.guests_count)}</td>
        <td>${esc(r.total_price)}</td>
        <td><span class="status-badge status-badge--${esc(r.status)}">${esc(STATUS_LABELS[r.status])}</span></td>
        <td>
          <button class="button button--small button--success" onclick="changeReservation(${r.id}, 'check-in')">Check-in</button>
          <button class="button button--small" onclick="changeReservation(${r.id}, 'check-out')">Check-out</button>
          <button class="button button--small button--danger" onclick="changeReservation(${r.id}, 'cancel')">Cancelar</button>
        </td>
      </tr>`).join("");
  } catch (error) {
    showMessage("No se pudo conectar con el servidor", true);
  }
}

document.getElementById("reservation-filter").addEventListener("change", loadReservations);

document.getElementById("reservation-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const data = Object.fromEntries(new FormData(form));
  data.room_id = Number(data.room_id);
  data.guest_id = Number(data.guest_id);
  data.guests_count = Number(data.guests_count);

  let body;

  try {
    body = await createReservation(data);
  } catch (error) {
    showMessage(error.message, true);
    return;
  }
  form.reset();
  showMessage("Reserva #" + body.id + " creada · total Bs " + body.total_price);
  loadReservations();
});

async function changeReservation(id, action) {
  let body;

  try {
    body = await updateReservation(id, action);
  } catch (error) {
    showMessage(error.message, true);
    return;
  }
  showMessage("Reserva #" + id + ": " + STATUS_LABELS[body.status]);
  loadReservations();
}

// ---------- inicio ----------
loadRooms();
loadGuests();
loadReservations();
