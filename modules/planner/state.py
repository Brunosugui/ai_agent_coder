from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class PlannerState:
    user_input: str
    output_path: str
    last_draft: str = ""
    last_reflection: str = ""
    next_node: str = "DrafterNode"
    messages: List[Dict[str, Any]] = field(default_factory=lambda: [])
    plan_dict: Dict[str, str] = field(default_factory=lambda: {})
    parse_retry: int = 0
    reflection_retry: int = 0
    plan_approved: bool = False
    used_rag: bool = False
    
