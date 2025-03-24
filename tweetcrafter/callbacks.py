import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Union


def _current_time() -> str:
    return datetime.now(UTC).isoformat()


def step_callback(
    agent_output: Union[Dict[str, Any], str],
    agent_name: str,
    log_file_path: Union[str, Path],
):
    """Log agent interactions to a file

    Args:
        agent_output: The output from the agent
        agent_name: Name of the agent
        log_file_path: Path to the log file
    """
    if isinstance(log_file_path, str):
        log_file_path = Path(log_file_path)
    
    if isinstance(agent_output, dict):
        log_data = {
            "agent": agent_name,
            "event": "agent_action",
            "timestamp": _current_time(),
            "prompt": agent_output.get("prompt", ""),
            "response": agent_output.get("response", ""),
        }
    else:
        log_data = {
            "agent": agent_name,
            "event": "agent_output",
            "timestamp": _current_time(),
            "output": str(agent_output),
        }
    
    with log_file_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(log_data) + "\n")
