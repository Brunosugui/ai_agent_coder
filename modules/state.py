from dataclasses import dataclass
from modules.planner.state import PlannerState


@dataclass
class AgentState:
    plannerState: PlannerState
