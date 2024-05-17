import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Envelope:
    messageId: str
    traceId: str
    sessionId: str
