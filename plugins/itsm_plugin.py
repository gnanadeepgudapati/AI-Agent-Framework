from langchain_core.tools import tool, BaseTool
from plugins.base_plugin import BasePlugin
from datetime import datetime
import random

MOCK_IT_DATA = {
    "EMP001": {"open_tickets": 2, "systems_access": ["Slack", "GitHub", "Jira"]},
    "EMP002": {"open_tickets": 0, "systems_access": ["Slack", "Salesforce"]},
    "EMP003": {"open_tickets": 1, "systems_access": ["Slack", "HubSpot", "Zoom"]},
}

MOCK_TICKETS = {}


@tool
def create_ticket(employee_id: str, issue: str, priority: str) -> str:
    """
    Create an IT support ticket for an employee.
    Use this when an employee reports a technical problem, bug, or IT issue that needs resolving.
    Priority should be 'low', 'medium', or 'high'.
    """
    employee_id_data = MOCK_IT_DATA.get(employee_id)

    if not employee_id_data:
        return f"No employee found with ID {employee_id}"

    allowed_priorities = ["low", "medium", "high"]
    if priority.lower() not in allowed_priorities:
        return (
            f"Invalid priority '{priority}'. "
            f"Must be one of: {', '.join(allowed_priorities)}"
        )

    ticket_id = f"TKT-{random.randint(1000, 9999)}"
    while ticket_id in MOCK_TICKETS:
        ticket_id = f"TKT-{random.randint(1000, 9999)}"

    MOCK_TICKETS[ticket_id] = {
        "employee_id": employee_id,
        "issue": issue,
        "priority": priority.lower(),
        "status": "open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assigned_to": "Auto-assigned to IT Support Team",
        "estimated_resolution": "2 hours" if priority.lower() == "high" else "1 business day",
    }

    MOCK_IT_DATA[employee_id]["open_tickets"] += 1

    return (
        f"IT ticket created successfully. "
        f"Ticket ID: {ticket_id}. "
        f"Issue: {issue}. "
        f"Priority: {priority}. "
        f"Status: Open. "
        f"Expected response time: {'2 hours' if priority.lower() == 'high' else '1 business day'}."
    )


@tool
def get_ticket_status(ticket_id: str) -> str:
    """
    Get the status of an existing IT support ticket.
    Use this when an employee asks about the progress or status of a ticket they raised.
    """
    ticket = MOCK_TICKETS.get(ticket_id)

    if not ticket:
        return f"No ticket found with ID {ticket_id}. Please check the ticket ID and try again."

    return (
        f"Ticket {ticket_id} — Status: {ticket['status'].upper()}. "
        f"Issue: {ticket['issue']}. "
        f"Priority: {ticket['priority']}. "
        f"Assigned to: {ticket['assigned_to']}. "
        f"Created: {ticket['created_at']}. "
        f"Estimated resolution: {ticket['estimated_resolution']}."
    )


@tool
def reset_password(employee_id: str, system: str) -> str:
    """
    Reset the password for an employee for a given system or application.
    Use this when an employee is locked out or needs a password reset for a specific system.
    """
    employee_data = MOCK_IT_DATA.get(employee_id)

    if not employee_data:
        return f"No employee found with ID {employee_id}"

    systems_lower = [s.lower() for s in employee_data["systems_access"]]
    if system.lower() not in systems_lower:
        return (
            f"Employee does not have access to {system}. "
            f"Current systems: {', '.join(employee_data['systems_access'])}. "
            f"Request access through your IT administrator."
        )

    return (
        f"Password reset initiated for {system}. "
        f"A temporary reset code has been sent to your registered email. "
        f"This code expires in 30 minutes. "
        f"You will be prompted to set a new password on first login."
    )


@tool
def request_software(employee_id: str, software_name: str, justification: str) -> str:
    """
    Submit a software access request for an employee.
    Use this when an employee wants to request access to a new software or application.
    """
    employee_data = MOCK_IT_DATA.get(employee_id)

    if not employee_data:
        return f"No employee found with ID {employee_id}"

    systems_lower = [s.lower() for s in employee_data["systems_access"]]
    if software_name.lower() in systems_lower:
        return (
            f"You already have access to {software_name}. "
            f"Current systems: {', '.join(employee_data['systems_access'])}."
        )

    request_id = f"REQ-{random.randint(1000, 9999)}"
    while request_id in MOCK_TICKETS:
        request_id = f"REQ-{random.randint(1000, 9999)}"

    MOCK_TICKETS[request_id] = {
        "employee_id": employee_id,
        "type": "software_request",
        "software": software_name,
        "justification": justification,
        "status": "pending_approval",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assigned_to": "IT Procurement Team",
        "estimated_resolution": "3-5 business days",
    }

    return (
        f"Software request submitted successfully. "
        f"Request ID: {request_id}. "
        f"Software: {software_name}. "
        f"Justification: {justification}. "
        f"Status: Pending manager approval. "
        f"Estimated provisioning time: 3-5 business days."
    )


class ITSMPlugin(BasePlugin):
    """
    IT Service Management plugin.
    Handles IT tickets, password resets, and software requests.
    """

    @property
    def name(self) -> str:
        return "itsm"

    @property
    def description(self) -> str:
        return "Handles IT requests — support tickets, password resets, and software access"

    def get_tools(self) -> list[BaseTool]:
        return [
            create_ticket,
            get_ticket_status,
            reset_password,
            request_software,
        ]