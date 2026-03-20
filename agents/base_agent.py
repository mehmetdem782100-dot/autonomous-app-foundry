import abc
from uuid import UUID

class BaseAgent(abc.ABC):
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type

    @abc.abstractmethod
    async def process_task(self, task_id: UUID, payload: dict) -> dict:
        pass

    def log_action(self, message: str, level: str = "INFO"):
        print(f"[{level}] {self.agent_type} ({self.agent_id}): {message}")
