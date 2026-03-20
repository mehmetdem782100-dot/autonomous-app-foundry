class CognitaBaseException(Exception):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

class AgentExecutionError(CognitaBaseException): pass
class OrchestratorRoutingError(CognitaBaseException): pass
class SandboxTimeoutError(CognitaBaseException): pass
class InvalidPayloadError(CognitaBaseException): pass
