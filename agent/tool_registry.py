# agent/tool_registry.py
# This is the wiring layer. It collects all tools from all plugins
# and hands them to the agent in one clean list.

from langchain_core.tools import BaseTool
from plugins.hris_plugin import (
    get_leave_balance, request_time_off, get_payslip,
    update_personal_info, check_leave_request, cancel_leave_request,
)
from plugins.itsm_plugin import (
    create_ticket, get_ticket_status, reset_password, request_software,
)
from plugins.facilities_plugin import (
    book_meeting_room, check_room_availability, report_maintenance,
    check_maintenance_status, request_parking, cancel_parking,
)


def get_all_tools() -> list[BaseTool]:
    """
    Returns all registered tools for the agent.
    Each plugin exposes its tools here.
    """
    tools = [
        # HR
        get_leave_balance,
        request_time_off,
        get_payslip,
        update_personal_info,
        check_leave_request,
        cancel_leave_request,
        # IT
        create_ticket,
        get_ticket_status,
        reset_password,
        request_software,
        # Facilities
        book_meeting_room,
        check_room_availability,
        report_maintenance,
        check_maintenance_status,
        request_parking,
        cancel_parking,
    ]

    return tools