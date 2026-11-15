"""
Plugin SDK - Rate Limiter

Provides rate limiting enforcement for plugin API calls.
Supports both per-minute and per-hour limits with token bucket algorithm.
"""

import time
import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from collections import deque


@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    calls_per_minute: int = 1000
    calls_per_hour: int = 100000
    calls_per_day: int = 1000000
    burst_allowance: int = 100  # Allow burst of calls


@dataclass
class RateLimitState:
    """Current rate limit state."""
    minute_calls: int = 0
    hour_calls: int = 0
    day_calls: int = 0
    minute_start: float = field(default_factory=time.time)
    hour_start: float = field(default_factory=time.time)
    day_start: float = field(default_factory=time.time)


class RateLimiter:
    """Token bucket rate limiter for plugins."""

    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self.state = RateLimitState()
        self._lock = asyncio.Lock()
        self.call_history: deque = deque(maxlen=10000)  # For sliding window

    async def check_limit(self, cost: int = 1) -> Dict[str, Any]:
        """Check if a call is allowed under rate limits."""
        async with self._lock:
            now = time.time()
            self._reset_windows(now)

            # Check minute limit
            if self.state.minute_calls + cost > self.config.calls_per_minute:
                wait_time = 60 - (now - self.state.minute_start)
                return {
                    "allowed": False,
                    "reason": "minute_limit_exceeded",
                    "retry_after": wait_time,
                    "limit": self.config.calls_per_minute,
                    "used": self.state.minute_calls,
                    "remaining": max(0, self.config.calls_per_minute - self.state.minute_calls)
                }

            # Check hour limit
            if self.state.hour_calls + cost > self.config.calls_per_hour:
                wait_time = 3600 - (now - self.state.hour_start)
                return {
                    "allowed": False,
                    "reason": "hour_limit_exceeded",
                    "retry_after": wait_time,
                    "limit": self.config.calls_per_hour,
                    "used": self.state.hour_calls,
                    "remaining": max(0, self.config.calls_per_hour - self.state.hour_calls)
                }

            # Check day limit
            if self.state.day_calls + cost > self.config.calls_per_day:
                wait_time = 86400 - (now - self.state.day_start)
                return {
                    "allowed": False,
                    "reason": "day_limit_exceeded",
                    "retry_after": wait_time,
                    "limit": self.config.calls_per_day,
                    "used": self.state.day_calls,
                    "remaining": max(0, self.config.calls_per_day - self.state.day_calls)
                }

            # Allow the call
            self.state.minute_calls += cost
            self.state.hour_calls += cost
            self.state.day_calls += cost
            self.call_history.append({"timestamp": now, "cost": cost})

            return {
                "allowed": True,
                "limit_minute": self.config.calls_per_minute,
                "limit_hour": self.config.calls_per_hour,
                "limit_day": self.config.calls_per_day,
                "used_minute": self.state.minute_calls,
                "used_hour": self.state.hour_calls,
                "used_day": self.state.day_calls,
                "remaining_minute": self.config.calls_per_minute - self.state.minute_calls,
                "remaining_hour": self.config.calls_per_hour - self.state.hour_calls,
                "remaining_day": self.config.calls_per_day - self.state.day_calls
            }

    async def wait_if_needed(self, cost: int = 1) -> Dict[str, Any]:
        """Wait until rate limit allows the call."""
        while True:
            result = await self.check_limit(cost)
            if result["allowed"]:
                return result
            # Wait for the limit to reset
            wait_time = result.get("retry_after", 60)
            await asyncio.sleep(min(wait_time, 60))

    def _reset_windows(self, now: float):
        """Reset rate limit windows if they've expired."""
        if now - self.state.minute_start >= 60:
            self.state.minute_calls = 0
            self.state.minute_start = now

        if now - self.state.hour_start >= 3600:
            self.state.hour_calls = 0
            self.state.hour_start = now

        if now - self.state.day_start >= 86400:
            self.state.day_calls = 0
            self.state.day_start = now

    def get_status(self) -> Dict[str, Any]:
        """Get current rate limit status."""
        now = time.time()
        self._reset_windows(now)

        return {
            "minute": {
                "limit": self.config.calls_per_minute,
                "used": self.state.minute_calls,
                "remaining": max(0, self.config.calls_per_minute - self.state.minute_calls),
                "reset_at": self.state.minute_start + 60
            },
            "hour": {
                "limit": self.config.calls_per_hour,
                "used": self.state.hour_calls,
                "remaining": max(0, self.config.calls_per_hour - self.state.hour_calls),
                "reset_at": self.state.hour_start + 3600
            },
            "day": {
                "limit": self.config.calls_per_day,
                "used": self.state.day_calls,
                "remaining": max(0, self.config.calls_per_day - self.state.day_calls),
                "reset_at": self.state.day_start + 86400
            }
        }

    def reset(self):
        """Manually reset rate limit state."""
        self.state = RateLimitState()
        self.call_history.clear()


