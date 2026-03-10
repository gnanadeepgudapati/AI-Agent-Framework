from langchain_core.tools import tool, BaseTool
from plugins.base_plugin import BasePlugin

# Mock HR database — simulates what a real HRIS system would return
# In production this would be an API call to Workday, SAP, etc.
MOCK_HR_DATA = {
    "EMP001": {"name": "Alex Johnson", "leave_balance": 14, "department": "Engineering"},
    "EMP002": {"name": "Sarah Chen", "leave_balance": 7,  "department": "Marketing"},
    "EMP003": {"name": "Marcus Riley", "leave_balance": 21, "department": "Sales"},
}

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
def request_time_off(employee_id : str, start_date: str, end_date: str, reason: str):
    """
    Submit a time off request for an employee.
    Use this when an employee wants to book, request, or apply for leave or vacation days.
    """
    from datetime import datetime

    employee = MOCK_HR_DATA.get(employee_id)

    if not employee:
        return f"No employee found with ID {employee_id}"
    
     # Calculate how many days they're requesting
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    days_requested = (end - start).days + 1

    if days_requested > employee["leave_balance"]:
        return (
            f"Sorry {employee['name']}, you requested {days_requested} days "
            f"but only have {employee['leave_balance']} remaining."
        )

    return (
        f"Time off request submitted for {employee['name']}. "
        f"Dates: {start_date} to {end_date}. "
        f"Days requested: {days_requested}. "
        f"Reason: {reason}. "
        f"Remaining balance after approval: {employee['leave_balance'] - days_requested} days."
    )

@tool
def get_payslip(employee_id: str, month: str, year: str) -> str:
    """
    Retrieve payslip information for an employee for a given month and year.
    Use this when an employee asks about their salary, payslip, or pay for a specific month.
    """
    from datetime import datetime

    employee = MOCK_HR_DATA.get(employee_id)

    if not employee:
        return f"No employee found with ID {employee_id}"

    # Can't request a payslip for a future month
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

    # Actually update the mock data
    MOCK_HR_DATA[employee_id][field] = new_value

    return (
        f"Successfully updated {field} for {employee['name']}. "
        f"New value: {new_value}. "
        f"Change logged and HR notified."
    )

def get_tools(self) -> list[BaseTool]:
        """
        Returns all HRIS tools for the agent.
        """
        return [
            get_leave_balance,
            request_time_off,
            get_payslip,
            update_personal_info,
        ]