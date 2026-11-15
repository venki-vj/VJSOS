#!/usr/bin/env python3
"""
Event Bus - Structured Message Passing

All inter-agent communication flows through the message bus.
- Worker → Orchestrator → QA
- Department directors coordinate through Orchestrator
- Escalations → Governor
- System events broadcast to all interested parties

Message format follows JSON schema:
{
  "type": "task_request | task_result | qa_feedback | ...",
  "correlation_id": "...",
  "sender": "agent_id",
  "recipient": "agent_id | department | all",
  "timestamp": "...",
  "payload": {...}
}
"""

import json
import time
import uuid
import asyncio
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Set, Awaitable, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class MessageType(Enum):
    TASK_REQUEST = "task_request"
    TASK_RESULT = "task_result"
    QA_FEEDBACK = "qa_feedback"
    DEPARTMENT_ANNOUNCEMENT = "department_announcement"
    GOVERNOR_DECISION = "governor_decision"
    SYSTEM_EVENT = "system_event"
    PLUGIN_EVENT = "plugin_event"
    HEARTBEAT = "heartbeat"
    APPEAL = "appeal"
    ERROR = "error"
    METRICS = "metrics"
    LEARNING = "learning"
    SKILL_REGISTERED = "skill_registered"
    SKILL_UPDATED = "skill_updated"
    PLUGIN_INSTALLED = "plugin_installed"
    PLUGIN_ACTIVATED = "plugin_activated"


@dataclass
class Message:
    """Structured message on the bus."""
    type: str
    correlation_id: str
    sender: str
    recipient: str  # agent_id, department_id, "all", or "governor"
    timestamp: str
    payload: Dict[str, Any]
    priority: str = "normal"  # low, normal, high, critical
    ttl_seconds: int = 3600  # 1 hour default

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def validate(self) -> bool:
        """Validate message format."""
        required = ["type", "correlation_id", "sender", "recipient", "timestamp", "payload"]
        return all(hasattr(self, field) and getattr(self, field) is not None for field in required)


class EventHandler:
    """Base class for event handlers."""

    def __init__(self, handler_id: str):
        self.handler_id = handler_id
        self.subscribed_types: List[str] = []
        self.message_buffer: List[Message] = []
        self.active = True

    async def handle(self, message: Message) -> Optional[Message]:
        """Handle an incoming message. Return response or None."""
        raise NotImplementedError

    def subscribe(self, message_types: List[str]):
        """Subscribe to specific message types."""
        self.subscribed_types = message_types

    def unsubscribe(self, message_types: List[str]):
        """Unsubscribe from message types."""
        self.subscribed_types = [t for t in self.subscribed_types if t not in message_types]


