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