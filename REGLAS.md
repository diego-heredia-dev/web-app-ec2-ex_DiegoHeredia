# Reglas de negocio - Hotel Mirador

## 1. Fechas de reserva válidas
- **Regla:** La fecha de salida (`check_out`) debe ser posterior a la fecha de ingreso (`check_in`) al momento de crear o modificar una reserva.
- **Respuesta API:** HTTP 422 - `{"error": "La fecha de salida debe ser posterior a la fecha de ingreso."}`

## 2. Reservas futuras
- **Regla:** La fecha de ingreso (`check_in`) de una nueva reserva no puede ser anterior a la fecha actual.
- **Respuesta API:** HTTP 422 - `{"error": "No se pueden realizar reservas para fechas pasadas."}`

## 3. Capacidad de habitación
- **Regla:** La cantidad de huéspedes de una reserva no puede superar la capacidad máxima de la habitación seleccionada.
- **Respuesta API:** HTTP 422 - `{"error": "La cantidad de huéspedes supera la capacidad de la habitación."}`

## 4. Habitaciones en mantenimiento
- **Regla:** No se puede crear una reserva para una habitación que se encuentre en mantenimiento o fuera de servicio.
- **Respuesta API:** HTTP 422 - `{"error": "La habitación no está disponible para reservas."}`

## 5. Disponibilidad de habitaciones
- **Regla:** Una habitación no puede tener dos reservas activas cuyos períodos de estadía se superpongan.
- **Respuesta API:** HTTP 422 - `{"error": "La habitación ya tiene una reserva para esas fechas."}`

## 6. Límite de reservas por huésped
- **Regla:** Un huésped no puede tener más de tres reservas activas simultáneamente al momento de crear una nueva reserva.
- **Respuesta API:** HTTP 422 - `{"error": "El huésped no puede tener más de tres reservas activas."}`

## 7. Descuento por estadías largas
- **Regla:** Las reservas cuya duración sea igual o superior a siete noches deben recibir automáticamente un descuento del 10 % sobre el total.
- **Respuesta API:** HTTP 200 - Devuelve el total de la reserva con el descuento del 10 % aplicado.

## 8. Penalización por cancelación tardía
- **Regla:** Cuando una reserva se cancela con menos de 48 horas de anticipación respecto a la fecha y hora de ingreso, se debe cobrar el importe correspondiente a la primera noche; si se cancela con 48 horas o más de anticipación, no se aplica penalización.
- **Respuesta API:** HTTP 200 - Devuelve la cancelación con el importe de la penalización correspondiente.

## 9. Check-in válido
- **Regla:** Solo se puede realizar el check-in de una reserva activa y a partir de su fecha de ingreso; no se permite realizarlo anticipadamente ni sobre reservas canceladas.
- **Respuesta API:** HTTP 422 - `{"error": "No se puede realizar el check-in para esta reserva."}`

## 10. Check-out válido
- **Regla:** Solo se puede realizar el check-out de una reserva que previamente haya registrado un check-in.
- **Respuesta API:** HTTP 422 - `{"error": "No se puede realizar el check-out sin haber registrado el check-in."}`



#	Regla	Dificultad	Dónde se aplica
1	Fechas válidas	Fácil	Crear reserva
2	Reservas futuras	Fácil	Crear reserva
3	Capacidad de habitación	Fácil	Crear reserva
4	Habitaciones en mantenimiento	Fácil	Crear reserva
5	Disponibilidad de habitación	Media	Crear reserva