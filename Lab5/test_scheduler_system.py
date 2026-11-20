"""Regression tests for the conference room scheduler."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scheduler_system import RoomScheduler, slot_hours


class SchedulerTests(unittest.TestCase):
    """Verify rejection, isolation, equipment reuse and file operations."""

    def setUp(self):
        self.scheduler = RoomScheduler()

    def test_default_equipment_is_independent(self):
        first = self.scheduler.schedule_room("A", "09-10")
        second = self.scheduler.schedule_room("B", "09-10")
        self.scheduler.reservations[first]["equipment"].append("projector")
        self.assertEqual(self.scheduler.reservations[second]["equipment"], [])

    def test_callers_list_is_copied(self):
        equipment = ["projector"]
        booking = self.scheduler.schedule_room("A", "09-10", equipment)
        equipment.append("webcam")
        self.assertEqual(
            self.scheduler.reservations[booking]["equipment"], ["projector"]
        )

    def test_same_and_partially_overlapping_room_is_rejected(self):
        self.scheduler.schedule_room("A", "09-11")
        for slot in ("09-11", "10-12", "08-10", "08-12"):
            with self.assertRaises(ValueError):
                self.scheduler.schedule_room("A", slot)
        self.assertEqual(len(self.scheduler.reservations), 1)
        self.assertEqual(self.scheduler.next_reservation, 2)

    def test_adjacent_slots_are_allowed(self):
        self.scheduler.schedule_room("A", "09-11")
        self.scheduler.schedule_room("A", "11-12")
        self.assertEqual(len(self.scheduler.reservations), 2)

    def test_invalid_slots(self):
        for slot in (1530, "14-12", "10-10", "24-25", "9-11", "aa-bb"):
            with self.subTest(slot=slot), self.assertRaises(ValueError):
                self.scheduler.schedule_room("A", slot)
        self.assertEqual(self.scheduler.reservations, {})
        self.assertEqual(slot_hours("00-24"), 24)

    def test_invalid_room_and_equipment_inputs(self):
        for room in (None, "", " "):
            with self.assertRaises(ValueError):
                self.scheduler.schedule_room(room, "09-10")
        for equipment in ("webcam", [None], ["unknown"]):
            with self.assertRaises(ValueError):
                self.scheduler.schedule_room("A", "09-10", equipment)

    def test_equipment_cannot_be_overbooked(self):
        self.scheduler.schedule_room("A", "09-11", ["webcam"])
        with self.assertRaises(ValueError):
            self.scheduler.schedule_room("B", "10-12", ["webcam"])
        self.assertEqual(len(self.scheduler.reservations), 1)

    def test_duplicate_equipment_quantities(self):
        with self.assertRaises(ValueError):
            self.scheduler.schedule_room("A", "09-11", ["webcam"] * 2)
        self.scheduler.schedule_room("A", "09-11", ["projector"] * 2)

    def test_equipment_reused_in_nonoverlapping_slots(self):
        self.scheduler.schedule_room("A", "09-11", ["webcam"])
        self.scheduler.schedule_room("B", "11-13", ["webcam"])
        self.assertEqual(len(self.scheduler.reservations), 2)

    def test_disjoint_bookings_do_not_overcount_equipment(self):
        self.scheduler.schedule_room("A", "09-10", ["projector"])
        self.scheduler.schedule_room("B", "10-11", ["projector"])
        self.scheduler.schedule_room("C", "09-11", ["projector"])
        self.assertEqual(len(self.scheduler.reservations), 3)

    def test_cancellation_frees_capacity_and_is_idempotent(self):
        booking = self.scheduler.schedule_room("A", "09-11", ["webcam"])
        self.assertTrue(self.scheduler.cancel_reservation(booking))
        self.assertFalse(self.scheduler.cancel_reservation(booking))
        self.assertFalse(self.scheduler.cancel_reservation(77))
        self.scheduler.schedule_room("B", "09-11", ["webcam"])

    def test_instances_are_isolated(self):
        self.scheduler.schedule_room("A", "09-11", ["webcam"])
        other = RoomScheduler()
        self.assertEqual(other.reservations, {})
        self.assertEqual(other.equipment_pool["webcam"], 1)

    def test_export_and_log_treat_shell_characters_as_filename(self):
        self.scheduler.schedule_room("A", "09-11")
        with self.assertRaises(ValueError):
            self.scheduler.schedule_room("A", "09-11")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "schedule.json"
            log = Path(directory) / "conflicts & echo injected.log"
            self.scheduler.export_schedule(output)
            self.assertEqual(json.loads(output.read_text())["1"]["room"], "A")
            with contextlib.redirect_stdout(io.StringIO()):
                self.scheduler.log_conflicts(log)
                self.scheduler.log_conflicts(log)
            self.assertEqual(log.read_text().count("double-booked"), 1)

    def test_io_errors_are_visible(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing" / "schedule.json"
            with self.assertRaises(OSError):
                self.scheduler.export_schedule(missing)


if __name__ == "__main__":
    unittest.main()
