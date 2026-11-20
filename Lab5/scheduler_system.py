"""Book conference rooms and allocate shared equipment by time slot."""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def parse_slot(time_slot):
    """Return validated integer hours for an HH-HH interval on one day."""
    if not isinstance(time_slot, str):
        raise ValueError("Time slot must be a string such as 09-11.")
    parts = time_slot.split("-")
    if len(parts) != 2 or any(
        len(part) != 2 or not part.isascii() or not part.isdigit()
        for part in parts
    ):
        raise ValueError("Use two-digit hours, for example 09-11.")
    start, end = map(int, parts)
    if not 0 <= start < end <= 24:
        raise ValueError("Hours must satisfy 00 <= start < end <= 24.")
    return start, end


def slot_hours(time_slot):
    """Return the positive duration of a validated time slot."""
    start, end = parse_slot(time_slot)
    return end - start


class RoomScheduler:
    """Maintain an isolated schedule and equipment stock for a single day."""

    def __init__(self):
        self.reservations = {}
        self.equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
        self.conflicts = []
        self.next_reservation = 1

    def _check_room(self, room_id, start, end, time_slot):
        """Reject any intersecting interval in the requested room."""
        for reservation in self.reservations.values():
            old_start, old_end = parse_slot(reservation["slot"])
            if reservation["room"] == room_id and (
                start < old_end and old_start < end
            ):
                message = f"{room_id} double-booked at {time_slot}"
                self.conflicts.append(message)
                raise ValueError(message)

    def _check_equipment(self, requested, start, end):
        """Check stock against overlapping bookings, including duplicates."""
        unknown = requested.keys() - self.equipment_pool.keys()
        if unknown:
            raise ValueError(f"Unknown equipment: {', '.join(sorted(unknown))}")
        for hour in range(start, end):
            used = Counter()
            for reservation in self.reservations.values():
                old_start, old_end = parse_slot(reservation["slot"])
                if old_start <= hour < old_end:
                    used.update(reservation["equipment"])
            for item, quantity in requested.items():
                if used[item] + quantity > self.equipment_pool[item]:
                    raise ValueError(f"Insufficient {item} at hour {hour:02d}.")

    def schedule_room(self, room_id, time_slot, equipment_list=None):
        """Validate a booking fully before storing it; return its unique ID."""
        if not isinstance(room_id, str) or not room_id.strip():
            raise ValueError("Room ID must be a non-empty string.")
        room_id = room_id.strip()
        start, end = parse_slot(time_slot)
        if equipment_list is not None and not isinstance(
            equipment_list, (list, tuple)
        ):
            raise ValueError("Equipment must be a list or tuple of names.")
        equipment = list(equipment_list) if equipment_list is not None else []
        if any(not isinstance(item, str) for item in equipment):
            raise ValueError("Equipment names must be strings.")
        self._check_room(room_id, start, end, time_slot)
        self._check_equipment(Counter(equipment), start, end)
        reservation_id = self.next_reservation
        self.reservations[reservation_id] = {
            "room": room_id,
            "slot": time_slot,
            "equipment": equipment,
        }
        self.next_reservation += 1
        return reservation_id

    def cancel_reservation(self, reservation_id):
        """Remove a booking; return False for an unknown ID without masking errors."""
        return self.reservations.pop(reservation_id, None) is not None

    def export_schedule(self, filename="schedule.json"):
        """Export current reservations as UTF-8 JSON; propagate I/O errors."""
        with Path(filename).open("w", encoding="utf-8") as stream:
            json.dump(self.reservations, stream, indent=2)
            stream.write("\n")

    def log_conflicts(self, filename="conflicts.log"):
        """Append pending conflicts and display the log without invoking a shell."""
        path = Path(filename)
        with path.open("a", encoding="utf-8") as stream:
            for conflict in self.conflicts:
                stream.write(f"{datetime.now().isoformat()} {conflict}\n")
        self.conflicts.clear()
        print(path.read_text(encoding="utf-8"), end="")


def main():
    """Demonstrate bookings and report invalid inputs without crashing."""
    scheduler = RoomScheduler()
    scheduler.schedule_room("Board-1", "09-11")
    for room_id, time_slot in (
        ("Board-1", "09-11"),
        ("Huddle-3", "14-12"),
        ("Huddle-3", 1530),
    ):
        try:
            scheduler.schedule_room(room_id, time_slot)
        except ValueError as error:
            print(f"Booking rejected: {error}")
    print("Unknown cancellation:", scheduler.cancel_reservation(77))
    try:
        slot = input("Slot for Board-2, like 10-12 (Enter for 10-12): ")
    except EOFError:
        slot = ""
    slot = slot.strip() or "10-12"
    try:
        scheduler.schedule_room("Board-2", slot, ["projector", "webcam"])
        print("Slot length:", slot_hours(slot))
    except ValueError as error:
        print(f"Booking rejected: {error}")
    try:
        scheduler.export_schedule()
        scheduler.log_conflicts()
    except OSError as error:
        print(f"Unable to write schedule or log: {error}")
    print("Equipment capacity:", scheduler.equipment_pool)
    print("Reservations:", scheduler.reservations)


if __name__ == "__main__":
    main()