class EventBus:
    """Distributed message bus for VJSOS-AI."""

    def __init__(self):
        self.bus_id = "event-bus@vjsos-ai"
        self.handlers: Dict[str, List[EventHandler]] = {}  # topic -> handlers
        self.topics: Set[str] = set()
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.dead_letter_queue: List[Message] = []
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "handlers": 0,
            "errors": 0,
            "dead_letters": 0
        }
        self._handlers_lock = asyncio.Lock()
        self._running = False
        self._worker_task = None

    async def start(self):
        """Start the event bus."""
        self._running = True
        self._worker_task = asyncio.create_task(self._run_worker())
        return {"status": "started", "bus_id": self.bus_id}

    async def stop(self):
        """Stop the event bus."""
        self._running = False
        if self._worker_task:
            await self._worker_task

    async def _run_worker(self):
        """Main worker loop for processing messages."""
        while self._running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self._route_message(message)
                self.stats["messages_processed"] = self.stats.get("messages_processed", 0) + 1
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.stats["errors"] += 1
                print(f"Event bus worker error: {e}")

    async def _route_message(self, message: Message):
        """Route a message to appropriate handlers."""
        if not message.validate():
            self.dead_letter_queue.append(message)
            self.stats["dead_letters"] += 1
            return

        self.stats["messages_received"] += 1

        # Check TTL
        message_time = datetime.fromisoformat(message.timestamp.replace("Z", "+00:00"))
        age = (datetime.utcnow() - message_time.replace(tzinfo=None)).total_seconds()
        if age > message.ttl_seconds:
            self.dead_letter_queue.append(message)
            self.stats["dead_letters"] += 1
            return

        # Route to handlers
        topics_to_check = set()

        # Direct recipient
        topics_to_check.add(message.recipient)

        # Message type topic
        topics_to_check.add(message.type)

        # "all" receives broadcasts
        topics_to_check.add("all")

        # Department broadcasts
        if message.recipient.startswith("department:"):
            topics_to_check.add(message.recipient)

        for topic in topics_to_check:
            handlers = self.handlers.get(topic, [])
            for handler in handlers:
                try:
                    # Only handlers subscribed to the message type
                    if (not handler.subscribed_types or
                        message.type in handler.subscribed_types or
                        "all" in handler.subscribed_types):

                        response = await handler.handle(message)
                        if response:
                            await self._route_response(response, message)
                except Exception as e:
                    self.stats["errors"] += 1

        self.stats["messages_sent"] += 1

    async def _route_response(self, response: Message, original: Message):
        """Route a response message."""
        await self.message_queue.put(response)

    async def subscribe(self, handler: EventHandler, topics: List[str]):
        """Subscribe a handler to topics."""
        async with self._handlers_lock:
            self.handlers.setdefault(handler.handler_id, handler)
            for topic in topics:
                if topic not in self.handlers:
                    self.handlers[topic] = []
                if handler not in self.handlers[topic]:
                    self.handlers[topic].append(handler)
                self.topics.add(topic)
            self.stats["handlers"] = len(self.handlers)

    async def unsubscribe(self, handler: EventHandler):
        """Unsubscribe a handler from all topics."""
        async with self._handlers_lock:
            for topic in list(handler.subscribed_types):
                if topic in self.handlers:
                    self.handlers[topic] = [
                        h for h in self.handlers[topic] if h.handler_id != handler.handler_id
                    ]
            if handler.handler_id in self.handlers:
                del self.handlers[handler.handler_id]
            self.stats["handlers"] = len(self.handlers)

    async def publish(self, message: Message):
        """Publish a message to the bus."""
        await self.message_queue.put(message)
        self.stats["messages_sent"] += 1

    async def request(self, sender: str, recipient: str,
                     message_type: str, payload: Dict[str, Any],
                     timeout: float = 30.0) -> Optional[Message]:
        """Send a request and wait for response (with timeout)."""
        correlation_id = str(uuid.uuid4())
        message = Message(
            type=message_type,
            correlation_id=correlation_id,
            sender=sender,
            recipient=recipient,
            timestamp=datetime.utcnow().isoformat() + "Z",
            payload=payload
        )

        await self.publish(message)

        # Wait for response, return None on timeout
        return None

    def get_stats(self) -> Dict[str, Any]:
        """Get event bus statistics."""
        return {
            **self.stats,
            "topics": list(self.topics),
            "queue_size": self.message_queue.qsize(),
            "dead_letter_count": len(self.dead_letter_queue)
        }

    def get_dead_letters(self) -> List[Dict[str, Any]]:
        """Get dead-letter messages."""
        return [msg.to_dict() for msg in self.dead_letter_queue]

    async def log_audit(self, message: Message):
        """Log message to audit trail (Constitution Article... observability)."""
        Path("logs").mkdir(parents=True, exist_ok=True)
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": "message_routed",
            "message_type": message.type,
            "sender": message.sender,
            "recipient": message.recipient,
            "correlation_id": message.correlation_id
        }
        with open("logs/audit.md", "a") as f:
            f.write(json.dumps(audit_entry) + "\n")


