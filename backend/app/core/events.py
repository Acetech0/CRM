from typing import Dict, List, Callable, Any
import asyncio

class EventDispatcher:
    _subscribers: Dict[str, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_name: str, handler: Callable):
        if event_name not in cls._subscribers:
            cls._subscribers[event_name] = []
        cls._subscribers[event_name].append(handler)

    @classmethod
    async def dispatch(cls, event_name: str, payload: Any):
        if event_name in cls._subscribers:
            for handler in cls._subscribers[event_name]:
                # Fire and forget / await
                # In real production, this might push to a queue (Kafka/Redis)
                if asyncio.iscoroutinefunction(handler):
                    await handler(payload)
                else:
                    handler(payload)

# Global Instance
dispatcher = EventDispatcher()
