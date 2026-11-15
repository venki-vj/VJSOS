"""
Plugin SDK - Event System

Provides event publishing and subscription for plugin integration
with the VJSOS-AI event bus.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List, AsyncIterator, Callable
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum


class EventPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Event:
    """Event structure for the VJSOS event bus."""
    event_id: str
    event_type: str
    source: str
    timestamp: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    priority: str = "normal"
    ttl_seconds: int = 3600

    @classmethod
    def create(cls, event_type: str, source: str, payload: Dict[str, Any],
               correlation_id: Optional[str] = None, priority: str = "normal") -> "Event":
        """Create a new event."""
        return cls(
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            event_type=event_type,
            source=source,
            timestamp=datetime.utcnow().isoformat() + "Z",
            payload=payload,
            correlation_id=correlation_id,
            priority=priority
        )


class EventPublisher:
    """Publishes events to the VJSOS event bus."""

    def __init__(self, plugin_id: str, event_bus=None):
        self.plugin_id = plugin_id
        self.event_bus = event_bus
        self.published_events: List[Event] = []

    async def publish(self, event_type: str, payload: Dict[str, Any],
                     correlation_id: Optional[str] = None, priority: str = "normal") -> Event:
        """Publish an event to the bus."""
        event = Event.create(
            event_type=event_type,
            source=self.plugin_id,
            payload=payload,
            correlation_id=correlation_id,
            priority=priority
        )

        self.published_events.append(event)

        if self.event_bus:
            await self.event_bus.publish(event)

        return event

    async def publish_batch(self, events: List[Dict[str, Any]]) -> List[Event]:
        """Publish multiple events."""
        published = []
        for event_data in events:
            event = await self.publish(
                event_type=event_data.get("event_type", ""),
                payload=event_data.get("payload", {}),
                correlation_id=event_data.get("correlation_id"),
                priority=event_data.get("priority", "normal")
            )
            published.append(event)
        return published

    def get_published_count(self) -> int:
        """Get count of events published by this plugin."""
        return len(self.published_events)


class EventSubscriber:
    """Subscribes to and handles events from the VJSOS event bus."""

    def __init__(self, plugin_id: str, event_bus=None):
        self.plugin_id = plugin_id
        self.event_bus = event_bus
        self.handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.subscriptions: List[str] = []
        self.received_events: List[Event] = []
        self._running = False
        self._handler_task = None

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to an event type with a handler."""
        self.handlers[event_type].append(handler)
        if event_type not in self.subscriptions:
            self.subscriptions.append(event_type)

    def unsubscribe(self, event_type: str):
        """Unsubscribe from an event type."""
        if event_type in self.handlers:
            del self.handlers[event_type]
        if event_type in self.subscriptions:
            self.subscriptions.remove(event_type)

    async def handle_event(self, event: Event) -> Optional[Dict[str, Any]]:
        """Process a received event through registered handlers."""
        self.received_events.append(event)

        handlers = self.handlers.get(event.event_type, [])
        handlers += self.handlers.get("*", [])  # Wildcard handlers

        results = []
        for handler in handlers:
            try:
                result = await handler(event)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Error in event handler for {event.event_type}: {e}")

        return results[0] if results else None

    async def start_listening(self):
        """Start listening for events from the event bus."""
        if self._running:
            return

        self._running = True
        if self.event_bus:
            await self.event_bus.subscribe(self, self.subscriptions)
            self._handler_task = asyncio.create_task(self._listen_loop())

    async def stop_listening(self):
        """Stop listening for events."""
        self._running = False
        if self.event_bus:
            await self.event_bus.unsubscribe(self)
        if self._handler_task:
            self._handler_task.cancel()
            try:
                await self._handler_task
            except asyncio.CancelledError:
                pass

    async def _listen_loop(self):
        """Internal event listening loop."""
        while self._running:
            # In a real implementation, this would pull from the event bus
            # For now, this is a placeholder
            await asyncio.sleep(1)

    def get_received_count(self) -> int:
        """Get count of events received by this plugin."""
        return len(self.received_events)


