from langchain_core.tools import tool, BaseTool
from plugins.base_plugin import BasePlugin
from datetime import datetime, timedelta
import random

MOCK_ROOMS = {
    "ROOM-A": {"name": "boardroom", "capacity": 20, "floor": 1, "bookings": []},
    "ROOM-B": {"name": "meeting room 1", "capacity": 8, "floor": 2, "bookings": []},
    "ROOM-C": {"name": "meeting room 2", "capacity": 8, "floor": 2, "bookings": []},
    "ROOM-D": {"name": "huddle room", "capacity": 4, "floor": 3, "bookings": []},
}

MOCK_PARKING = {
    "total_spots": 50,
    "available_spots": 23,
    "reservations": {}
}

MOCK_MAINTENANCE = {}


@tool
def book_meeting_room(
    employee_id: str,
    start_date: str,
    end_date: str,
    time: str,
    capacity_needed: int
) -> str:
    """
    Book a meeting room for an employee for a single day or multiple consecutive days.
    Use this when an employee wants to reserve or book a meeting room or conference room.
    start_date and end_date should be in YYYY-MM-DD format.
    For a single day booking, start_date and end_date should be the same.
    Capacity needed is the number of people attending.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if end < start:
        return "End date cannot be before start date."

    all_dates = []
    current = start
    while current <= end:
        all_dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    days_requested = len(all_dates)

    available_room = None
    for room_id, room in MOCK_ROOMS.items():
        if room["capacity"] >= capacity_needed:
            conflict = any(
                b["date"] in all_dates and b["time"] == time
                for b in room["bookings"]
            )
            if not conflict:
                available_room = (room_id, room)
                break

    if not available_room:
        return (
            f"No available rooms for {capacity_needed} people "
            f"from {start_date} to {end_date} at {time}. "
            f"Please try different dates or time."
        )

    room_id, room = available_room
    booking_ref = f"BKG-{random.randint(1000, 9999)}"
    while any(
        b["ref"] == booking_ref
        for r in MOCK_ROOMS.values()
        for b in r["bookings"]
    ):
        booking_ref = f"BKG-{random.randint(1000, 9999)}"

    for date in all_dates:
        room["bookings"].append({
            "ref": booking_ref,
            "employee_id": employee_id,
            "date": date,
            "time": time,
            "capacity_needed": capacity_needed,
        })

    return (
        f"Room booked successfully. "
        f"Booking reference: {booking_ref}. "
        f"Room: {room['name'].title()} (Floor {room['floor']}). "
        f"Capacity: {room['capacity']} people. "
        f"Dates: {start_date} to {end_date} ({days_requested} days) at {time}."
    )


@tool
def check_room_availability(date: str, capacity_needed: int) -> str:
    """
    Check which meeting rooms are available on a specific date.
    Use this when an employee wants to see available rooms before making a booking.
    """
    available_rooms = []

    for room_id, room in MOCK_ROOMS.items():
        if room["capacity"] >= capacity_needed:
            booked_times = [
                b["time"] for b in room["bookings"]
                if b["date"] == date
            ]
            available_rooms.append(
                f"{room['name'].title()} (Floor {room['floor']}, "
                f"Capacity: {room['capacity']}) — "
                f"Booked times: {', '.join(booked_times) if booked_times else 'fully available'}"
            )

    if not available_rooms:
        return (
            f"No rooms available for {capacity_needed} people on {date}. "
            f"Try a different date."
        )

    return (
        f"Available rooms for {capacity_needed} people on {date}:\n" +
        "\n".join(available_rooms)
    )


@tool
def report_maintenance(employee_id: str, location: str, issue: str, urgency: str) -> str:
    """
    Report a maintenance issue in the building.
    Use this when an employee reports a physical problem in the office
    such as broken equipment, leaks, electrical issues, or cleaning needs.
    Urgency should be 'low', 'medium', or 'high'.
    """
    allowed_urgency = ["low", "medium", "high"]
    if urgency.lower() not in allowed_urgency:
        return (
            f"Invalid urgency '{urgency}'. "
            f"Must be one of: {', '.join(allowed_urgency)}"
        )

    report_id = f"MNT-{random.randint(1000, 9999)}"
    while report_id in MOCK_MAINTENANCE:
        report_id = f"MNT-{random.randint(1000, 9999)}"

    MOCK_MAINTENANCE[report_id] = {
        "employee_id": employee_id,
        "location": location,
        "issue": issue,
        "urgency": urgency.lower(),
        "status": "reported",
        "reported_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assigned_to": "Facilities Team",
        "estimated_resolution": (
            "2 hours" if urgency.lower() == "high"
            else "1 business day" if urgency.lower() == "medium"
            else "3 business days"
        )
    }

    return (
        f"Maintenance issue reported successfully. "
        f"Report ID: {report_id}. "
        f"Location: {location}. "
        f"Issue: {issue}. "
        f"Urgency: {urgency}. "
        f"Assigned to: Facilities Team. "
        f"Estimated resolution: {MOCK_MAINTENANCE[report_id]['estimated_resolution']}."
    )


@tool
def check_maintenance_status(report_id: str) -> str:
    """
    Check the status of a previously submitted maintenance report.
    Use this when an employee wants to follow up on a maintenance issue they reported.
    """
    report = MOCK_MAINTENANCE.get(report_id)

    if not report:
        return (
            f"No maintenance report found with ID {report_id}. "
            f"Please check the report ID and try again."
        )

    return (
        f"Maintenance Report {report_id} — "
        f"Status: {report['status'].upper()}. "
        f"Issue: {report['issue']}. "
        f"Location: {report['location']}. "
        f"Urgency: {report['urgency']}. "
        f"Reported at: {report['reported_at']}. "
        f"Assigned to: {report['assigned_to']}. "
        f"Estimated resolution: {report['estimated_resolution']}."
    )


@tool
def request_parking(employee_id: str, date: str, vehicle_number: str) -> str:
    """
    Reserve a parking spot for an employee on a specific date.
    Use this when an employee needs to reserve or book a parking spot.
    Date should be in YYYY-MM-DD format.
    """
    if employee_id in MOCK_PARKING["reservations"]:
        existing = MOCK_PARKING["reservations"][employee_id]
        if date in existing:
            return (
                f"You already have a parking reservation on {date}. "
                f"Vehicle: {existing[date]['vehicle_number']}."
            )

    if MOCK_PARKING["available_spots"] == 0:
        return (
            f"No parking spots available on {date}. "
            f"Please try a different date or contact facilities."
        )

    if employee_id not in MOCK_PARKING["reservations"]:
        MOCK_PARKING["reservations"][employee_id] = {}

    MOCK_PARKING["reservations"][employee_id][date] = {
        "vehicle_number": vehicle_number,
        "reserved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "spot_number": f"P-{random.randint(1, 50)}",
    }

    MOCK_PARKING["available_spots"] -= 1

    return (
        f"Parking spot reserved successfully. "
        f"Date: {date}. "
        f"Vehicle: {vehicle_number}. "
        f"Spot: {MOCK_PARKING['reservations'][employee_id][date]['spot_number']}. "
        f"Remaining spots today: {MOCK_PARKING['available_spots']}."
    )


@tool
def cancel_parking(employee_id: str, date: str) -> str:
    """
    Cancel an existing parking reservation for an employee on a specific date.
    Use this when an employee wants to cancel or remove a parking booking they made.
    """
    if employee_id not in MOCK_PARKING["reservations"]:
        return f"No parking reservations found for employee {employee_id}."

    if date not in MOCK_PARKING["reservations"][employee_id]:
        return (
            f"No parking reservation found for {date}. "
            f"Please check the date and try again."
        )

    cancelled = MOCK_PARKING["reservations"][employee_id][date]
    del MOCK_PARKING["reservations"][employee_id][date]
    MOCK_PARKING["available_spots"] += 1

    return (
        f"Parking reservation cancelled successfully. "
        f"Date: {date}. "
        f"Vehicle: {cancelled['vehicle_number']}. "
        f"Spot {cancelled['spot_number']} has been released. "
        f"Available spots: {MOCK_PARKING['available_spots']}."
    )


class FacilitiesPlugin(BasePlugin):
    """
    Facilities Management plugin.
    Handles room bookings, maintenance requests, and parking.
    """

    @property
    def name(self) -> str:
        return "facilities"

    @property
    def description(self) -> str:
        return "Handles facilities requests — room bookings, maintenance issues, and parking"

    def get_tools(self) -> list[BaseTool]:
        return [
            book_meeting_room,
            check_room_availability,
            report_maintenance,
            check_maintenance_status,
            request_parking,
            cancel_parking,
        ]