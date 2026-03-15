# Troubleshooting Log

Real issues encountered during development and how they were resolved.

---

## Issue 1 — Wrong `langchain` Package Installed

**Date:** March 2026  
**Phase:** Phase 2 — Service Plugins

### What Happened

After installing `langchain` via pip, the server crashed with:

```
ImportError: cannot import name 'create_tool_calling_agent' from 'langchain.agents'
```

Running `python -c "from langchain import agents; print(dir(agents))"` showed only:

```
['AgentState', 'create_agent', 'factory', 'middleware', 'structured_output']
```

### Root Cause

There are two completely different packages on PyPI with similar names:

| Package | Version | What it is |
|---------|---------|------------|
| `langchain` (wrong) | 1.2.12 | An unrelated package that happens to share the name |
| `langchain` (correct) | 0.3.x | The official LangChain AI framework |

pip installed the wrong one because it was already cached from a previous install.

### Fix

Uninstall the wrong package and install the correct one explicitly:

```bash
pip uninstall langchain -y
pip install langchain==0.3.25 langchain-openai langchain-core
```

### Verify

```bash
python -c "import langchain; print(langchain.__version__)"
# Should print 0.3.25

python -c "from langchain.agents import create_tool_calling_agent; print('works')"
# Should print: works
```

---

## Issue 2 — Python 3.14 Incompatibility with LangChain Dependencies

**Date:** March 2026  
**Phase:** Phase 2 — Service Plugins

### What Happened

After fixing the wrong package issue, `langchain==0.3.7` still failed to install:

```
error: metadata-generation-failed
╰─> numpy

ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc'], ['clang']]
```

### Root Cause

Chain of failures caused by Python version being too new:

```
Python 3.14 — released too recently
    ↓
langchain 0.3.7 requires numpy<2.0.0
    ↓
numpy 1.26.x has no pre-built wheel for Python 3.14
    ↓
pip tries to compile numpy from source
    ↓
compiling from source requires a C compiler (gcc/clang/cl)
    ↓
no C compiler installed on the machine
    ↓
install fails completely
```

Additionally, LangChain's Pydantic V1 dependency showed this warning on every startup:

```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
```

### Fix

Two-part fix:

**Part 1** — Use a newer version of LangChain that doesn't require numpy:

```bash
pip install langchain==0.3.25 langchain-openai langchain-core
```

Version `0.3.25` dropped the numpy dependency entirely.

**Part 2** — If that still fails, create a virtual environment using Python 3.13 instead of 3.14. Python 3.13 has pre-built wheels for all dependencies:

```bash
# Check available Python versions
py --list

# Create new venv with Python 3.13
py -3.13 -m venv .venv313

# Activate it
.venv313\Scripts\activate  # Windows
source .venv313/bin/activate  # Mac/Linux

# Reinstall everything
pip install fastapi uvicorn pydantic python-dotenv httpx boto3
pip install langchain==0.3.25 langchain-openai langchain-core
```

### Verify

```bash
python --version
# Should print Python 3.13.x

python -c "from langchain.agents import create_tool_calling_agent; print('works')"
# Should print: works
```

### Lesson Learned

Always check Python version compatibility before starting a project. As a rule of thumb:

- **Use the latest-1 version** — if 3.14 is latest, use 3.13
- The newest Python release will often have missing pre-built wheels for popular packages for several months after release
- Check [https://pypi.org/project/numpy/#files](https://pypi.org/project/numpy/#files) to see if a pre-built wheel exists for your Python version before installing

---

## Issue 3 — `@abstractmethod` and `@property` Decorator Order

**Date:** March 2026  
**Phase:** Phase 2 — Service Plugins

### What Happened

All plugin imports failed with:

```
ImportError: cannot import name 'BasePlugin' from 'plugins.base_plugin'
```

### Root Cause

The decorators on the `name` property in `base_plugin.py` were in the wrong order:

```python
# WRONG — causes silent failure
@abstractmethod
@property
def name(self) -> str:
    pass
```

Python requires `@property` to come before `@abstractmethod`. When the order is reversed, Python cannot properly register the abstract property and the class behaves unexpectedly.

### Fix

```python
# CORRECT — property decorator must come first
@property
@abstractmethod
def name(self) -> str:
    pass
```

### Rule

When stacking decorators in Python, the order matters. For abstract properties specifically — `@property` always goes on top, `@abstractmethod` goes below it.

---

## Issue 4 — Tools Defined Inside Class Instead of Outside

**Date:** March 2026  
**Phase:** Phase 2 — Service Plugins

### What Happened

The agent was responding conversationally instead of calling tools. For example:

```
Query:   "How many vacation days does EMP001 have left?"
Expected: calls get_leave_balance tool, returns "Alex Johnson has 14 days"
Actual:   "I will route your request to the HR system... I don't have direct access..."
```

### Root Cause

LangChain `@tool` decorated functions were placed inside the plugin class as methods instead of as standalone functions outside the class:

```python
# WRONG — tools inside the class
class HRISPlugin(BasePlugin):
    @tool
    def get_leave_balance(employee_id: str) -> str:
        ...
```

When `@tool` is used inside a class, Python treats the function as a method and automatically injects `self` as the first argument. This breaks the tool signature — LangChain and GPT-4o receive an unexpected parameter and cannot call the tool correctly.

### Fix

All `@tool` decorated functions must live **outside** the class as standalone functions. The class only contains `name`, `description`, and `get_tools()`:

```python
# CORRECT — tools outside the class
@tool
def get_leave_balance(employee_id: str) -> str:
    ...

class HRISPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "hris"

    def get_tools(self) -> list[BaseTool]:
        return [get_leave_balance, ...]
```

### Rule

`@tool` functions are independent workers. The plugin class is just the manager that knows which workers belong to its team. Workers don't live inside the manager — they just report to it.

---

## General Setup Notes

**Recommended Python version:** 3.11 or 3.13 (not 3.14 — too new for most ML/AI packages)

**Virtual environment setup (Windows):**

```bash
py -3.13 -m venv .venv313
.venv313\Scripts\activate
pip install -r requirements.txt
```

**Virtual environment setup (Mac/Linux):**

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Verify all tools load correctly before starting server:**

```bash
python -c "from agent.tool_registry import get_all_tools; tools = get_all_tools(); print([t.name for t in tools])"
```

Should print all 16 tool names. If this errors — fix it before running the server.