class EventStream:
    """Async event stream for real-time event processing."""

    def __init__(self, subscriber: EventSubscriber):
        self.subscriber = subscriber
        self._queue = asyncio.Queue()

    async def __aiter__(self) -> AsyncIterator[Event]:
        """Async iterator over events."""
        while True:
            event = await self._queue.get()
            yield event

    async def push(self, event: Event):
        """Push an event to the stream."""
        await self._queue.put(event)

    async def close(self):
        """Close the stream."""
        await self._queue.put(None)


class EventFilter:
    """Filter events based on criteria."""

    def __init__(self):
        self.filters: List[Callable[[Event], bool]] = []

    def add_filter(self, filter_fn: Callable[[Event], bool]):
        """Add a filter function."""
        self.filters.append(filter_fn)

    def matches(self, event: Event) -> bool:
        """Check if event matches all filters."""
        return all(f(event) for f in self.filters)

    @staticmethod
    def by_type(event_type: str) -> Callable[[Event], bool]:
        """Filter by event type."""
        return lambda e: e.event_type == event_type

    @staticmethod
    def by_source(source: str) -> Callable[[Event], bool]:
        """Filter by event source."""
        return lambda e: e.source == source

    @staticmethod
    def by_priority(priority: str) -> Callable[[Event], bool]:
        """Filter by event priority."""
        return lambda e: e.priority == priority

    @staticmethod
    def by_correlation_id(correlation_id: str) -> Callable[[Event], bool]:
        """Filter by correlation ID."""
        return lambda e: e.correlation_id == correlation_id

    @staticmethod
    def by_payload_key(key: str, value: Any) -> Callable[[Event], bool]:
        """Filter by payload key/value."""
        return lambda e: e.payload.get(key) == value


class EventBusConnector:
    """Connector to integrate plugins with the VJSOS event bus."""

    def __init__(self, plugin_id: str, event_bus=None):
        self.plugin_id = plugin_id
        self.event_bus = event_bus
        self.publisher = EventPublisher(plugin_id, event_bus)
        self.subscriber = EventSubscriber(plugin_id, event_bus)

    async def connect(self):
        """Connect to the event bus."""
        await self.subscriber.start_listening()

    async def disconnect(self):
        """Disconnect from the event bus."""
        await self.subscriber.stop_listening()

    async def publish(self, event_type: str, payload: Dict[str, Any],
                     correlation_id: Optional[str] = None) -> Event:
        """Publish an event."""
        return await self.publisher.publish(event_type, payload, correlation_id)

    def on(self, event_type: str, handler: Callable):
        """Register an event handler."""
        self.subscriber.subscribe(event_type, handler)

    def off(self, event_type: str):
        """Unregister an event handler."""
        self.subscriber.unsubscribe(event_type)

    async def request_response(self, target: str, event_type: str,
                              payload: Dict[str, Any], timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Send a request and wait for response."""
        correlation_id = f"req_{uuid.uuid4().hex[:12]}"

        # Publish request
        await self.publisher.publish(
            event_type=f"{event_type}_request",
            payload=payload,
            correlation_id=correlation_id
        )

        # Wait for response (simplified - in real impl, would use message queue)
        return None


# Standard VJSOS event types
class SystemEvents:
    """Standard system event types."""
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    TASK_FEEDBACK = "task_feedback"
    QA_STARTED = "qa_started"
    QA_COMPLETED = "qa_completed"
    AGENT_HEARTBEAT = "agent_heartbeat"
    AGENT_STARTED = "agent_started"
    AGENT_STOPPED = "agent_stopped"
    DEPARTMENT_ANNOUNCEMENT = "department_announcement"
    GOVERNOR_DECISION = "governor_decision"
    SYSTEM_HEALTH = "system_health"
    CONFIG_CHANGED = "config_changed"
    PLUGIN_INSTALLED = "plugin_installed"
    PLUGIN_ACTIVATED = "plugin_activated"
    PLUGIN_DEACTIVATED = "plugin_deactivated"
    SKILL_REGISTERED = "skill_registered"
    SKILL_UPDATED = "skill_updated"
    MEMORY_STORED = "memory_stored"
    MEMORY_RETRIEVED = "memory_retrieved"