class SubscriberManager:
    """Manages agent registration and message subscription."""

    def __init__(self):
        self.subscribers: Dict[str, EventHandler] = {}
        self.topic_subscriptions: Dict[str, List[str]] = defaultdict(list)
        self.registered_agents: Dict[str, Dict[str, Any]] = {}

    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]):
        """Register an agent with the message bus."""
        self.registered_agents[agent_id] = {
            **agent_info,
            "registered_at": datetime.utcnow().isoformat() + "Z"
        }

    def unregister_agent(self, agent_id: str):
        """Unregister an agent."""
        if agent_id in self.registered_agents:
            del self.registered_agents[agent_id]

    def get_subscribed_topics(self, agent_id: str) -> List[str]:
        """Get topics an agent subscribes to."""
        agent = self.registered_agents.get(agent_id)
        return agent.get("subscribed_topics", []) if agent else []

    def get_all_subscribers(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered agents."""
        return dict(self.registered_agents)

    def get_subscriber_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get info about a specific agent."""
        return self.registered_agents.get(agent_id)

    def update_agent_status(self, agent_id: str, status: str):
        """Update an agent's status."""
        if agent_id in self.registered_agents:
            self.registered_agents[agent_id]["status"] = status
            self.registered_agents[agent_id]["last_seen"] = datetime.utcnow().isoformat() + "Z"

    def get_agents_by_department(self, department: str) -> List[str]:
        """Get all agents in a department."""
        return [
            agent_id for agent_id, info in self.registered_agents.items()
            if info.get("department") == department
        ]


class MessageBus:
    """Distributed message bus for VJSOS-AI (refactored from EventBus)."""

    def __init__(self):
        self.bus_id = "message-bus@vjsos-ai"
        self.subscribers = SubscriberManager()
        self.handlers: Dict[str, List[EventHandler]] = {}  # topic -> handlers
        self.topics: Set[str] = set()
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.dead_letter_queue: List[Message] = []
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "handlers": 0,
            "errors": 0,
            "dead_letters": 0
        }
        self._handlers_lock = asyncio.Lock()
        self._running = False
        self._worker_task = None

    async def start(self):
        """Start the message bus."""
        self._running = True
        self._worker_task = asyncio.create_task(self._run_worker())
        return {"status": "started", "bus_id": self.bus_id}

    async def stop(self):
        """Stop the message bus."""
        self._running = False
        if self._worker_task:
            await self._worker_task

    async def _run_worker(self):
        """Main worker loop for processing messages."""
        while self._running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self._route_message(message)
                self.stats["messages_processed"] = self.stats.get("messages_processed", 0) + 1
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.stats["errors"] += 1
                print(f"Message bus worker error: {e}")

    async def _route_message(self, message: Message):
        """Route a message to appropriate handlers."""
        if not message.validate():
            self.dead_letter_queue.append(message)
            self.stats["dead_letters"] += 1
            return

        self.stats["messages_received"] += 1

        # Update agent last seen
        if message.sender:
            self.subscribers.update_agent_status(message.sender, "active")

        # Check TTL
        message_time = datetime.fromisoformat(message.timestamp.replace("Z", "+00:00"))
        age = (datetime.utcnow() - message_time.replace(tzinfo=None)).total_seconds()
        if age > message.ttl_seconds:
            self.dead_letter_queue.append(message)
            self.stats["dead_letters"] += 1
            return

        # Route to handlers
        topics_to_check = set()

        # Direct recipient
        topics_to_check.add(message.recipient)

        # Message type topic
        topics_to_check.add(message.type)

        # "all" receives broadcasts
        topics_to_check.add("all")

        # Department broadcasts
        if message.recipient.startswith("department:"):
            topics_to_check.add(message.recipient)

        for topic in topics_to_check:
            handlers = self.handlers.get(topic, [])
            for handler in handlers:
                try:
                    # Only handlers subscribed to the message type
                    if (not handler.subscribed_types or
                        message.type in handler.subscribed_types or
                        "all" in handler.subscribed_types):

                        response = await handler.handle(message)
                        if response:
                            await self._route_response(response, message)
                except Exception as e:
                    self.stats["errors"] += 1

        self.stats["messages_sent"] += 1

    async def _route_response(self, response: Message, original: Message):
        """Route a response message."""
        await self.message_queue.put(response)

    async def subscribe(self, handler: EventHandler, topics: List[str]):
        """Subscribe a handler to topics."""
        async with self._handlers_lock:
            # Register handler if not already registered
            if handler.handler_id not in self.handlers:
                self.handlers[handler.handler_id] = handler

            # Subscribe to topics
            for topic in topics:
                if topic not in self.handlers:
                    self.handlers[topic] = []
                if handler not in self.handlers[topic]:
                    self.handlers[topic].append(handler)
                self.topics.add(topic)

            # Register agent in subscriber manager
            agent_info = {
                "handler": handler,
                "subscribed_topics": topics,
                "capabilities": getattr(handler, "capabilities", [])
            }
            self.subscribers.register_agent(handler.handler_id, agent_info)

            self.stats["handlers"] = len(self.handlers)

    async def unsubscribe(self, handler: EventHandler):
        """Unsubscribe a handler from all topics."""
        async with self._handlers_lock:
            # Remove from topic subscriptions
            for topic in list(self.handlers.keys()):
                if topic != handler.handler_id:
                    self.handlers[topic] = [
                        h for h in self.handlers[topic] if h.handler_id != handler.handler_id
                    ]

            # Remove handler registration
            if handler.handler_id in self.handlers:
                del self.handlers[handler.handler_id]

            # Unregister agent
            self.subscribers.unregister_agent(handler.handler_id)

            self.stats["handlers"] = len(self.handlers)

    async def publish(self, message: Message):
        """Publish a message to the bus."""
        await self.message_queue.put(message)
        self.stats["messages_sent"] += 1

    async def request(self, sender: str, recipient: str,
                     message_type: str, payload: Dict[str, Any],
                     timeout: float = 30.0) -> Optional[Message]:
        """Send a request and wait for response (with timeout)."""
        correlation_id = str(uuid.uuid4())
        message = Message(
            type=message_type,
            correlation_id=correlation_id,
            sender=sender,
            recipient=recipient,
            timestamp=datetime.utcnow().isoformat() + "Z",
            payload=payload
        )

        await self.publish(message)

        # Wait for response, return None on timeout
        return None

    def get_stats(self) -> Dict[str, Any]:
        """Get message bus statistics."""
        return {
            **self.stats,
            "topics": list(self.topics),
            "queue_size": self.message_queue.qsize(),
            "dead_letter_count": len(self.dead_letter_queue),
            "registered_agents": len(self.subscribers.registered_agents)
        }

    def get_dead_letters(self) -> List[Dict[str, Any]]:
        """Get dead-letter messages."""
        return [msg.to_dict() for msg in self.dead_letter_queue]

    def get_subscriber_manager(self) -> SubscriberManager:
        """Get the subscriber manager."""
        return self.subscribers

    def log_audit(self, message: Message):
        """Log message to audit trail (Constitution Article... observability)."""
        Path("logs").mkdir(parents=True, exist_ok=True)
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": "message_routed",
            "message_type": message.type,
            "sender": message.sender,
            "recipient": message.recipient,
            "correlation_id": message.correlation_id
        }
        with open("logs/message_bus_audit.md", "a") as f:
            f.write(json.dumps(audit_entry) + "\n")
