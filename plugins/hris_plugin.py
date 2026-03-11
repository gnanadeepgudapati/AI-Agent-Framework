import random
from datetime import datetime
from langchain_core.tools import tool, BaseTool
from plugins.base_plugin import BasePlugin

MOCK_HR_DATA = {
    "EMP001": {"name": "Alex Johnson", "leave_balance": 14, "department": "Engineering"},
    "EMP002": {"name": "Sarah Chen", "leave_balance": 7,  "department": "Marketing"},
    "EMP003": {"name": "Marcus Riley", "leave_balance": 21, "department": "Sales"},
}

MOCK_LEAVE_REQUESTS = {}


@tool
def get_leave_balance(employee_id: str) -> str:
    """
    Get the remaining leave balance for an employee.
    Use this when an employee asks how many vacation or leave days they have left.
    """
    employee = MOCK_HR_DATA.get(employee_id)
    if not employee:
        return f"No employee found with ID {employee_id}"
    return f"{employee['name']} has {employee['leave_balance']} vacation days remaining."


@tool
def request_time_off(employee_id: str, start_date: str, end_date: str, reason: str) -> str:
    """
    Submit a time off request for an employee.
    Use this when an employee wants to book, request, or apply for leave or vacation days.
    """
    employee = MOCK_HR_DATA.get(employee_id)

    if not employee:
        return f"No employee found with ID {employee_id}"

    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    days_requested = (end - start).days + 1

    if days_requested > employee["leave_balance"]:
        return (
            f"Sorry {employee['name']}, you requested {days_requested} days "
            f"but only have {employee['leave_balance']} remaining."
        )

    request_id = f"LVE-{random.randint(1000, 9999)}"
    while request_id in MOCK_LEAVE_REQUESTS:
        request_id = f"LVE-{random.randint(1000, 9999)}"

    MOCK_LEAVE_REQUESTS[request_id] = {
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "days_requested": days_requested,
        "reason": reason,
        "status": "pending",
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    return (
        f"Time off requested for {employee['name']}. "
        f"Request ID: {request_id}. "
        f"Dates: {start_date} to {end_date}. "
        f"Days requested: {days_requested}. "
        f"Reason: {reason}. "
        f"Status: Pending approval. "
        f"Remaining balance after approval: "
        f"{employee['leave_balance'] - days_requested} days."
    )


@tool
def get_payslip(employee_id: str, month: str, year: str) -> str:
    """
    Retrieve payslip information for an employee for a given month and year.
    Use this when an employee asks about their salary, payslip, or pay for a specific month.
    """
    employee = MOCK_HR_DATA.get(employee_id)

    if not employee:
        return f"No employee found with ID {employee_id}"

    requested = datetime.strptime(f"{month} {year}", "%B %Y")
    if requested > datetime.now():
        return (
            f"Payslip for {month} {year} is not available yet. "
            f"Payslips are generated at end of each month."
        )

    return (
        f"Payslip for {employee['name']} — {month} {year}. "
        f"Department: {employee['department']}. "
        f"Gross salary: $5,200. Net salary: $3,900. "
        f"Deductions: $1,300 (tax + benefits). "
        f"Status: Processed and paid."
    )


@tool
def update_personal_info(employee_id: str, field: str, new_value: str) -> str:
    """
    Update personal information for an employee such as phone number, address, or emergency contact.
    Use this when an employee wants to change or update their personal details.
    """
    employee = MOCK_HR_DATA.get(employee_id)

    if not employee:
        return f"No employee found with ID {employee_id}"

    allowed_fields = ["phone", "address", "emergency_contact"]

    if field not in allowed_fields:
        return (
            f"Cannot update '{field}'. "
            f"Allowed fields: {', '.join(allowed_fields)}"
        )

    MOCK_HR_DATA[employee_id][field] = new_value

    return (
        f"Successfully updated {field} for {employee['name']}. "
        f"New value: {new_value}. "
        f"Change logged and HR notified."
    )


@tool
def check_leave_request(request_id: str) -> str:
    """
    Check the status of a previously submitted leave or time off request.
    Use this when an employee wants to follow up on a leave request they submitted.
    """
    request = MOCK_LEAVE_REQUESTS.get(request_id)

    if not request:
        return (
            f"No leave request found with ID {request_id}. "
            f"Please check the request ID and try again."
        )

    return (
        f"Leave Request {request_id} — "
        f"Status: {request['status'].upper()}. "
        f"Dates: {request['start_date']} to {request['end_date']}. "
        f"Days: {request['days_requested']}. "
        f"Reason: {request['reason']}. "
        f"Submitted: {request['submitted_at']}."
    )


@tool
def cancel_leave_request(employee_id: str, request_id: str) -> str:
    """
    Cancel a previously submitted leave or time off request.
    Use this when an employee wants to cancel or withdraw a leave request.
    """
    request = MOCK_LEAVE_REQUESTS.get(request_id)

    if not request:
        return (
            f"No leave request found with ID {request_id}. "
            f"Please check the request ID and try again."
        )

    if request["employee_id"] != employee_id:
        return "You can only cancel your own leave requests."

    if request["status"] in ["approved", "cancelled"]:
        return (
            f"Cannot cancel request {request_id}. "
            f"Current status: {request['status'].upper()}."
        )

    days_to_restore = request["days_requested"]
    employee = MOCK_HR_DATA.get(employee_id)
    employee["leave_balance"] += days_to_restore
    MOCK_LEAVE_REQUESTS[request_id]["status"] = "cancelled"

    return (
        f"Leave request {request_id} cancelled successfully. "
        f"{days_to_restore} days restored to your balance. "
        f"New balance: {employee['leave_balance']} days."
    )


class HRISPlugin(BasePlugin):
    """
    HR Information System plugin.
    Handles leave balances, payroll, and employee info.
    """

    @property
    def name(self) -> str:
        return "hris"

    @property
    def description(self) -> str:
        return "Handles HR requests — leave balances, payroll, and employee information"

    def get_tools(self) -> list[BaseTool]:
        return [
            get_leave_balance,
            request_time_off,
            check_leave_request,
            cancel_leave_request,
            get_payslip,
            update_personal_info,
        ]