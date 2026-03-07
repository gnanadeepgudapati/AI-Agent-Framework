# agent/tool_registry.py
# This is the wiring layer. It collects all tools from all plugins
# and hands them to the agent in one clean list.
# In Phase 2, we import real plugin tools here. For now it returns an empty list.

from langchain_core.tools import BaseTool

# Phase 2 imports will look like this:
# from plugins.hris_plugin import get_leave_balance, get_payroll_info
# from plugins.itsm_plugin import create_ticket, reset_password
# from plugins.facilities_plugin import book_room, report_maintenance


def get_all_tools() -> list[BaseTool]:
    """
    Returns all registered tools for the agent.
    Each plugin exposes its tools here.
    Right now returns empty list — agent works but has no special abilities yet.
    Phase 2 will populate this.
    """
    tools = []

    # Phase 2: uncomment and add real tools
    # tools.extend(hris_tools)
    # tools.extend(itsm_tools)
    # tools.extend(facilities_tools)

    return tools