class SlidingWindowRateLimiter(RateLimiter):
    """Sliding window rate limiter for more precise limiting."""

    def __init__(self, config: Optional[RateLimitConfig] = None, window_seconds: int = 60):
        super().__init__(config)
        self.window_seconds = window_seconds

    async def check_limit(self, cost: int = 1) -> Dict[str, Any]:
        """Check limit using sliding window."""
        async with self._lock:
            now = time.time()
            window_start = now - self.window_seconds

            # Remove expired calls from history
            while self.call_history and self.call_history[0]["timestamp"] < window_start:
                self.call_history.popleft()

            # Count calls in window
            calls_in_window = sum(call["cost"] for call in self.call_history)

            limit = self.config.calls_per_minute  # Use minute limit for sliding window

            if calls_in_window + cost > limit:
                oldest = self.call_history[0] if self.call_history else {"timestamp": now}
                retry_after = max(0, self.window_seconds - (now - oldest["timestamp"]))
                return {
                    "allowed": False,
                    "reason": "sliding_window_exceeded",
                    "retry_after": retry_after,
                    "limit": limit,
                    "used": calls_in_window,
                    "remaining": max(0, limit - calls_in_window)
                }

            # Allow the call
            self.call_history.append({"timestamp": now, "cost": cost})
            return {
                "allowed": True,
                "limit": limit,
                "used": calls_in_window + cost,
                "remaining": limit - calls_in_window - cost
            }


class AdaptiveRateLimiter(RateLimiter):
    """Rate limiter that adapts based on server responses."""

    def __init__(self, config: Optional[RateLimitConfig] = None):
        super().__init__(config)
        self.error_count = 0
        self.success_count = 0
        self.backoff_factor = 1.0
        self.max_backoff = 60.0

    async def check_limit(self, cost: int = 1) -> Dict[str, Any]:
        """Check limit with adaptive backoff."""
        result = await super().check_limit(cost)

        # Apply backoff if we've seen recent errors
        if self.backoff_factor > 1.0 and result["allowed"]:
            # Reduce effective limit during backoff
            effective_minute_limit = int(self.config.calls_per_minute / self.backoff_factor)
            if self.state.minute_calls >= effective_minute_limit:
                return {
                    "allowed": False,
                    "reason": "adaptive_backoff",
                    "retry_after": 60 - (time.time() - self.state.minute_start),
                    "limit": effective_minute_limit,
                    "used": self.state.minute_calls,
                    "remaining": 0
                }

        return result

    def record_success(self):
        """Record a successful call."""
        self.success_count += 1
        self.error_count = max(0, self.error_count - 1)
        if self.success_count % 10 == 0:
            self.backoff_factor = max(1.0, self.backoff_factor * 0.9)

    def record_error(self, is_rate_limit: bool = False):
        """Record an error, potentially triggering backoff."""
        self.error_count += 1
        self.success_count = 0

        if is_rate_limit:
            self.backoff_factor = min(self.max_backoff, self.backoff_factor * 2.0)
        elif self.error_count >= 5:
            self.backoff_factor = min(self.max_backoff, self.backoff_factor * 1.5)

    def get_backoff_status(self) -> Dict[str, Any]:
        """Get current backoff status."""
        return {
            "backoff_factor": self.backoff_factor,
            "error_count": self.error_count,
            "success_count": self.success_count,
            "effective_minute_limit": int(self.config.calls_per_minute / self.backoff_factor)
        }