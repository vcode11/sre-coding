import threading
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: int):
        self.capacity = capacity
        self.refill_rate_per_sec = refill_rate_per_sec
        self.tokens = capacity
        self.lock = threading.Lock()
        self.last_fill_time = time.time()
    
    def _refill(self):
        with self.lock:
            curr = time.time()
            elapsed = curr - self.last_fill_time
            tokens_to_refill = int(elapsed*self.refill_rate_per_sec)
            self.tokens = min(self.capacity, self.tokens + tokens_to_refill)
            self.last_fill_time = curr

    def _is_allowed(self, tokens_needed: int) -> bool:
        if tokens_needed <= self.tokens:
            self.tokens -= tokens_needed
            return True
        else: 
            return False

    def allow_request(self, tokens_needed: int) -> bool:
        if self._is_allowed(tokens_needed):
            return True
        self._refill()
        return self._is_allowed(tokens_needed)
    

rate_limiter = TokenBucketRateLimiter(capacity=5, refill_rate_per_sec=1)
assert rate_limiter.allow_request(10) is False
assert rate_limiter.allow_request(5) is True
time.sleep(1)
assert rate_limiter.allow_request(1) is True