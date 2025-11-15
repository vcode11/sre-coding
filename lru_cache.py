from dataclasses import dataclass
import heapq
from typing import Any, Dict, Tuple

@dataclass
class ListNode:
    _next: Any # type: ignore # noqa: F821
    _prev: Any
    value: Tuple[int, int]

    __slots__ = ("_next", "_prev", "value")

    def __eq__(self, other):
        return self.value == other.value


@dataclass
class DLL:
    head: ListNode
    tail: ListNode

    __slots__ = ("head", "tail")

    def __str__(self):
        values = []
        curr = self.head
        while curr is not None:
            values.append(curr.value)
            curr = curr._next

        return str(values)
    
    def pop_front(self):
        if self.head is None:
            return 
        if self.head == self.tail:
            self.head = self.tail = None
            return
        assert self.head._prev is None
        next_node = self.head._next
        next_node._prev = None
        self.head._next = None
        self.head = next_node
    
    def pop_back(self):
        print(self)
        if self.tail is None:
            return
        if self.head == self.tail:
            self.head = self.tail = None
            return
        prev_node = self.tail._prev
        assert prev_node is not None
        assert self.tail._next is None

        prev_node._next = None
        self.tail._prev = None

        self.tail = prev_node

    
    def remove(self, node):
        if node == self.head:
            return self.pop_front()
        if node == self.tail:
            return self.pop_back()
        print(node.value, self.tail.value, (node == self.tail), sep=', ')
        assert node._next is not None
        assert node._prev is not None
        prev_node = node._prev
        next_node = node._next
        prev_node._next = None
        next_node._prev = None
    
    def append_front(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
            return node
        if self.head == self.tail:
            self.tail._prev = node
            node._next = self.tail
            self.head = node
            return 
        node._next = self.head
        self.head._prev = node
        self.head = node

class LRUCacheDLL:
    def __init__(self, max_size):
        self.max_size = max_size
        self.dll = DLL(head=None, tail=None)
        assert self.dll is not None
        self.cache: Dict[int, ListNode] = {}
    
    def __str__(self):
        return f"{self.cache}"

    def get(self, key):
        node = self.cache[key]
        self.dll.remove(node)
        self.dll.append_front(node)
        return node.value[1]
    
    def _evict_lru_if_needed(self):
        if len(self.cache) >= self.max_size:
            tail = self.dll.tail
            self.dll.remove(tail)
            self.cache.pop(tail.value[0])

    def put(self, key, value):
        self._evict_lru_if_needed()
        node = ListNode(
            _next=None,
            _prev=None,
            value=(key,value)
        )
        self.cache[key] = node
        self.dll.append_front(node)

    def delete(self, key):
        node = self.cache.pop(key)
        self.dll.remove(node)

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

lru = LRUCacheDLL(max_size=3)
lru.put(1, 2)
lru.put(2, 4)
lru.put(3, 6)

assert len(lru.cache) == 3 
assert lru.get(1) == 2, f"Got {lru.get(1)}"
assert len(lru.cache) == 3 
assert 2 not in lru.cache