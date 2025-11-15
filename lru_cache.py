from typing import Tuple
import heapq

class LRUCache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.cache = {}
        self.last_accessed_at = {}
        self.ts = 0
        self.time_queue = []

    def get(self, key: int) -> int:
        # O(1)
        self._update_access_times(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        # O(n)
        self._evict_lru_if_needed()
        self._update_access_times(key)
        self.cache[key] = value

    def delete(self, key: int) -> None:
        #O(1)
        self.cache.pop(key)
        self.last_accessed_at.pop(key)

    def _evict_lru_if_needed(self):
        if len(self.cache) < self.max_size:
            return
        while True:
            ts, key = heapq.heappop(self.time_queue)
            if self.last_accessed_at.get(key) != ts:
                continue
            self.delete(key)
            return

    def _update_access_times(self, key: int):
        self.ts+=1
        self.last_accessed_at[key] = self.ts
        heapq.heappush(self.time_queue, (self.ts, key))

lru = LRUCache(max_size=3)
lru.put(1, 2)
lru.put(2, 4)
lru.put(3, 6)
assert len(lru.cache) == 3 
assert lru.get(1) == 2
lru.put(4, 8)
assert len(lru.cache) == 3 
assert 2 not in lru.cache